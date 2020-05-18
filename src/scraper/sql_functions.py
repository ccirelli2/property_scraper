from datetime import datetime
import pandas as pd
import mysql.connector


# MYSQL - CLEAR TABLE FUNCTION-----------------------------------------
def clear_table(mydb, decision='No'):

    if decision in ('Yes', 'yes'):

        # Delete Addresses Data
        mycursor = mydb.cursor()
        sql_command = 'DELETE FROM ADDRESSES;'
        mycursor.execute(sql_command)
        mydb.commit()
        print("Data successfully cleared from 'Addresses' table")

        # Delete House Details Data
        mycursor = mydb.cursor()
        sql_command = 'DELETE FROM HOUSE_DETAILS;'
        mycursor.execute(sql_command)
        mydb.commit()
        print("Data successfully cleared from 'House Details' table")

        # Delete Schools Data
        mycursor = mydb.cursor()
        sql_command = 'DELETE FROM SCHOOLS;'
        mycursor.execute(sql_command)
        mydb.commit()
        print("Data successfully cleared from 'Schools' table\n")

    elif decision in ('No', 'no'):
        # Do Not Delete Table Data
        print('''Data will not be cleared from the Addresses,
                 House details and Schools tables\n''')


def sql_insert_warning_logs(mydb, module, funct, url, description, err):  # pylint: disable=too-many-arguments
    ''' Desc:  Insert warning logs into sql table
    '''
    pull_date = datetime.today().date()
    vals = [url, pull_date, module, funct, description, err]
    sql_command = '''
    INSERT IGNORE INTO LOGS (
    url_logs, pull_date, module, funct, description, err)
    VALUES(%s, %s, %s, %s, %s, %s)'''
    mycursor = mydb.cursor()
    mycursor.execute(sql_command, vals)
    mydb.commit()


def sql_insert_function_addresses(mydb, val):
    try:
        mycursor = mydb.cursor()
        sql_command = '''
            INSERT IGNORE INTO ADDRESSES (
            street_address, state, zipcode, city, pull_date, url)
            VALUES(%s, %s, %s, %s, %s, %s)'''

        mycursor.execute(sql_command, val)
        mydb.commit()

    except mysql.connector.errors.ProgrammingError as err:
        print('sql insert addresses function generated an error => {}'.format(err))

    except mysql.connector.errors.IntegrityError as err:
        print('sql insert addresses function generated an error => {}'.format(err))


# SCHOOL RANKING INSERT FUNCTION -----------------------------------------
def sql_insert_function_schools(mydb, val, street_address, pull_date, url):

    if val is not None:
        if len(val) < 3:
            print('Less than three school rankings scraped. Returning 0,0,0')
            return [0, 0, 0]

        # If its not, lets proceed with the insertion.
        try:
            mycursor = mydb.cursor()
            sql_command = '''
            INSERT IGNORE INTO SCHOOLS (

                street_address, pull_date,
                elementary_school_rating, middle_school_rating,
                high_school_rating, url)

                VALUES(%s, %s, %s, %s, %s, %s)'''
            val_insert = [street_address, pull_date, val[0], val[1], val[2], url]
            mycursor.execute(sql_command, val_insert)
            mydb.commit()

        except mysql.connector.errors.ProgrammingError as err:
            print('sql insert schools function generated an error => {}'.format(err))
            print('sql insert schools function generated an error => {}'.format(err))

    return []


# ZILLOW API INSERT FUNCTION --------------------------------------------------
def replace_none_values(val):
    # ** Note that we need to figure out a way to not have this apply to the dates
    # Define new list object
    new_val = []
    if val is not None:
        for value in val:
            if value is None or value == 'None':
                new_val.append(0)
            else:
                new_val.append(value)

    return new_val


def sql_insert_function_zillow_api_data(mydb, val):
    mycursor = mydb.cursor()
    sql_command = '''
    INSERT IGNORE INTO HOUSE_DETAILS (
        street_address, pull_date, zillow_id, home_type,
        tax_year, tax_value, year_built, last_sold_date, last_sold_price,
        home_size, property_size, num_bedrooms, num_bathrooms,
        zillow_low_est, zillow_high_est, value_change, zillow_percentile, asking_price)

    VALUES( %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s)
    '''
    try:
        mycursor.execute(sql_command, replace_none_values(val))
        mydb.commit()
    except mysql.connector.errors.ProgrammingError as err:
        print('Zillow insert function geneted an error => {}'.format(err))

    except mysql.connector.errors.IntegrityError as err:
        print('sql insert zillow function generated an error => {}'.format(err))


# GET GEORGIA MUNICIPAL DATA

def get_ga_muni_data(mydb):
    sql_command = '''SELECT
        NAME, TYPE, COUNTY
        FROM GA_MUNICIPALITIES
        WHERE TYPE = 'Town';'''

    df = pd.read_sql(sql_command, mydb)
    return df
