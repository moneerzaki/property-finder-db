#########################
######## IMPORTS ########
#########################

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index(): 
    if request.method = 'POST':
        # RETREIVE data submitted in form
        userdata = request.form
        name = userDetails['name']
        email = userDetails['email']
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)