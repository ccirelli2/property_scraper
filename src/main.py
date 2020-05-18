#!/usr/bin/env python3
from time import sleep
import random
import logging

import pymysql

import scraper.settings as settings
import scraper.scraper_functions as helper_funcs

logging.basicConfig(level=logging.INFO)


mydb = pymysql.connect(
    host=settings.host,
    user=settings.user,
    passwd=settings.password,
    database=settings.database)


logging.info('\n ************************ INITIALIZING SCRAPER *****************************\n')


def scraper(state=None, city=None, count=1):
    # If First Iteration - Gather Info
    if count == 1:
        logging.info('\nInitializing test for scraper protections\n')
        logging.info('Step 1: gather state & city information')

        state = input('For which state would you like to gather information (Ex: GA) ? ')
        city = input('For which city would you like to gather information (must include - between names, ex: Johns-Creek)? \n')

    PHRASE = "human to continue"
    rand_dur = random.randint(5, 7)

    # Check for web scraper protections
    logging.info('Iteration %s, testing web page scraper protections', count)
    bsObj, url = helper_funcs.get_bsObj_main_page(city, state, 1)
    bsObj_str = str(bsObj)

    if count < 100:
        # Check if protections blocking scraper
        if PHRASE in bsObj_str or len(bsObj_str) < 1:
            logging.info('Web page protections are blocking the scraper')
            logging.info('Sleeping for %s seconds\n', rand_dur)
            sleep(rand_dur)

        # If the phrase is not found, fun main scraper function
        else:
            logging.info('Scraper protection test passed.  Initiate scraper')
            helper_funcs.main_get_home_data(city, state, bsObj, url)

    else:
        logging.warning('Unable to pass scraper protections. Try again later')

    return (state, city)


def run_scraper():
    count = 1
    state = None
    city = None
    while True:
        state, city = scraper(state, city, count)


if __name__ == '__main__':
    run_scraper()
