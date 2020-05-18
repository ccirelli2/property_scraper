#!/usr/bin/env python3
from time import sleep
import random
import logging

import pymysql

import scraper.scraper_functions as helper_funcs


def _scraper(mydb, state, city, count=1):
    PHRASE = "human to continue"
    rand_dur = random.randint(5, 7)

    # Check for web scraper protections
    logging.info('Iteration %s, testing web page scraper protections', count)
    bsObj, url = helper_funcs.get_bsObj_main_page(city, state, True)
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
            helper_funcs.main_get_home_data(mydb, city, state, bsObj, url)

    else:
        logging.warning('Unable to pass scraper protections. Try again later')

    return (state, city)


def run_scraper(dbConfig, appConfig):
    mydb = pymysql.connect(
        host=dbConfig.get('host', None),
        user=dbConfig.get('user', None),
        passwd=dbConfig.get('password', None),
        database=dbConfig.get('database', None))

    count = 1
    state = appConfig.get('state', None)
    city = appConfig.get('city', None)
    while True:
        state, city = _scraper(mydb, state, city, count)
        count = count + 1
