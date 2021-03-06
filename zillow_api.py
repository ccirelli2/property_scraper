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
import pymysql
import pyzillow
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails
from settings import *


# Import Project Modules
import sql_functions as m1

# Instantiate Connect to MySQL --------------------------
mydb = pymysql.connect(
        host='localhost',
        user= user,
        passwd= password,
        database='upwork_test_db')
'''
m1.sql_insert_warning_logs(mydb, 'module_1', 'get_list_homes', url,
                          'Error possible due to website scraper protections', str(err))
'''



def get_house_data_zillow_api(address, zipcode, pull_date, asking_price, url):
    try:
        # Instantiate connection to zillow database
        web_service_id  = ''
        documentation   = ''
        d2              = ''
        zillow_data = ZillowWrapper(web_service_id)

        # Start Search
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        result = GetDeepSearchResults(deep_search_response)

        # Create Object for the old & new stdout
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        # Generate stdout - should redirect to StringIO
        print('Key, Value')
        print('zillow_id,{}'.format(result.zillow_id))
        print('home_type,{}'.format(result.home_type))
        print('tax_year,{}'.format(result.tax_year))
        print('tax_value,{}'.format(result.tax_value))
        print('year_built,{}'.format(result.year_built))
        print('last_sold_date,{}'.format(result.last_sold_date))
        print('last_sold_price,{}'.format(result.last_sold_price))
        print('home_size,{}'.format(result.home_size))
        print('property_size,{}'.format(result.property_size))
        print('num_bedrooms,{}'.format(result.bedrooms))
        print('num_bathrooms,{}'.format(result.bathrooms))
        print('zillow_low_est,{}'.format(result.zestimate_valuationRange_low))
        print('zillow_high_est,{}'.format(result.zestimate_valuation_range_high))
        print('zillow_value_change,{}'.format(result.zestimate_value_change))
        print('zillow_percentile,{}'.format(result.zestimate_percentile))

        # Convert stdout from StringIO to String
        new_stdout_str = new_stdout.getvalue()
        test_stdout_str = open('zillow_api_data.csv', 'w')
        test_stdout_str.write(new_stdout_str)
        test_stdout_str.close()

        # Return to old stdout
        sys.stdout = old_stdout

        # Read CSV back in as a pandas dataframe
        df = pd.read_csv('zillow_api_data.csv')
        df.set_index('Key', inplace=True)

        # Need to convert values from strings to correct input value for db
        val_zillow_api = []

        val_zillow_api.append(address)
        val_zillow_api.append(pull_date)
        val_zillow_api.append(df.iloc[0,0])                 # zillow_id
        val_zillow_api.append(df.iloc[1,0])                 # home type
        val_zillow_api.append(df.iloc[2,0])                 # tax year
        val_zillow_api.append(df.iloc[3,0])                 # tax value
        val_zillow_api.append(df.iloc[4,0])                 # year built
        val_zillow_api.append(datetime.strptime('01/01/1900', '%m/%d/%Y')) # last sold date
        val_zillow_api.append(df.iloc[6,0])                 # last sold price
        val_zillow_api.append(df.iloc[7,0])                 # home size

        # Test if property value == none.  Appaned 0 if None.
        if df.iloc[8,0] == None or df.iloc[8,0] == 'None':
            val_zillow_api.append(0)                    # property size
        else:
            val_zillow_api.append(df.iloc[8,0])

        # Continue with other values
        val_zillow_api.append(df.iloc[9,0])                 # number bed rooms
        val_zillow_api.append(df.iloc[10,0])                # num bathrooms
        val_zillow_api.append(df.iloc[11,0])                # zillow_low_est
        val_zillow_api.append(df.iloc[12,0])                # zillow high est
        val_zillow_api.append(df.iloc[13,0])                # value change
        val_zillow_api.append(df.iloc[14,0])                # zillow percentile
        val_zillow_api.append(asking_price)					# value is an input to this function

        # Return List Object to be passed to sql insert function
        #print('Zillow API data successfully obtained\n')
        return val_zillow_api

    except IndexError as err:
        print('pyzillow generated an error => {}'.format(err))
        m1.sql_insert_warning_logs(mydb, 'module_3', 'get_house_data_zillow_api', url,
                                    'Error generated when accessing api', str(err))
    except pyzillow.pyzillowerrors.ZillowError:
        print('pyzillow generated an error')
        m1.sql_insert_warning_logs(mydb, 'module_3', 'get_house_data_zillow_api', url,
                                    'Error generated when accessing api', str(err))
    except ZillowError as err:
        print('Zillow generated an error => {}'.format(err))
        m1.sql_insert_warning_logs(mydb, 'module_3', 'get_house_data_zillow_api', url,
                                    'Error generated when accessing', str(err))









