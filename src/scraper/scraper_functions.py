import re
from urllib.request import urlopen
import urllib
from time import sleep
from datetime import datetime
import random
import logging

from bs4 import BeautifulSoup
import pymysql
import scraper.settings as settings


# Import Project Modules ---------------------------------------------
import scraper.sql_functions as m1
import scraper.bot_protections as m2
import scraper.zillow_api as m3

# Instantiate Connect to MySQL ---------------------------------------
mydb = pymysql.connect(
    host=settings.host,
    user=settings.user,
    passwd=settings.password,
    database=settings.database)

# Functions -----------------------------------------------------------


# GET BEAUTIFUL SOUP OBJECT OF PAGE OR TOTAL NUMBER OF PAGES TO SCRAPE--------------
def get_bsObj_main_page(city, state, pprint=False):
    '''
    Purpose:    Obtain the bsObj for the main page where the list of houses are located.
    Input:      Seach criteria includes the city and state where the house is located
                The purpose of the page input is to iterate each of the pages to scrape
                more housing data.
    **Note:     We should expand the search criteria to include other limiting fields.
    Output:     The user may chose to output the max page number from the page
                or return the bsObj of the page '''
    # Define url object
    url = 'https://www.zillow.com/homes/{},-{}_rb/'.format(city, state)

    # Generate Random Header (serves to fake bot protections)
    random_header = m2.generate_ran_headers()

    # Generate the url request with zillow headings
    Content = urllib.request.Request(url, headers=random_header)

    html = urlopen(Content)
    # Create Beautifulsoup object
    bsObj = BeautifulSoup(html.read(), 'lxml')

    # Logging
    if pprint:
        print(bsObj.prettify())

    # Return bsObj
    return bsObj, url


def get_max_page_num(bsObj):
    '''
    Purpose:    Get the max page number from the main page
    Input:      The bsObj from the main page.
    Output:     Int value of last page'''

    # Get Tag Containing totalPages value
    links_pages = str(bsObj.find('script', {'data-zrr-shared-data-key': 'mobileSearchPageStore'}))

    # Use Regex Statement to Obtain phrase "total_Pages:##"
    '''Assuming totalPages exists on the first page, re_search will
       return a string that looks like 'totalPages":18'
    '''
    regex = re.compile('totalPages":[0-9][0-9]')

    # Try to get total page numbers
    try:
        re_search = re.findall(regex, links_pages)[0]
        # Get Number after colon from re_search result return ['##']
        regex_2 = re.compile('[0-9][0-9]')
        re_search = re.findall(regex_2, re_search)
        # Result
        return int(re_search[0])

    except IndexError as err:
        logging.info('max page number generated an error')
        logging.warning(err)
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_max_page_num', 'url',
                                   'Attempt to obtain max page number failed. Returning max page num = 20', str(err))
        return 20

    except TypeError as err:
        logging.info('max page number generated an error')
        logging.warning(err)
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_max_page_num', 'url',
                                   'Attempt to obtain max page number failed.  Returning max page num = 20', str(err))
        return 20

# GET LIST OF HOMES --------------------------------------------------


def get_list_homes(bsObj, url):
    '''Descr:   Obtain the photo-card object for each of the homes listed
                on the main page.  There is import information that can be
                scraped directly from the card like price, address, etc.
        '''

    try:
        photo_cards = bsObj.find('ul', {'class': 'photo-cards'})
        list_homes = photo_cards.findAll('li')
        return list_homes
    except AttributeError as err:
        logging.warning('Attribute error generated from find property-photo-card request.  Possibly due to bad tag request or website scraper protections')
        logging.warning(err)
        logging.info('Sleep for 30 seconds')
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_list_homes', url,
                                   'Error possible due to website scraper protections', str(err))
        # Sleep for 30 Seconds and Try Again
        sleep(30)
        try:
            logging.info('Trying a different approach')
            photo_cards = bsObj.find('ul', {'class': 'photo-cards photo-cards_wow'})
            list_homes = photo_cards.findAll('li')
            return list_homes
        except AttributeError as err:
            logging.warning('Unable to retreive the photocard tag')
            m1.sql_insert_warning_logs(mydb, 'module_1', 'get_list_homes', url,
                                       'Second attempt failed to retrieve property-photo-card', str(err))


# GET ZIP CODE----------------------------------------------------------
def clean_house_tags_4_address_zipcode_scrape(home_data):
    # Limit to specific tags contianing this phrase
    if '<li><script type="application/ld+json">' in str(home_data):
        home_data = str(home_data)
        regex = re.compile('name.*","floor')
        re_search = re.search(regex, home_data)
        re_group = re_search.group()
        remove_front = re_group.split(':')[1]
        remove_back = remove_front.split('floor')[0]
        remove_punct = remove_back.replace('"', '')
        # return clean tag containing address & zipcode
        return remove_punct
    return ''


def get_zip_code(clean_house_tag):
    # Search for zipcode
    regex_zip_code = re.compile('[0-9]{5},')
    re_search_zip = re.search(regex_zip_code, clean_house_tag)
    re_group_zip = re_search_zip.group()
    zip_code = re_group_zip.split(',')[0]
    # Return Zip Code
    return zip_code

# GET ADDRESS ----------------------------------------------------------


def get_address(clean_house_tag):
    ''' The first comma follows the street name and is followed by the city.
        therefore, we should be able to split on the comma and take the string
            value in the index = 0 position to be the address'''
    address = clean_house_tag.split(',')[0]
    return address


# GET URL ---------------------------------------------------------------------
def get_url(home_data):
    if 'url' in str(home_data):

        regex_href = re.compile('/homedetails/.+_zpid/"}')
        re_search = re.search(regex_href, str(home_data))
        href = re_search.group().split('"')[0]
        return href
    return ''


