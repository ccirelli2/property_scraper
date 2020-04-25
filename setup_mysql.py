import mysql.connector
import logging
import os
from time import sleep
import sql_functions as f1
import subprocess
logging.basicConfig(level=logging.INFO)


# SETUP FUNCTIONS ----------------------------------------------

def gather_info(response=True):

    if response:
        print('''
            Initializing the setup script to create the MySQL database and tables
            required by this program\n''')

    # Time Delay
    sleep(1)

    # Question 1
    q1 = input('\tDo you have installed on this computer an instance of MySQL (Yes, no)? ')

    # If Yes
    if q1 in ('Yes', 'yes'):
        username = input('\tPlease enter your user name: ')
        password = input('\tPlease enter your password: ')
        return username, password

    # If No
    if q1 in ('No', 'no'):
        print('''
            This program requires a MySQL username and password have been created.
            Once created, please re-run this script.  Good Bye...''')

    # If incorred response
    else:
        print('''
            Response not recognized.
            Please try again by entering one of the following responses: Yes, yes, No, no\n''')
        gather_info(False)


def try2connect_mysql(username, password, connection=True):

    print('\tAttempting to connect to MySQL')

    try:
        mysql.connector.connect(
            host='localhost',
            user=username,
            passwd=password,
            auth_plugin='mysql_native_password')

        print('\tConnection established')
        return True

    except mysql.connector.errors.NotSupportedError as err:
        print('''
              Connection to MySQL database failed.
              Please try to enter your username and password again''')
        gather_info(False)
    except mysql.connector.errors.ProgrammingError as err:
        print('''
              Connection to MySQL database failed.
              Please try to enter your username and password again\n''')
        gather_info(False)



def create_db(username, password, database):
    logging.info('Creating MySQL database')

    # Instantiate Connection
    conn = mysql.connector.connect(
        host='localhost',
        user=username,
        passwd=password,
        auth_plugin='mysql_native_password')

    # Try Creating Database
    try:
        mycursor = conn.cursor()
        sql_command = ''' CREATE DATABASE {}'''.format('upwork_test_db')
        mycursor.execute(sql_command)
        conn.commit()
        logging.info('Database -{}- created successfully'.format(database))
    except mysql.connector.errors.ProgrammingError as err:
        logging.info('mysql.connector generated an error')
        logging.warning(err)
    except mysql.connector.errors.DatabaseError as err:
        logging.info('Database error')
        logging.warning(err)




def import_sql_schema(username, password):

    try:
        logging.info('Trying connection to datbase -> upwork_test_db')
        conn = mysql.connector.connect(
        host='localhost',
        user=username,
        passwd=password,
        database='upwork_test_db',
        auth_plugin='mysql_native_password')
        logging.info('Connection successfully established to db.  Procceding to import schema')

        # Use Subprocess to execute import of schema
        os.system('mysql -u root -p upwork_test_db < mysql_scraper_schema.sql')
        logging.info('Schema imported correctly')
        # Add a function to test if schema created correctly


    except mysql.connector.errors.DatabaseError as err:
        logging.info('Unable to connect to database => upwork_test_db')
        logging.info('Please check to see that database was created correctly')
        logging.warning(err)


# EXECUTE FUNCTIONS ---------------------------------------------

# Run Gather info function
username, password = gather_info()

# Try Connecting to MySQL
connection_status = try2connect_mysql(username, password)

# If Connection Established Successfully
if connection_status:
    # Create Database
    create_db(username, password, 'upwork_test_db')
    # Import Schema
    import_sql_schema(username, password)



