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
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

# IMPORT MODULES----------------------------------------------------------------------
import sql_functions as m1
import scraper_functions as m2
import zillow_api as m3
import url_filters as m4


# INSTANTIATE CONNECTION TO MYSQL DATABASE--------------------------------------------
mydb = mysql.connector.connect(
        host='localhost',
        user= input('Username => ',
        passwd= input('Password => ',
        database='upwork_test_db',
        auth_plugin='mysql_native_password')


# SCRAPER FUNCTION -----------------------------------------------------------
def main_get_home_data(city, state):

    # Get Beautiful Soup Object
    bsObj = m2.get_bsObj_main_page(city, state, 1)

    # Get Max Page Number
    max_page_num = m2.get_max_page_num(bsObj)

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
        if list_homes:                                              # if list not empty
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

                    # Insert Location
                    val_addresses = [address, state, zip_code, city, pull_date, url]
                    m1.sql_insert_function_addresses(mydb, val_addresses)

                    # Get Zillow Data-------------------- ------------------------------
                    val_zillow_api_data = m3.get_house_data_zillow_api(address, zip_code,
                                                                       pull_date, asking_price, url)
                    m1.sql_insert_function_zillow_api_data(mydb, val_zillow_api_data)

                    # Get School Ranking Data ------------------------------------------
                    school_rankings = m2.get_school_ranking(url)
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

    return None


# MAIN FUNCTION----------------------------------------------------------------

logging.info('\n ************************ INITIALIZING SCRAPER ******************************\n')


# Define Run-Type:
def run_scraper():
    # Step 1: Gather Information
    logging.info('Step 1: gather state & city information')
    state= input('For which state would you like to gather information (Ex: GA) ? ')
    city= input('For which city would you like to gather information (Ex: Roswell)? \n')

    # Step 2: Check Scraper Protections
    p_status = m2.test_scraper_protections(state, city, count=1, pprint=True)

    # If Scraper Protections Off
    if p_status:

        # Run Scraper for Selected City/State
        main_get_home_data(city, state)
    else:
        pass

run_scraper()










