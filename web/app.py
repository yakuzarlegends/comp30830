from flask import Flask, render_template, jsonify
import pymysql
import json
import sys
import os


KIERAN_RDS_HOST = os.environ['KIERAN_RDS_HOST']
KIERAN_RDS_USER = os.environ['KIERAN_RDS_USER']
KIERAN_RDS_PW = os.environ['KIERAN_RDS_PW']

app = Flask(__name__)


connection = pymysql.connect(host=KIERAN_RDS_HOST,
                             user=KIERAN_RDS_USER,
                             password=KIERAN_RDS_PW,
                             db='comp30830', cursorclass=pymysql.cursors.DictCursor)
print(sys.path)

with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM staticdata"
        cursor.execute(sql)
        stations = cursor.fetchall()
        connection.close()


for i in range(len(stations)):
    current = stations[i]
    current["latitude"] = float(current["latitude"])
    current["longitude"] = float(current["longitude"])
    

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/name")
def other():
    return render_template('home.html', stations=stations)

@app.route('/api/static')
def coordinates():
    return jsonify(stations)
 
 