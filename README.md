## Description -----------------------------------------------------
This program is for an upwork contract to create web scraper to obtain 
real estate listing in Colorado.  Below are the milestones of the 
project. 

- Due Aril 24th		Submission of Code & Data 
- Due April 27th	Setup mysql database
- Due April 30th	Walk client through code


## Setup & Dependencies --------------------------------------------
- OS		Ubuntu 19	

- Python	This program was written using Python 3.7.

		See requirements.txt file for installation of required
		python modules.  Use pip3 install -r requirements.txt.


- Database:	This program requires a local instance of MySQL to
		be installed and a username and password to already
		have been created. 
		 
		Please run the mysql_scraper_schema.sql file in order to create
		the required database and tables.  

		Please update the settings.py file with your user name and 
		password. 

- APIs		This program utilizes the zillow api.  For this program
		to run properly a user id and credentials for this api
		are required. 

		Within the zillow_api file, please amend the following line items
		with your credentials and save. 
		web_service_id  = ''
        	documentation   = ''
        	d2              = ''



## Disclosures & Legal Responsibility ------------------------------ 
1.)	The user of this program acknowledges and expressely agrees that 
	they alone take full responsibility and assume all legal liability 
	for the use this program and agree to fully indemnify the programmer of all
	defense costs and liability for their use of this program. 

2.) 	The user agrees to hold harmless and seek no legal recourse for any 
    	destruction to personal property or information that the use of this 
	program may cause to the user. 

3.) 	The programmer provides no gaurantees that this program will continue
    	to work after the initial installation and setup.

## How to
```
usage: main.cli run [-h] [-s STATE] [-c CITY_NAME] [-e HOST] [-u USER]
                    [-d DATABASE] [-p PASSWORD]
                    [STATE-ABBR] [CITY]

Run the srapper.

positional arguments:
  STATE-ABBR            State to search.
  CITY                  City with in State to search.

optional arguments:
  -h, --help            show this help message and exit
  -s STATE, --state STATE
                        A full state name.
                        Examples:
                        	Alabama
                        	Alaska
                        	Arizona
                        	Arkansas
                        	California
                        	Colorado
                        	Connecticut
                        	Delaware
                        	District Of Columbia
                        	Florida
                        	Georgia
                        	Hawaii
                        	Idaho
                        	Illinois
                        	Indiana
                        	Iowa
                        	Kansas
                        	Kentucky
                        	Louisiana
                        	Maine
                        	Maryland
                        	Massachusetts
                        	Michigan
                        	Minnesota
                        	Mississippi
                        	Missouri
                        	Montana
                        	Nebraska
                        	Nevada
                        	New Hampshire
                        	New Jersey
                        	New Mexico
                        	New York
                        	North Carolina
                        	North Dakota
                        	Ohio
                        	Oklahoma
                        	Oregon
                        	Pennsylvania
                        	Rhode Island
                        	South Carolina
                        	South Dakota
                        	Tennessee
                        	Texas
                        	Utah
                        	Vermont
                        	Virginia
                        	Washington
                        	West Virginia
                        	Wisconsin
                        	Wyoming
  -c CITY_NAME, --city-name CITY_NAME
                        Choose a city with-in the provided state.
  -e HOST, --host HOST  Database host.
  -u USER, --user USER  Database user.
  -d DATABASE, --database DATABASE
                        Database to use.
  -p PASSWORD, --password PASSWORD
                        Database password to use. If not provided it will default to pull SCRAPER_PASSWORD from environment.
                        export SCRAPER_PASSWORD=<your password>
```
