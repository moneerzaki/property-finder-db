#########################
######## IMPORTS ########
#########################

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import pymysql
from faker import Faker
import random
import database

faker = Faker()
app = Flask(__name__)

# Configure Database

connection = pymysql.connect(
    host = database.host,
    user = database.user,
    password = database.password,
    db = database.db,
)

print("Connected successfully\n")

cursor = connection.cursor()

cursor.execute("use propertyfinder55")

# ************ ************ ************
# Main Page
# ************ ************ ************
@app.route('/', methods=['GET','POST'])
def index(): 
    return render_template('index.html')

# ************ ************ ************
# Page to create new user - /createuser
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
        register_user_cmd = "INSERT INTO user VALUES ('"+name+"','"+email+"','"+gender+"',"+str(age)+",'"+dob+"','"+focus+"')"
        print(register_user_cmd)
        cursor.execute(register_user_cmd)
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
    if request.method == 'GET':
        pass
        
    return render_template('createuser.html')
# ************ ************ ************
# Page to view all users - /viewusers
# ************ ************ ************

@app.route('/viewusers')
def viewusers():
    cursor.execute("SELECT * from property limit 100")
    users = cursor.fetchall()
    return render_template('viewusers.html',users=users)

# ************ ************ ************
# Page to add review on agent
# ************ ************ ************
alladdedreviews = []
@app.route('/addreview', methods =['GET','POST'])
def addreview():
    cursor.execute("select id from agent limit 20;")
    listofagents = cursor.fetchall()
    
    cursor.execute("select * from review limit 20;")
    allreviews = cursor.fetchall()

    if request.method == 'POST':
        reviewid = faker.ean()
        reviewtext = request.form.get("reviewtext")
        agentid = request.form.get("selectedagent").replace("(","").replace(")","").replace(",","").replace("'","")
        print("Agent ID ##########\n")
        print(agentid)
        date = request.form.get("date")
        rating = request.form.get("rating")
        username = request.form.get("username")
        
        cursor.execute("insert into review values('"+reviewid+"','"+username+"','"+agentid+"','"+date+"','"+reviewtext+"',"+rating+");") 

        print("query successfully executed")
        
        addedreview = [reviewid,reviewtext,agentid,date,username]
        alladdedreviews.append(addedreview)
        
        return render_template('addreview.html',listofagents=listofagents,addedreview=addedreview,alladdedreviews=alladdedreviews,allreviews=allreviews)
    
    if request.method == 'GET':
        return render_template('addreview.html',listofagents=listofagents,allreviews=allreviews)

    
# ************ ************ ************
# View Reviews of an Agent
# ************ ************ ************

@app.route('/viewreviewsbyagent',methods=['GET','POST'])
def viewreviewsbyagent():
    if request.method == 'POST':
        selectedagent =  request.form.get("selectedagent")
        cursor.execute("select * from review where agent_id ='"+selectedagent+"';")
        # CHANGE THIS
        # cursor.commit()
        listofreviews = cursor.fetchall()
        return render_template('viewreviewsbyagent.html', listofreviews = listofreviews,selectedagent=selectedagent)
    if request.method =='GET':
        cursor.execute("select id from agent limit 20")
        listofagents = cursor.fetchall()
        return render_template('viewreviewsbyagent.html',listofagents=listofagents)



# ************ ************ ************
# View Aggregated Rating of Broker Company
# ************ ************ ************

