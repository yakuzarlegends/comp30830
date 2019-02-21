import requests
import time
import csv
import json
import calendar
import private
import MySQLdb
from datetime import datetime

class Scraper:

    PASSWORD = private.pw
    WEATHER_APIKEY = private.yvette_weather_api
    BIKE_APIKEY = private.jcd_api
    LANGUAGE = "en-us"
    DETAILS = "false"
    URL = private.weather_url
    STATIONS_URL = private.jcd_url
    WEATHER_PATH = private.weather
    STATIONS_PATH = private.stations
    NAME = "dublin"
    STATIC_PATH = private.static_path

    def __init__(self):
        self._jcd_counter = 1
        self._weather_counter = 1
        self._bike_json = []
        self.weather_json = []


    def main(self):
        self.populate_weather()
        while True:
            time.sleep(1)
            if self._jcd_counter % 12 == 0:
                self._weather_counter += 1
                self.populate_weather()
            self.populate_bikes()
        
    def build_static_data(self):
        self.insert_to_db("staticdata", Scraper.STATIC_PATH)

    def populate_weather(self):
        print("WEATHER COUNTER AT START: ", self._weather_counter)
        data = self.get_weather_json()
        self.build_weather_csv(data, self._weather_counter)
        self.insert_to_db("weatherdata", Scraper.WEATHER_PATH)
        print("Weather successfully inserted")
        print("WEATHER COUNTER AT END: ", self._weather_counter)
        
    def populate_bikes(self):
        print("WEATHER COUNTER AT BIKES START: ", self._weather_counter)
        data = self.get_bike_json()
        print(self._weather_counter, self._jcd_counter, "here!!")
        self.build_bike_csv(data, self._weather_counter, self._jcd_counter)
        self.insert_to_db("dynamicdata", Scraper.STATIONS_PATH)
        print("successfully populated bikes")
        self._jcd_counter += 1
        time.sleep(30)

    def get_bike_json(self):
        r = requests.get(Scraper.STATIONS_URL, params={"apiKey": Scraper.BIKE_APIKEY,"contract": Scraper.NAME})
        print("bikes received")
        self._bike_json = json.loads(r.text)
        return self._bike_json

    def get_weather_json(self):
        r = requests.get(Scraper.URL, params={"apikey": Scraper.WEATHER_APIKEY, "language": Scraper.LANGUAGE,"details": Scraper.DETAILS})
        print("weather received")
        self.weather_json = json.loads(r.text)
        return self.weather_json

    def build_bike_csv(self, data, weather_time, download_counter):

        f = csv.writer(open("stations.csv", "w"))
        f.writerow(["number", "contract_name", "address", "latitude",
        "longitude","banking","bonus, bike_stands", "available_bike_stands","available_bikes",
        "status","last_update"])

        for x in data:
            f.writerow([
                download_counter,
                x["number"],
                x["last_update"],
                weather_time,
                x["banking"],
                x["bonus"],
                x["bike_stands"],
                x["available_bike_stands"],
                x["available_bikes"],
                x["status"],
                self.get_day(),
                self.get_hour_and_min()
                ])

    def build_weather_csv(self, json, time):
        f = csv.writer(open("weather.csv", "w"))
        f.writerow(["WeatherText", "Temperature - Celcius", "timestamp"])
        for x in json:
            f.writerow([ 
                time,
                x["WeatherText"], 
                x["Temperature"]['Metric']['Value'],
                x["EpochTime"],
                ])
    
    def insert_to_db(self, tablename, filename):
        path = filename
        cnx = MySQLdb.connect(user='root', password=Scraper.PASSWORD,
                                host='localhost',
                                database='comp30830', local_infile=True)

        # opening the cursor    
        cursor = cnx.cursor()
        script = """
        LOAD DATA LOCAL INFILE '{filenamepath}'
        INTO TABLE {tablename}
        FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
        IGNORE 1 LINES;
        """.format(filenamepath=path,tablename=tablename)
        cursor.execute(script)
        cursor.close()
        cnx.commit()
        print("inserted!!")

    
    def get_day(self):
        right_now = datetime.utcnow()
        dayName =(calendar.day_name[right_now.weekday()])
        return dayName

    def get_hour_and_min(self):
        right_now = datetime.utcnow()
        dayHour = datetime.strftime(right_now,"%H%M")
        return dayHour

my_test = Scraper()

# my_test.populate_weather()
my_test.main()