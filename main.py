import mysql.connector
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib
from time import sleep
from datetime import datetime
import random
import pyzillow
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails
import logging

logging.basicConfig(level=logging.INFO)


# IMPORT MODULES----------------------------------------------------------------------
import module1_sql_functions as m1
import module2_get_value_functions as m2
import module3_zillow_api as m3
import module4_url_filters as m4


# INSTANTIATE CONNECTION TO MYSQL DATABASE--------------------------------------------
mydb = mysql.connector.connect(
                host='localhost',
                user='cc2',
                passwd='Gsu2020!',
                database='upwork_property_scraper',
                auth_plugin='mysql_native_password')


# SCRAPER FUNCTION -----------------------------------------------------------
def main_get_home_data(city, state):

    # Get Max Page Number
    max_page_num = m2.get_bsObj_main_page(city, state, 1, 'max_page_num')

    # Iterate Over Pages (max_page_num because its up to but not including)
    for page_num in range(1, max_page_num + 1):

        # User Info
        print('Scraping page {} of {} -----------------------------------------'\
				.format(page_num, max_page_num))

        # Generate Datetime Object
        pull_date = datetime.today().date()

        # Get Beautiful Soup Object of Page N that contain links to each home listing
        bsObj = m2.get_bsObj_main_page(city, state, page_num)

        # Get List of Houses (Photo-cards) for each page)
        list_homes = m2.get_list_homes(bsObj)

		# Count Homes Scraped Obj
        count_homes_scraped = 0

        # Loop over home tags and scrape data --------------------------------
        if list_homes:
            for home in list_homes:

                # Get Tag Containing Address & Zip Code
                clean_house_tags = m2.clean_house_tags_4_address_zipcode_scrape(home)

                # Function may return null obj. Pass if None.
                if not clean_house_tags:
                    logging.info('No house tags found')

                else:
                    # Get Url
                    url = m2.get_url(home)

                    # Get Home Details -------------------------------------------

                    # Get Asking Price
                    asking_price = m2.get_sale_asking_price(home, url)

                    # Num home object
                    total_homes_on_page = len(list_homes)

                    # Get Zipcode
                    zip_code = m2.get_zip_code(clean_house_tags)
                    # Get Address
                    address = m2.get_address(clean_house_tags)
                    # Insert Address Fields into Address Table
                    val_addresses = [address, state, zip_code, city, pull_date, url]
                    m1.sql_insert_function_addresses(mydb, val_addresses)

                    # Get & Insert Fields From Zillow API ------------------------------
                    val_zillow_api_data = m3.get_house_data_zillow_api(address, zip_code,
                                                                       pull_date, asking_price)
                    m1.sql_insert_function_zillow_api_data(mydb, val_zillow_api_data)

                    # Get & Insert School Ranking Info ---------------------------------
                    school_rankings = m2.get_school_ranking(url)
                    m1.sql_insert_function_schools(mydb, school_rankings, address,
                                                   pull_date, url)

                    # Increment Num homes
                    print('{} of {} home data scraped'.format(
                        count_homes_scraped, total_homes_on_page))
                    count_homes_scraped += 1


            # Generate Random Sleep Period
            logging.info('Data successfully scraped for page {}'.format(page_num))
            sleep_seconds = random.randint(5, 10)
            logging.info('Sleeping for {} seconds\n'.format(sleep_seconds))
            sleep(sleep_seconds)

        # No Homes Found
        else:
            logging.warning('No homes found in search.  Ending scraper program')

    return None


# USER INPUT---------------------------------------------------------------------


# Clear Existing Table Data:
#clear_tables_decision = input('''Do you want to delete the data from the following tables?
#	1. Addresses,
#	2. House Details,
#	3. Schools
#	Indicate Yes or No:  ''')
#m1.clear_table(mydb, clear_tables_decision)


# MAIN FUNCTION----------------------------------------------------------------

logging.info('\n ************************ INITIALIZING SCRAPER ******************************\n')

# Define Run-Type:
def run_scraper():
    # Choose Run-Type
    print('How do you wan to run the scraper, for an individual state and city or all cities in a given state?')
    run_type = input('Acceptable responses => indv or all: ')

    # Run For Single State + City
    if run_type == 'indv':
        # User Input Data:
        State = input('Enter State (ex: GA)    : ')
        City = input('Enter City (ex: Roswell): ')

        # Run Scraper for Selected City/State
        main_get_home_data(City, State)

    # Run For State + List of Cities
    elif run_type == 'all':
        # Obtain list of cities from MySQL Table
        df_cities = list(m1.get_ga_muni_data(mydb)['NAME'])
        # Iterate Cities
        for city in df_cities:
            # Scrape data
            main_get_home_data(city, 'GA')
            logging.info('Scraping data for city => {}'.format())
    else:
        logging.warning('Input value incorrect. Must be either "indv or all"')

run_scraper()

# NOTES_ ----------------------------------------------------------------------
'''Add filter for home types'''










