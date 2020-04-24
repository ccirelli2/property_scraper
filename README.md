# Description -----------------------------------------------------
This program is for an upwork contract to create web scraper to obtain 
real estate listing in Colorado.  Below are the milestones of the 
project. 

- Due Aril 24th		Submission of Code & Data 
- Due April 27th	Setup mysql database
- Due April 30th	Walk client through code


# Setup & Dependencies --------------------------------------------
- OS		Ubuntu 19	

- Python	This program was written using Python 3.7.
		See requirements file for installation of required
		python modules.  Python 3.7 and all modules must be
		installed before running any of the scripts associated
		with this program.


- Database:	This program requires a local instance of MySQL to
		be installed and a username and password to already
		have been created. 
		 
		Please run the mysql_scraper_schema.sql file in order to create
		the required database and tables.  


- APIs		This program utilizes the zillow api.  For this program
		to run properly a user id and credentials for this api
		are required. 



# Scraper output fields -------------------------------------------
- HOA Fees
- Rent Estimate
- Annual Taxes


# Disclosures & Legal Responsibility ------------------------------ 
1.)	The user of this program acknowledges and agrees that they alone
	take full responsibility and assume all legal liability for the use
	of this program and agree to fully indemnify the programmer of all
	defense costs and liability for their use of this program. 
2.) The user agrees to hold harmless and seek no legal recourse for any 
    destruction to personal property or information that the use of this 
	program may cause to the user. 
3.) The programmer provides no gaurantees that this program will continue
    to work after the initial installation and setup.

	


Debugging ---------------------------------------------------------

1.) README File:        Redo
2.) Repository:         Change all file names.
3.) MySQL:              Need to create unique script that the user can
                        run in order to automatically create database and tables.

4.) Logging:		Replace error and warning statements with logging. 
			Add User Input function to select logging level
			Set up sql table to capture logs

5.) Main Script:	Move main_get_home_data to another file
			What if the user puts in an invalide city + state combo?


6.) Module 2:		Replace print(err) with logging


7.) School Rankings:  	Need to replace with link to provider of information and
			scrape data from there. 

.) Zillow Data		- Is zillow percentile pulling correctly?


7.) MySQL Tables:	- Need to add primary key to each table. 
			- Probably should be URL and name of col should be diff
			  for each table. 
			- pull_date needs to be changed to a date object





