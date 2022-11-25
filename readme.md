# Property Finder Query Tool

## Overview

The purpose of this project was to carry out web scraping on a real estate website, populate a SQL database with data points of properties, real estate agents, broker companies, development projects, and other entities, and then host this database remotely and create a GUI tool to query the database.

The first step was creating database schema to fit all the data points needed, taking into account all relevant entities (property, real estate agent, broker company, development project, user, review) and implementing unique primary keys to identify entities as well as foreign keys to link entities (e.g. every property is listed by a real estate agent).

The BeautifulSoup library in Python was used to do the initial web scraping, obtaining all the needed values from 7000+ pages and then using pandas to enter them into a dataframe and export as CSV.

The CSV files were then imported into a local MySQL database using MySQL workbench in order to generate dump files. Using d4free.net, these dump files were used to recreate the database on a remote server.

The final phase involved building a GUI application using Flask and pymysql in order to query the remote database and display the results in HTML format.

The GUI app has several functionalities, including:
* Register a new user to the database
* Create a new review on an existing agent
* View all reviews of a given agent
* View the average rating of all the agents working for a broker company
* Show the location, average price per square meter and number of listings per unit type (e.g. Apartment, Villa) for any given development project
* Display the top 5 broker companies by total number of listings and show their average price per square meter, number of agents and average number of listings per agent
* Display all of the properties listed by a given agent
* Show all of the properties in a given location, along with the average price per square meter for each unit type
* Show all of the properties in a certain locatin in a given price range and with a given set of amenities


## Instructions

To start the flask app, navigate to the main directory and run
```sh
python3 app.py
```

## Database

The 

Dump files are provided: 
#### ``create_database.sql``
#### ``propertyfinder55_dump_final``