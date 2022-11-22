import app
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pymysql
from faker import Faker
faker = Faker()
import random


# Configure Database
host = "db4free.net"
user = "user00001"
password = "11111111"
db = "propertyfinder55"

connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    db = db,
)

cursor = connection.cursor()

def register_user(name, email,gender,age,dob,focus):

  register_user_cmd = "INSERT INTO user VALUES ('"+name+"','"+email+"','"+gender+"',"+str(age)+",'"+dob+"','"+focus+"')"
  print(register_user_cmd)

  try:
    
    cursor.execute(register_user_cmd)
    # connection.commit()
    print("success")
  except Exception as e:
    print(e)
    print("Could not add user. Please try again later.")

  try:
    cursor.execute("select * from user where username = '"+name+"';")
    print(cursor.fetchall())
  except Exception as e:
    print(e)
