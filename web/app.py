from flask import Flask, render_template, jsonify, Response, request
import json
import sys
import os
import pymysql
from helpers.sql_query import sequeler 
from datetime import datetime
import requests
import csv
import pandas as pd
from sklearn.externals import joblib
from time import sleep
from pandas.io.json import json_normalize


KIERAN_RDS_HOST = os.environ['KIERAN_RDS_HOST']
KIERAN_RDS_USER = os.environ['KIERAN_RDS_USER']
KIERAN_RDS_PW = os.environ['KIERAN_RDS_PW']

RAPH_WEATHER_KEY = os.environ['RAPH_WEATHER_API']

app = Flask(__name__)


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


today_index = datetime.now().weekday()


  
day_dict = {
    "0": "Monday", 
    "1": "Tuesday",
    "2": "Wednesday",
    "3": "Thursday",
    "4": "Friday",
    "5": "Saturday",
    "6": "Sunday"
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



# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/stations/<int:number>")
def one_station(number):
    for i in range(len(stations)):
        if stations[i]['number'] == number:
            return jsonify(stations[i])  
    return "Sorry, no station data"
            

# @app.route("/name")
# def name():
#     return render_template('raph_home.html', stations=stations)


    
# @app.route("/index")
# def indexer():
#     return render_template('index.html', stations=stations, dynamic=dynamicdata)

@app.route('/api/static/')
def coordinates():
    return jsonify(stations)





@app.route('/mock/predict', methods=['POST', 'GET'])
def predict():
    
    connection = pymysql.connect(host=KIERAN_RDS_HOST,
                             user=KIERAN_RDS_USER,
                             password=KIERAN_RDS_PW,
                             db='comp30830', cursorclass=pymysql.cursors.DictCursor)


    with connection.cursor() as cursor:
        query = "select data from weather_forecast"
        cursor.execute(query)
        query_data = cursor.fetchall()
    connection.close()
    
    weather_string = query_data[0]


    # print(type(weather_string))

    data = request.get_json(force = True)
    day = int(data["weekday"])
    time = int(data["hour"])
    station = data["station_id"]
    
    

  
    difference = int(day) - today_index

    data["weekday"] = day_dict[data["weekday"]]
    isDay = "True"

    if time < 6 or time > 21:
        isDay = 0
    else:
        isDay = 1

    if difference < 0:
            difference = difference + 7
    counter = 0

    data_dict = json.loads(weather_string["data"])

    # print(data_dict)

    print("YOU WANT ", difference, " DAYS FROM NOW")
        
    for x in data_dict['DailyForecasts']:
        
        if counter == difference:
            print(type(x["Day"]["RainProbability"]))
            data["weather_text"] = x["Day"]["IconPhrase"],
            data["hasprecip"] = x["Day"]["RainProbability"],
            data["isday"] = isDay,
            data["tempc"] = x["Temperature"]["Maximum"]["Value"],   #
            data["rftempc"] = x["RealFeelTemperature"]["Maximum"]["Value"],
            data["windspeedv"] = x["Day"]["Wind"]["Speed"]["Value"]
        counter += 1

    my_new_dict = {
        "station_id": data["station_id"],
        "weekday": data["weekday"],
        "weather_text": data["weather_text"],
        "hasprecip": data["hasprecip"],
        "isday": data["isday"],
        "tempc": data["tempc"],
        "rftempc": data["rftempc"],
        "windspeedv": data["windspeedv"],
        "hour": data["hour"]
    }

    print(my_new_dict)

    if my_new_dict["isday"][0] > 0:
        my_new_dict["isday"] = True
    else:
         my_new_dict["isday"] = False

    if my_new_dict["hasprecip"][0] > 0:
        my_new_dict["hasprecip"] = True
    else:
         my_new_dict["hasprecip"] = False
    
    
    # print(my_new_dict)

    start_hour = int(my_new_dict["hour"]) - 3
    end_hour = int(my_new_dict["hour"]) + 4

    predictions = []

    for i in range(start_hour, end_hour):
        my_new_dict["hour"] = i
        new_dataframe = pd.DataFrame(my_new_dict)
        # print(new_dataframe)
        categorical_columns = new_dataframe[['station_id', 'weekday', 'weather_text', 'hour']].columns
        for column in categorical_columns:
            new_dataframe[column] = new_dataframe[column].astype('category')

        
        query = pd.get_dummies(new_dataframe)
        query = query.reindex(columns=model_columns, fill_value=0)
        prediction = list(lr.predict(query))
        predictions.append((i, prediction))
  
    predictions.append(my_new_dict)
    data_lists = []
    counter = 0
    for item in predictions:
        if type(item) is tuple:
            data_lists.append(list(item))
            counter += 1
            print(counter)
    return jsonify({'prediction': str(predictions), 'tuples': data_lists})
   
    # return "done"
@app.route('/')
def mock():
    return render_template('index.html', stations=stations, dynamic=dynamicdata, weather=weather)

@app.route('/api/dynamic/')
def dynamic():
    return jsonify(dynamicdata)

def donow(csv):
    user_df = pd.read_csv(csv, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)

app.config["TEMPLATES_AUTO_RELOAD"] = True



has_been_called = False
lr = joblib.load("model.pkl") # Load "model.pkl"
print('Model loaded')
model_columns = joblib.load("model_columns.pkl") # Load "model_columns.pkl"
print ('Model columns loaded')

# grab weather forecast from accuweather and put in database
print("I'm calling it!")
URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/207931"
LANGUAGE = "en-us"
DETAILS = "true"
METRIC = "true"


r = requests.get(URL, params={"apikey": RAPH_WEATHER_KEY, "language": LANGUAGE,"details": DETAILS,"metric":METRIC})

weather_json = json.loads(r.text)

my_str =json.dumps(weather_json)

print("type is ", type(my_str), "my_str is ", my_str)

cnx = pymysql.connect(host=KIERAN_RDS_HOST, user=KIERAN_RDS_USER, password=KIERAN_RDS_PW,
                            database='comp30830', local_infile=1) 
cursor = cnx.cursor()
script = """
drop table if exists weather_forecast; 
"""
cursor.execute(script)
script = """
CREATE TABLE weather_forecast (
    data TEXT
);
"""
cursor.execute(script)
script = " INSERT into weather_forecast VALUES (" + "'" + my_str + "'" + ");"
cursor.execute(script)

cursor.close()
cnx.commit()


if __name__ == '__main__':

    app.run(host='0.0.0.0') 

 
