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
import module1_sql_functions as m1
import module2_get_value_functions as m2
import module3_zillow_api as m3
import module4_url_filters as m4

url = r'https://www.zillow.com/homedetails/278-Spring-Dr-Roswell-GA-30075/14665555_zpid/'




