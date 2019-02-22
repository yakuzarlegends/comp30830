import requests
import time
import csv
import json
import calendar
import private
import pymysql
from datetime import datetime

class Scraper:
    
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
    SQL_USER = private.raph_rds_user
    SQL_HOST = private.raph_rds_host
    PASSWORD = private.raph_rds_pw
    # SQL_USER = private.sql_user
    # SQL_HOST = private.sql_host
    # PASSWORD = private.pw


    def __init__(self):
        self._jcd_counter = 1
        self._weather_counter = 0
        self._bike_json = []
        self.weather_json = []


    def main(self):
        self.drop_and_restart()
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
        while True:
            try: 
                r = requests.get(Scraper.STATIONS_URL, params={"apiKey": Scraper.BIKE_APIKEY,"contract": Scraper.NAME})
                print("bikes received")
                self._bike_json = json.loads(r.text)
                return self._bike_json
            except: 
                pass
        

    def get_weather_json(self):
        while True:
            try:
                r = requests.get(Scraper.URL, params={"apikey": Scraper.WEATHER_APIKEY, "language": Scraper.LANGUAGE,"details": Scraper.DETAILS})
                print("weather received")
                self.weather_json = json.loads(r.text)
                return self.weather_json
            except: 
                pass

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

    def drop_and_restart(self):
        cnx = pymysql.connect(host=Scraper.SQL_HOST, user=Scraper.SQL_USER, password=Scraper.PASSWORD,
                                database='comp30830', local_infile=1)
        cursor = cnx.cursor()
        script = """
        drop table dynamicdata; 
        """
        cursor.execute(script)
        script = """
        drop table weatherdata;
        """
        cursor.execute(script)
        script = """

                CREATE TABLE weatherdata (
        id INT PRIMARY KEY,
        weather_text VARCHAR(255),
        temperature DECIMAL(3,1),
        timestamp BIGINT
        );
        """
        cursor.execute(script)
        script = """

CREATE TABLE dynamicdata (
download_number INT,
station_id INT,
timestamp BIGINT,
weather_id INT,
banking VARCHAR(10),
bonus VARCHAR(10),
total_bike_stands INT,
available_bike_stands INT,
available_bikes INT,
status VARCHAR(10),
weekday VARCHAR(20),
hour_and_minute INT(4),

CONSTRAINT pk_station PRIMARY KEY (station_id, download_number),

CONSTRAINT station_fk
FOREIGN KEY (station_id)
REFERENCES staticdata (number)
ON DELETE RESTRICT
ON UPDATE CASCADE,

CONSTRAINT weather_fk
FOREIGN KEY (weather_id)
REFERENCES weatherdata (id)
ON DELETE RESTRICT
ON UPDATE CASCADE
);
     """
        cursor.execute(script)
        cursor.close()
        cnx.commit()

    def insert_to_db(self, tablename, filename):
        path = filename
        cnx = pymysql.connect(host=Scraper.SQL_HOST, user=Scraper.SQL_USER, password=Scraper.PASSWORD,
                                database='comp30830', local_infile=1)
        # opening the cursor    
        cursor = cnx.cursor()
        script = """
        LOAD DATA LOCAL INFILE '{filenamepath}'
        INTO TABLE {tablename}
        FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
        IGNORE 1 LINES;
        """.format(filenamepath=path,tablename=tablename)
        cursor.execute(script)
        cnx.commit()
        cursor.close()
        
        
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