import requests
import csv
import json
from pprint import pprint
import time
import os
import sys
import private

APIKEY = private.api
NAME = "Dublin"
STATIONS_URI = private.stationsURI
timePeriod = 1

while True:

    timePeriodStr = str(timePeriod)
    fileName = "stations" + timePeriodStr + ".csv"

    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})

    # obj = json.loads(r.text)[1]['number']
    x = json.loads(r.text)

    f = csv.writer(open(fileName, "w"))

    # Write CSV Header, If yu dont need that, remove this line
    # f.writerow(["number", "contract_name", "address", "latitude",
    #  "longitude","banking","bonus", "bike_stands", "available_bike_stands","available_bikes",
    #  "status","last_update"])

    for x in x:
        f.writerow([x["number"],
                    x["contract_name"],
                    x["address"],
                    x["position"]["lat"],
                    x["position"]["lng"],
                    x["banking"],
                    x["bonus"],
                    x["bike_stands"],
                    x["available_bike_stands"],
                    x["available_bikes"],
                    x["status"],
                    x["last_update"]])

    filecall = "python insertDB.py " + fileName
    filecallStr = str(filecall)

    os.system(filecallStr)

    time.sleep(10)
    timePeriod += 1