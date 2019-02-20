import requests
import time
import csv
import json
from insert_to_db import insert
import private
#from pprint import pprint


URL = private.weather_url
APIKEY = private.raph_weather_api
weather_time = {
"value": 1
}

LANGUAGE = "en-us"
DETAILS = "false"

r = requests.get(URL, params={"apikey": APIKEY, "language": LANGUAGE,"details": DETAILS})

weather = json.loads(r.text)

def get_weather():
    r = requests.get(URL, params={"apikey": APIKEY, "language": LANGUAGE,"details": DETAILS})
    weather = json.loads(r.text)
    return weather

def build_weather_csv(json, time):
    print("time is ", time)
    f = csv.writer(open("weather.csv", "w"))
    f.writerow(["WeatherText", "Temperature - Celcius"])
    for x in json:
        f.writerow([ 
            time['value'],
            json[0]["WeatherText"], 
            json[0]["Temperature"]['Metric']['Value']
            ])


def weather_scrape():
    for i in range(3):
        weather_data = get_weather()
        build_weather_csv(weather_data, weather_time)
        insert("weatherdata")
        print("weather time is ", weather_time)
        weather_time['value'] += 1
        print("done!")

weather_scrape()