@app.route('/viewbrokerrating', methods=['GET', 'POST'])
def viewbrokerrating():
    cursor.execute("select b.name, b.id, count(a.id) from agent a inner join broker b on a.broker_id = b.id inner join review r on r.agent_id = a.id where b.name !='N/A' group by b.id order by count(a.id) desc;")

    allbrokers = cursor.fetchall()
    
    cursor.execute("select avg(r.rating), b.name, b.id, count(a.id), round(avg(p.price/p.area_sqm)) from agent a inner join broker b on a.broker_id = b.id inner join review r on r.agent_id = a.id inner join property p on p.agent_id = a.id where b.name !='N/A' group by b.id order by count(a.id) desc limit 5;")
    
    top5brokers=cursor.fetchall()
    
    if request.method == 'GET':

        return render_template('viewbrokerrating.html',allbrokers=allbrokers,top5brokers=top5brokers)

    if request.method == 'POST':
        selectedbroker =  request.form.get("selectedbroker")
        cursor.execute("select avg(r.rating), b.name,count(a.id) from agent a inner join broker b on a.broker_id = b.id inner join review r on r.agent_id = a.id where b.id = '"+selectedbroker+"' group by b.name;")
        
        brokerdetails = cursor.fetchall()

        return render_template('viewbrokerrating.html',brokerdetails=brokerdetails,allbrokers=allbrokers,top5brokers=top5brokers)

# ************ ************ ************
# View Details of Development Project
# ************ ************ ************

@app.route('/viewproject', methods=['GET','POST'])
def viewproject():
    cursor.execute("select name,id from project limit 20;")
    allprojects = cursor.fetchall()
    if request.method == 'GET':

        return render_template('viewproject.html',allprojects=allprojects)

    if request.method == 'POST':
        selectedproject =  request.form.get("selectedproject")
        cursor.execute("select * from project where id ='"+selectedproject+"';")
        projectdetails = cursor.fetchall()

        cursor.execute("select count(*),p.type, round(avg(p.price/p.area_sqm)) from project pr inner join property p on p.project_id= pr.id where pr.id = '"+projectdetails[0][0]+"'group by p.type;")

        projectdetails2 = cursor.fetchall()

        return render_template('viewproject.html',projectdetails=projectdetails,allprojects=allprojects,projectdetails2 = projectdetails2)
    


# ************ ************ ************
# View Listings and Prices in a Location
# ************ ************ ************

