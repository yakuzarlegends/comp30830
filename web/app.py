from flask import Flask, render_template, jsonify
import pymysql
import json
from Private import private

SQL_USER = private.raph_rds_user
SQL_HOST = private.raph_rds_host
PASSWORD = private.raph_rds_pw

app = Flask(__name__)

connection = pymysql.connect(host=SQL_HOST,
                             user=SQL_USER,
                             password=PASSWORD,
                             db='comp30830', cursorclass=pymysql.cursors.DictCursor)


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
 
 