# GET SCHOOL RANKINGS ----------------------------------------------------------

def get_school_ranking(url):
    url_full = 'https://www.zillow.com' + url
    Content = urllib.request.Request(url_full, headers={
        'authority': 'www.zillow.com',
        'method': 'GET',
        'path': '/homes/',
        'scheme': 'https',
        'user-agent':
        ''''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
        AppleWebKit/537.36 (KHTML, like Gecko)
        Chrome/61.0.3163.100 Safari/537.36'''})

    html = urlopen(Content)
    # Create Beautifulsoup object
    bsObj = BeautifulSoup(html.read(), 'lxml')

    # Try to Get School Ratings
    try:
        # Get Tags Associated with Shools
        school_list = bsObj.findAll('ul', {'class': 'ds-nearby-schools-list'})

        # Find All Span Tags (these tags include the ratings)
        span = school_list[0].findAll('span')

        # Create List of School values
        list_ratings = [span[0].text, span[5].test, span[10].text]

        # Return values
        return list_ratings

    except IndexError as err:
        logging.warning('\nSchool list => %s', school_list)
        logging.warning('School ratings function generated an error => %s', err)
        logging.warning('Url that generated the error => %s', url_full)
        logging.warning(err)
        logging.warning('Trying a different technique\n')
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_school_rankings', url,
                                   'Error possibly due to missing data point', str(err))
        # return list of all zeros
        return [0, 0, 0]
    except ValueError as err:
        logging.warning('Get school ranking function generated and error => %s', err)
        logging.warning('Returning 0,0,0')
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_school_rankings', url,
                                   'Second attempt to retrieve school rankings', str(err))
        # return list of all zeros
        return [0, 0, 0]


def get_sale_asking_price(home, url):
    '''
    Purpose:	Get the asking price for the house from the photo tag
    home:		The input value is the individual home tag
    url:        used for logging
    This function sits within the "for home in list_homes" loop.
    Output:		Integer value for asking price
    '''
    # Test if we can find the article tag

    try:
        list_price = home.find('div', {'class': 'list-card-price'})\
            .text.replace('$', '').replace(',', '')

        # Return asking price as an integer
        return int(list_price)

    # Except an attribute error where no tag is found
    except AttributeError as err:
        logging.warning('Get asking price generated an error => %s', err)
        logging.warning('Returning asking price => $%s', '0')
        # Insert warning into database
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_sale_asking_price', url,
                                   'Value likely not found.  Returning 0', str(err))

        return 0

    # Except ValueError - some values look like this 'Est. 166283'
    except ValueError as err:
        logging.warning('Get asking price generated an error => %s', err)
        logging.warning('Try removing text in asking price')
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_sale_asking_price', url,
                                   'Value likely not found.  Returning 0', str(err))

        try:
            list_price_new = list_price.replace('Est.', '').replace('+', '').replace('++', '')\
                .replace('--', '')
            if list_price_new is not None:
                logging.info('Asking price scraped successfully')
                return int(list_price)
            logging.warning('Unable to obtain asking price.  Returning $0')

        except ValueError:
            logging.warning('Unable to clean asking price.  Returning $0')

        return 0


def main_get_home_data(city, state, bsObj, url):

    # Get Max Page Number
    max_page_num = get_max_page_num(bsObj)

    # Iterate Over Pages (max_page_num because its up to but not including)
    for page_num in range(1, max_page_num + 1):

        # User Info
        print('Scraping page {} of {} -----------------------------------------'
              .format(page_num, max_page_num))

        # Generate Datetime Object
        pull_date = datetime.today().date()

        # Get Beautiful Soup Object of Page N that contain links to each home listing
        bsObj = get_bsObj_main_page(city, state, page_num)

        # Get List of Houses (Photo-cards) for each page)
        list_homes = get_list_homes(bsObj, url)

        # Count Homes Scraped Obj
        count_homes_scraped = 0

        # Loop over home tags and scrape data --------------------------------
        if list_homes:

            for home in list_homes:

                # Get Tag Containing Address & Zip Code
                clean_house_tags = clean_house_tags_4_address_zipcode_scrape(home)

                # Function may return null obj. Pass if None.
                if not clean_house_tags:
                    logging.info('No house tags found')

                else:
                    # Get Url
                    url = get_url(home)

                    # Get Home Details -------------------------------------------

                    # Get Asking Price
                    asking_price = get_sale_asking_price(home, url)

                    # Num home object
                    total_homes_on_page = len(list_homes)

                    # Get Zipcode
                    zip_code = get_zip_code(clean_house_tags)

                    # Get Address
                    address = get_address(clean_house_tags)

                    # Insert Location
                    val_addresses = [address, state, zip_code, city, pull_date, url]
                    m1.sql_insert_function_addresses(mydb, val_addresses)

                    # Get Zillow Data-------------------- ------------------------------
                    val_zillow_api_data = m3.get_house_data_zillow_api(address, zip_code,
                                                                       pull_date, asking_price, url)
                    m1.sql_insert_function_zillow_api_data(mydb, val_zillow_api_data)

                    # Get School Ranking Data ------------------------------------------
                    school_rankings = get_school_ranking(url)
                    m1.sql_insert_function_schools(mydb, school_rankings, address,
                                                   pull_date, url)

                    # Increment Num homes
                    print('{} of {} home data scraped'.format(
                        count_homes_scraped, total_homes_on_page))
                    count_homes_scraped += 1

            # Generate Random Sleep Period
            print('Data successfully scraped for page {}'.format(page_num))
            sleep_seconds = random.randint(5, 10)
            print('Sleeping for {} seconds\n'.format(sleep_seconds))
            sleep(sleep_seconds)

        # No Homes Found
        else:
            logging.warning('No homes found in search.  Ending scraper program')
