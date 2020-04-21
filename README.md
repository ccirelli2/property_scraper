# Description -----------------------------------------------------
Upwork Contract:  Create web scraper to obtain real estate listing in Colorado. 

# Implementation --------------------------------------------------
Python

# Output Fields----------------------------------------------------
address, 
zip code, 
listing pricing, 
number of beds, 
number of baths, 
square footage, 
HOA fees, 
rent estimate, 
annual taxes.

# Storage ---------------------------------------------------------
Utilize MySQL

# Milestones ------------------------------------------------------

1.) Due Aril 24th
	Submission of Code & Data 
2.) Due April 27th
    Setup mysql database=
3.) Due April 30th
    Walk client through code

Debugging ---------------------------------------------

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

7.) MySQL Tables:	- Need to add primary key to each table. 
			- Probably should be URL and name of col should be diff
			  for each table. 
			- pull_date needs to be changed to a date object
