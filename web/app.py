from flask import Flask, render_template, jsonify, Response
import json
import sys
import os
import pymysql
from helpers.sql_query import sequeler 
from datetime import datetime




# KIERAN_RDS_HOST = os.environ['KIERAN_RDS_HOST']
# KIERAN_RDS_USER = os.environ['KIERAN_RDS_USER']
# KIERAN_RDS_PW = os.environ['KIERAN_RDS_PW']

app = Flask(__name__)

# connection = pymysql.connect(host=KIERAN_RDS_HOST,
#                              user=KIERAN_RDS_USER,
#                              password=KIERAN_RDS_PW,
#                              db='comp30830', cursorclass=pymysql.cursors.DictCursor)
# print(sys.path)



# with connection.cursor() as cursor:
#     # Read a single record
#     sql = "SELECT * FROM dynamicdata WHERE download_number = (SELECT MAX(download_number) FROM dynamicdata);"
#     cursor.execute(sql)
#     dynamic = cursor.fetchall()
#     connection.close()


data = sequeler.collectData(["SELECT * FROM staticdata", "SELECT * FROM dynamicdata WHERE download_number = (SELECT MAX(download_number) FROM dynamicdata)", "SELECT * FROM weatherdata WHERE id = (SELECT MAX(id) FROM weatherdata)"])
# dynamic = sequeler.collectData("SELECT * FROM dynamicdata WHERE download_number = (SELECT MAX(download_number) FROM dynamicdata);")
stations = data[0]
dynamic = data[1]
weather = data[2]



for i in range(len(stations)):
    current = stations[i]
    current["latitude"] = float(current["latitude"])
    current["longitude"] = float(current["longitude"])


for i in range(len(dynamic)):
    current = dynamic[i]
    timestamp = current["timestamp"] // 1000
    current["timestamp"] = timestamp

temperature = float(weather[0]['tempc'])
description = weather[0]['weather_text']
current_time = weather[0]['timestamp']

current_date = datetime.utcfromtimestamp(current_time).strftime("%A %d %B %Y")
current_time = datetime.utcfromtimestamp(current_time).strftime("%H:%M")


dynamicdata = []
for i in range(len(dynamic)):
    dynamicdata.append(dynamic[i])

# print(dynamicdata)

weather = {
    'temperature': temperature,
    'description': description
}



  

# RAPH: use this sql query to get the most recent dynamicdata

# SELECT 
#     *
# FROM
#     dynamicdata
# WHERE
#     download_number = (
#  SELECT 
#             MAX(download_number)
#         FROM
#             dynamicdata);



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/stations/<int:number>")
def one_station(number):
    for i in range(len(stations)):
        if stations[i]['number'] == number:
            return jsonify(stations[i])  
    return "Sorry, no station data"
            

@app.route("/name")
def name():
    return render_template('raph_home.html', stations=stations)

@app.route("/mapscrn")
def map():
    return render_template('mapscrn.html')

@app.route("/index/3")
def index3():
    return render_template('index3.html')

@app.route("/index")
def indexer():
    return render_template('index.html', stations=stations, dynamic=dynamicdata)

@app.route('/api/static/')
def coordinates():
    return jsonify(stations)

@app.route('/mock')
def mock():
    return render_template('mockup.html', stations=stations, dynamic=dynamicdata, weather=weather)

@app.route('/api/dynamic/')
def dynamic():
    return jsonify(dynamicdata)

app.config["TEMPLATES_AUTO_RELOAD"] = True
 
app.run(host='0.0.0.0', port=5000) 