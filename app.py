#########################
######## IMPORTS ########
#########################

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import pymysql
from faker import Faker
import random
import script

faker = Faker()
app = Flask(__name__)

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

command1 = """
select * from property limit 20;
"""
cursor.execute(command1)
# print( cursor.fetchall())
connection.commit()
# ************ ************ ************
# Main Page
# ************ ************ ************
@app.route('/', methods=['GET','POST'])
def index(): 
    return render_template('index.html')

# ************ ************ ************
# create new user
# ************ ************ ************
@app.route('/createuser', methods=['GET','POST'])
def createuser(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        gender = userDetails['gender']
        age = userDetails['age']
        dob = str(userDetails['dob'])
        focus = userDetails['focus']
        script.register_user(name, email,gender,age,dob,focus)
        
    return render_template('createuser.html')
# ************ ************ ************
# Create new user
# ************ ************ ************

@app.route('/viewusers')
def viewusers():
    cursor.execute("SELECT * FROM user")
    viewusers = cursor.fetchall()
    return render_template('viewusers.html', newuser=viewusers)

@app.route('/users')
def users():
    resultValue = cursor.execute("SELECT * from user")
    if resultValue > 0:
        userDetails = cursor.fetchall()
        return render_template('users.html',userDetails=userDetails)


if __name__ == '__main__':
    app.run(debug=True)