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
logging.basicConfig(level=logging.CRITICAL)

# IMPORT MODULES----------------------------------------------------------------------

url = r'https://www.zillow.com/Denver,-CO_rb/'



def get_home_fact_list(url):
    Content = urllib.request.Request(url, headers={
        'authority': 'www.zillow.com',
        'method': 'GET',
        'path': '/homes/',
        'scheme': 'https',
        'user-agent': ''''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)
         AppleWebKit/537.36 (KHTML, like Gecko)
        Chrome/61.0.3163.100 Safari/537.36'''})

    html = urlopen(Content)
    bsObj = BeautifulSoup(html.read(), 'lxml')
    print(bsObj.prettify())


get_home_fact_list(url)


