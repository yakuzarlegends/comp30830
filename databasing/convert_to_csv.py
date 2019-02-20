import requests
import csv
import json
import weather_scrape
from datetime import datetime
import private
import time
import calendar
from pprint import pprint
APIKEY = private.jcd_api
NAME ="Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
download_counter = 1
current_weather_time = 1

def populate_csv():
    print("hi there")

def populate_csv():

    if download_counter % 12 == 0:
        current_weather_time = weather_scrape()

    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY,"contract": NAME})
    x = json.loads(r.text)
    f = csv.writer(open("stations.csv", "w"))

    f.writerow(["number", "contract_name", "address", "latitude",
     "longitude","banking","bonus, bike_stands", "available_bike_stands","available_bikes",
     "status","last_update"])

    for x in x:
        f.writerow(
            [download_counter,
            x["number"],
            x["last_update"],
            current_weather_time,
            x["banking"],
            x["bonus"],
            x["bike_stands"],
            x["available_bike_stands"],
            x["available_bikes"],
            x["status"],
            get_day(),
            get_hour_and_min()
            ])


# def get_day():
#     right_now = datetime.utcnow()
#     dayName =(calendar.day_name[right_now.weekday()])
#     return dayName

# def get_hour_and_min():
#     right_now = datetime.utcnow()
#     dayHour = datetime.strftime(right_now,"%H%M")
#     return type(dayHour)






#today as a day eg Tuesday

# print(dayName)
# # current hour and minutes
# dayHour = datetime.strftime(right_now,"%H%M")
# print(dayHour)
# # current minutes utc universal time
# dayMinute = datetime.strftime(right_now, "%M")
# print(dayMinute)