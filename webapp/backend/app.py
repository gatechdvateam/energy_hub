#This is the main app module. You should define all your views here.
#Please add all code that loads data 

from flask import Flask, render_template, request, redirect, url_for

#import the function that loads your data here.
from loaddataset import LoadBasicVisualsData

#Create the app
app = Flask(__name__)


#Home page
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
   return render_template('index.html')

#Sample visuals page
@app.route('/basicvisuals')
def basicvisuals():
    """Renders this page."""
    return render_template(
        'basicvisuals.html',
        title='Home Page',
        #pass the data to the template page
        ChartData = LoadBasicVisualsData(),
    )

#Runs the app on your machine!
if __name__ == '__main__':
   app.run(debug=True)