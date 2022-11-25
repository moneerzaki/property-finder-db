-- Online SQL Editor to Run SQL Online.
-- Use the editor to create new tables, insert data and all other SQL operations.

-- Tables: PROPERTY, AMENITIES, USER, BROKER_COMPANY, AGENT, DEVELOPMENT_PROJECT, VIEWS, REVIEWS
  
create database if not exists Property_finder;

use Property_finder;
SET GLOBAL local_infile=1;

create table if not exists PROPERTY (
  
Property_ID char(10) not null primary key,
Area float not null,
Location varchar(50) not null,
Development varchar(50) not null,
Type_ varchar(50) not null, 
Number_of_Bedrooms int not null,
Number_of_Bathrooms int not null,
List_of_Amenities varchar(255) not null,
Description_ varchar(255) not null,
Listing_Date date not null,
Payment_Method varchar(50) not null,
Sales_Option varchar(50) not null,
Agent_Phone_Number varchar(10) not null,
foreign key(Development_Project_ID) references DEVELOPMENT_PROJECT(PROJECT_ID)
);

create table if not exists USER_ (
  
  username varchar(50) not null primary key,
  Email_Address varchar(50) not null,
  Gender varchar(50) not null,
  Age int not null,
  Birthdate date not null,
  Area_Of_Focus varchar(50) not null

);

create table if not exists DEVELOPMENT_PROJECT (
 
  Project_ID varchar(10) not null primary key,
  Name varchar(50) not null,
  Location varchar(50) not null,
  Price_Per_Square_Feet int not null,
  Total_Units int not null,
  Quarter varchar(10) not null,
  Development_Year year not null,
  Status varchar(50) not null

);

create table if not exists AGENT (
  Phone_Number varchar(10) not null primary key,
  Email varchar(50) not null,
  Name varchar(50) not null,
  Broker_Company_Phone_Number varchar(10) not null,
  foreign key (Broker_Company_Phone_Number) references BROKER_COMPANY(Phone_Number)
  );


create table if not exists BROKER_COMPANY (
  Phone_Number varchar(10) not null primary key,
  Address varchar(50) not null,
  Broker_Name varchar(50) not null
 
  );
  
create table if not exists VIEWS (
  Property_ID varchar(50) not null,
  Username varchar(50),
  primary key(Property_ID, Username),
  foreign key(Property_ID) references PROPERTY(PROPERTY_ID) on update cascade on delete cascade,
  foreign key (Username) references USER_(Username) on update cascade on delete cascade

 );
   
create table if not exists REVIEW (
  Username varchar(50) not null,
  Agent_Phone_Number varchar(10) not null,
  Review_Date date not null,
  foreign key(Username) references USER_(Username) on delete cascade on update cascade,
  foreign key(Agent_Phone_Number) references AGENT(Phone_Number) on delete cascade on update cascade
  
);

LOAD DATA LOCAL INFILE '/Users/ibrahim/Desktop/database_project/drive tables/property_table.csv' INTO TABLE PROPERTY 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE '/Users/ibrahim/Desktop/database_project/drive tables/user_table.csv' INTO TABLE USER_ 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE '/Users/ibrahim/Desktop/database_project/drive tables/project_table.csv' INTO TABLE DEVELOPMENT_PROJECT
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA LOCAL INFILE '/Users/ibrahim/Desktop/database_project/drive tables/agent_table.csv' INTO TABLE AGENT
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';


LOAD DATA LOCAL INFILE '/Users/ibrahim/Desktop/database_project/drive tables/broker_table.csv' INTO TABLE BROKER_COMPANY
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';



LOAD DATA LOCAL INFILE '/Users/ibrahim/Desktop/database_project/drive tables/review_table.csv' INTO TABLE REVIEW 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

