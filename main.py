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
from settings import *
logging.basicConfig(level=logging.INFO)

# IMPORT MODULES----------------------------------------------------------------------
import sql_functions as m1
import scraper_functions as m2
import zillow_api as m3
import url_filters as m4


# INSTANTIATE CONNECTION TO MYSQL DATABASE--------------------------------------------


mydb = mysql.connector.connect(
        host='localhost',
        user= user,
        passwd= password,
        database='upwork_test_db',
        auth_plugin='mysql_native_password')


# RUN SCRAPER FUNCTION -------------------------------------------------
logging.info('\n ************************ INITIALIZING SCRAPER *****************************\n')

def run_scraper(state=None, city=None, count=1):

    # If First Iteration - Gather Info
    if count==1:
        logging.info('\nInitializing test for scraper protections\n')

        # Step 1: Gather Information
        logging.info('Step 1: gather state & city information')
        state= input('For which state would you like to gather information (Ex: GA) ? ')
        city= input('For which city would you like to gather information (must include - between names, ex: Johns-Creek)? \n')

    # Statement
    PHRASE = "human to continue"

    # Duration
    rand_dur = random.randint(5,7)

    # Check for web scraper protections
    logging.info('Iteration {}, testing web page scraper protections'.format(count))
    bsObj, url = m2.get_bsObj_main_page(city, state, 1)
    bsObj_str = str(bsObj)

    # Run 10 Iterations of Test
    if count < 100:

        # Check if protections blocking scraper
        if PHRASE in bsObj_str or len(bsObj_str) < 1:
            logging.info('Web page protections are blocking the scraper')
            logging.info('Sleeping for {} seconds\n'.format(rand_dur))
            sleep(rand_dur)
            # Increase Count
            count += 1
            # Rerun scraper protection function
            run_scraper(state, city, count=count)

        # If the phrase is not found, fun main scraper function
        else:
            logging.info('Scraper protection test passed.  Initiate scraper')
            # Run Scraper for Selected City/State
            m2.main_get_home_data(city, state, bsObj, url)

    else:
        logging.warning('Unable to pass scraper protections. Try again later')
        return None




# Initialize
run_scraper(state=None, city=None, count=1)










