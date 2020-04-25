import re
import sys
from io import StringIO
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib
from time import sleep
from datetime import datetime
import random
import mysql.connector
import pyzillow
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails
from time import sleep
import logging


# Import Project Modules ---------------------------------------------
import sql_functions as m1

# Instantiate Connect to MySQL ---------------------------------------
mydb = mysql.connector.connect(
        host='localhost',
        user= input('Username => '),
        passwd= input('Password => '),
        database='upwork_test_db',
        auth_plugin='mysql_native_password')


# Functions -----------------------------------------------------------

def get_max_page_num(bsObj):
    '''
    Purpose:    Get the max page number from the main page
    Input:      The bsObj from the main page.
    Output:     Int value of last page'''

    # Get Tag Containing totalPages value
    links_pages = str(bsObj.find('script', {'data-zrr-shared-data-key':'mobileSearchPageStore'}))

    # Use Regex Statement to Obtain phrase "total_Pages:##"
    '''Assuming totalPages exists on the first page, re_search will
       return a string that looks like 'totalPages":18'
    '''
    regex = re.compile('totalPages":[0-9][0-9]')
    re_search = re.findall(regex, links_pages)[0]

    # Get Number after colon from re_search result return ['##']
    regex_2 = re.compile('[0-9][0-9]')
    re_search = re.findall(regex_2, re_search)

    # Result
    return re_search[0]


# GET BEAUTIFUL SOUP OBJECT OF PAGE OR TOTAL NUMBER OF PAGES TO SCRAPE--------------
def get_bsObj_main_page(city, state, page, pprint=False):
    '''
    Purpose:    Obtain the bsObj for the main page where the list of houses are located.
    Input:      Seach criteria includes the city and state where the house is located
                The purpose of the page input is to iterate each of the pages to scrape
                more housing data.
    **Note:     We should expand the search criteria to include other limiting fields.
    Output:     The user may chose to output the max page number from the page
                or return the bsObj of the page '''
    # Define url object
    url = 'https://www.zillow.com/homes/for_sale/{},-{}_rb/{}/'.format(city, state, page)

     # Generate the url request with zillow headings
    Content = urllib.request.Request(url, headers={
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

    # Logging
    if pprint==True:
        print(bsObj.prettify())

    # Return bsObj
    return bsObj




def test_scraper_protections(state, city, count=1, pprint=False):
    ''' Desc:  The purpose is to test the scraping protections of the
                web page before initializing the scraper.
                This function will run for 10 iterations before it will
                stop.
    '''
    # Logging
    if count==1:
        logging.info('\nInitializing testing scraper protections\n')

    # Statement
    PHRASE = "Please verify you're a human to continue"

    # Duration
    rand_dur = random.randint(10,30)


    # Check for web scraper protections
    logging.info('Iteration {}, testing web page scraper protections'.format(count))
    bsObj = get_bsObj_main_page(city, state, 1)
    bsObj_str = str(bsObj)

    # Determine when to end
    if count < 10:

        # Check if protections blocking scraper
        if PHRASE in bsObj_str:
            logging.info('Web page protections are blocking the scraper')
            logging.info('Sleeping for {} seconds'.format(rand_dur))
            sleep(rand_dur)
            # Increase Count
            count += 1
            # Rerun scraper protection function
            test_scraper_protections(state, city, count=count)

        else:
            logging.info('Scraper protection test passed.  Initiate scraper')
            return True
    else:
        logging.warning('Unable to pass scraper protections. Try again later')




# GET LIST OF HOMES --------------------------------------------------
def get_list_homes(bsObj):
    '''Descr:   Obtain the photo-card object for each of the homes listed
                on the main page.  There is import information that can be
                scraped directly from the card like price, address, etc.
	'''
    url = bsObj[1]
    bsObj = bsObj[0]

    try:
        photo_cards = bsObj.find('ul', {'class':'photo-cards'})
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
            photo_cards = bsObj.find('ul', {'class':'photo-cards photo-cards_wow'})
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
		home_data    = str(home_data)
		regex        = re.compile('name.*","floor')
		re_search    = re.search(regex, home_data)
		re_group     = re_search.group()
		remove_front = re_group.split(':')[1]
		remove_back  = remove_front.split('floor')[0]
		remove_punct = remove_back.replace('"', '')
		# return clean tag containing address & zipcode
		return remove_punct

def get_zip_code(clean_house_tag):
	# Search for zipcode
	regex_zip_code = re.compile('[0-9]{5},')
	re_search_zip  = re.search(regex_zip_code, clean_house_tag)
	re_group_zip   = re_search_zip.group()
	zip_code       = re_group_zip.split(',')[0]
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
		re_search  = re.search(regex_href, str(home_data))
		href     = re_search.group().split('"')[0]
		return href



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
        school_list = bsObj.findAll('ul', {'class':'ds-nearby-schools-list'})

        # Find All Span Tags (these tags include the ratings)
        span = school_list[0].findAll('span')

        # Create List of School values
        list_ratings = [span[0].text, span[5].test, span[10].text]

        # Return values
        return list_ratings

    except IndexError as err:
        logging.warning('\nSchool list => {}'.format(school_list))
        logging.warning('School ratings function generated an error => {}'.format(err))
        logging.warning('Url that generated the error => {}'.format(url_full))
        logging.warning(err)
        logging.warning('Trying a different technique\n')
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_school_rankings', url,
                                   'Error possibly due to missing data point', str(err))
        # return list of all zeros
        return [0, 0, 0]
    except ValueError as err:
        logging.warning('Get school ranking function generated and error => {}'.format(err))
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
        list_price = home.find('div', {'class':'list-card-price'})\
                    .text.replace('$','').replace(',','')

        # Return asking price as an integer
        return int(list_price)

    # Except an attribute error where no tag is found
    except AttributeError as err:
        logging.warning('Get asking price generated an error => {}'.format(err))
        logging.warning('Returning asking price => ${}'.format('0'))
        # Insert warning into database
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_sale_asking_price', url,
                              'Value likely not found.  Returning 0', str(err))

        return 0

    # Except ValueError - some values look like this 'Est. 166283'
    except ValueError as err:
        logging.warning('Get asking price generated an error => {}'.format(err))
        logging.warning('Try removing text in asking price')
        m1.sql_insert_warning_logs(mydb, 'module_1', 'get_sale_asking_price', url,
                              'Value likely not found.  Returning 0', str(err))

        try:
            list_price_new = list_price.replace('Est.','').replace('+','').replace('++','')\
                .replace('--','')
            if list_price_new != None:
                logging.info('Asking price scraped successfully')
                return int(list_price)
            else:
                logging.warning('Unable to obtain asking price.  Returning $0')
                return 0

        except ValueError as err:
            logging.warning('Unable to clean asking price.  Returning $0')
            return 0






# Test Get School Rankings on Single Url
'''
url = r'/homedetails/10905-Shallowford-Rd-Roswell-GA-30075/14662538_zpid/'
get_school_ranking(url)
'''
