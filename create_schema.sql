create database if not exists propertyfinder55;


-- ORDER of IMPORT
-- user —> project —> broker —> agent —> property —> review

  create table if not exists user (
  
  username varchar(250) not null,
  email varchar(250) not null,
  gender varchar(3),
  age int not null,
  birthdate varchar(250),
  focus varchar(50) not null
  rating int not null

);


create table if not exists project (
 
  id varchar(250) not null primary key,
  name varchar(250) not null,
  location varchar(250),
  head_office varchar(250),
  total_units int,
  photo varchar(250),
  status varchar(50)
  
);

create table if not exists broker (
  id varchar(250) not null primary key,
  name varchar(250) not null,
  listings int,
  phone_no varchar(50) not null
);

  create table if not exists agent (
  id varchar(250) not null,
  name varchar(50) not null,
  phone varchar(50),
  email varchar(50),
  whatsapp varchar(50),
  broker_id varchar(250) not null,
  primary key(id),
  foreign key (broker_id) references broker(id)
  );


create table if not exists property (
  
id varchar(250) not null primary key,
type varchar(50),
price int,
area_sqft int,
area_sqm int,
bedrooms int,
bathrooms int,
listing_date varchar(50),
location varchar(250),
description_ varchar(250),
amenities varchar(250),
agent_id varchar(250) not null,
project_id varchar(250),
foreign key(project_id) references project(id),
foreign key (agent_id) references agent(id)

);



  create table if not exists review (
  
  id varchar(250) not null,
  username varchar(50) not null,
  agent_id varchar(250), 
  date varchar(50),
  primary key(id),
  foreign key(agent_id) references agent(id)

);