@app.route('/viewlocation',methods=['GET','POST'])
def viewlocation():
    cursor.execute("select distinct  location, count(id) from property where location != 'N/A' group by location order by count(id) desc;")
    alllocations = cursor.fetchall()


    listofamenities = [
    'Unfurnished',
    'Security',        
    'Lobby in Building',
    'Balcony',
    'Shared Gym',
    'Shared Pool',
    'Kitchen Appliances',
    'Central A/C',
    'Private Jacuzzi',
    'Private Garden',
    "s Pool",
    'Concierge',
    'Maid Service',
    'Built in Wardrobes',
    'Private Gym',
    'Maids Room',
    'Walk-in Closet',
    'Covered Parking',
    'Pets Allowed',
    "Play Area",
    'Shared Spa',
    'Barbecue Area',
    'View of Water',
    'View of Landmark',
    'Partly furnished']

    print(len(listofamenities))


    if request.method == 'GET':

        return render_template('viewlocation.html',alllocations=alllocations,listofamenities=listofamenities)

    if request.method == 'POST':
        selectedlocation =  request.form.get("selectedlocation")

        cursor.execute("select * from property where location ='"+selectedlocation+"' and price != 0;")
        
        listofproperties = cursor.fetchall()

        cursor.execute("select type, round(avg(p.price/p.area_sqm)),count(p.id) from property p where location ='"+selectedlocation+"' and price != 0 group by type;")

        avgprices = cursor.fetchall()

        minprice =  request.form.get("minprice")
        maxprice = request.form.get("maxprice")

        amenities1=request.form.get('amenities1')
        amenities2=request.form.get('amenities2')
        amenities3=request.form.get('amenities3')
        amenities4=request.form.get('amenities4')
        amenities5=request.form.get('amenities5')
        amenities6=request.form.get('amenities6')
        amenities7=request.form.get('amenities7')
        amenities8=request.form.get('amenities8')
        amenities9=request.form.get('amenities9')
        amenities10=request.form.get('amenities10')
        amenities11=request.form.get('amenities11')
        amenities12=request.form.get('amenities12')
        amenities13=request.form.get('amenities13')
        amenities14=request.form.get('amenities14')
        amenities15=request.form.get('amenities15')
        amenities16=request.form.get('amenities16')
        amenities17=request.form.get('amenities17')
        amenities18=request.form.get('amenities18')
        amenities19=request.form.get('amenities19')
        amenities20=request.form.get('amenities20')
        amenities21=request.form.get('amenities21')
        amenities22=request.form.get('amenities22')
        amenities23=request.form.get('amenities23')
        amenities24=request.form.get('amenities24')


        selectedamenities = []
        selectedamenities.append(amenities1)
        selectedamenities.append(amenities2)
        selectedamenities.append(amenities3)
        selectedamenities.append(amenities4)
        selectedamenities.append(amenities5)
        selectedamenities.append(amenities6)
        selectedamenities.append(amenities7)
        selectedamenities.append(amenities8)
        selectedamenities.append(amenities9)
        selectedamenities.append(amenities10)
        selectedamenities.append(amenities11)
        selectedamenities.append(amenities12)
        selectedamenities.append(amenities13)
        selectedamenities.append(amenities14)
        selectedamenities.append(amenities15)
        selectedamenities.append(amenities16)
        selectedamenities.append(amenities17)
        selectedamenities.append(amenities18)
        selectedamenities.append(amenities19)
        selectedamenities.append(amenities20)
        selectedamenities.append(amenities21)
        selectedamenities.append(amenities22)
        selectedamenities.append(amenities23)
        selectedamenities.append(amenities24)
        for i in selectedamenities:
            print(i)
    
        
        cursor.execute("select type, price, id, amenities from property where price > "+ minprice + " and price < "+maxprice+ " and location = '"+selectedlocation+"' and amenities like '%"
        +amenities1+"%' and amenities like '%"+amenities2+"%' and amenities like '%"
        +amenities3+"%' and amenities like '%"+amenities4+"%' and amenities like '%"+amenities5+"%' and amenities like '%"+amenities6+"%' and amenities like '%"+amenities7+"%' and amenities like '%"+amenities8+"%' and amenities like '%"+amenities9+"%' and amenities like '%"+amenities10+"%' and amenities like '%"+amenities11+"%' and amenities like '%"+amenities12+"%' and amenities like '%"+amenities13+"%' and amenities like '%"+amenities14+"%' and amenities like '%"+amenities15+"%' and amenities like '%"+amenities16+"%' and amenities like '%"+amenities17+"%' and amenities like '%"+amenities18+"%' and amenities like '%"+amenities19+"%' and amenities like '%"+amenities20+"%' and amenities like '%"+amenities21+"%' and amenities like '%"+amenities22+"%' and amenities like '%"+amenities23+"%' and amenities like '%"+amenities24+"%';")

        listofproperties2 = cursor.fetchall()

        print(amenities1)
    

        return render_template('viewlocation.html',selectedlocation=selectedlocation,listofproperties=listofproperties,alllocations=alllocations,avgprices=avgprices, listofproperties2=listofproperties2,minprice=minprice,maxprice=maxprice,listofamenities=listofamenities,amenities1=amenities1,selectedamenities=selectedamenities)
    

# ************ ************ ************
# View Properties Listed by an Agent
# ************ ************ ************

@app.route('/viewagent',methods=['GET','POST'])
def viewagent():
    cursor.execute("select id,name from agent where name != 'N/A';")
    
    listofagents = cursor.fetchall()
    
    if request.method == 'GET':
        return render_template('viewagent.html',listofagents=listofagents)
    
    
    if request.method == 'POST':
        selectedagent =  request.form.get("selectedagent").replace(')',"").replace("(","").replace("'","").replace(",","")

        cursor.execute("select p.id, p.type, p.price, a.name from property p inner join agent a on p.agent_id = a.id where a.id = '"+selectedagent+"';")

        listofproperties = cursor.fetchall()
        
        return render_template('viewagent.html', listofagents = listofagents,selectedagent=selectedagent,listofproperties=listofproperties)


# ************ ************ ************
# RUN APP
# ************ ************ ************
if __name__ == '__main__':
    app.run(debug=True)