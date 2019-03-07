import requests
import time
import csv
import json
import calendar
import pymysql
from datetime import datetime
import os

class Scraper:

    DETAILS = "true"    
    METRIC = "true" 
    NAME="dublin"
    LANGUAGE = "en-us"

    STATIC_PATH = "./static.csv"

    # WEATHER
    YVETTE_WEATHER_API = os.environ['YVETTE_WEATHER_API']
    RAPH_WEATHER_API = os.environ['RAPH_WEATHER_API']
    WEATHER_URL = os.environ['WEATHER_URL']

    # BIKES

    JCD_API = os.environ['JCD_API']
    JCD_URL = os.environ['JCD_URL']

    # Kieran RDS

    KIERAN_RDS_HOST = os.environ['KIERAN_RDS_HOST']
    KIERAN_RDS_USER = os.environ['KIERAN_RDS_USER']
    KIERAN_RDS_PW = os.environ['KIERAN_RDS_PW']

    # Raph RDS

    RAPH_RDS_PW = os.environ['RAPH_RDS_PW']
    RAPH_RDS_USER = os.environ['RAPH_RDS_USER']
    RAPH_RDS_HOST = os.environ['RAPH_RDS_HOST']

    # CSVs

    STATIONS = os.environ['STATIONS']
    WEATHER = os.environ['WEATHER']




    
    # WEATHER_APIKEY = private.yvette_weather_api
    # BIKE_APIKEY = private.jcd_api
 
    # DETAILS = "false"
    # URL = private.weather_url
    # STATIONS_URL = private.jcd_url
    # WEATHER_PATH = private.weather
    # STATIONS_PATH = private.stations
    # NAME = "dublin"
    # STATIC_PATH = private.static_path
    # SQL_USER = private.raph_rds_user
    # SQL_HOST = private.raph_rds_host
    # PASSWORD = private.raph_rds_pw
    # SQL_USER = private.sql_user
    # SQL_HOST = private.sql_host
    # PASSWORD = private.pw


    def __init__(self):
        self._jcd_counter = 1
        self._weather_counter = 1
        self._bike_json = []
        self.weather_json = []


    def main(self):
        self.drop_and_restart()
        self.populate_weather()
        while True:
            time.sleep(1)
            if self._jcd_counter == self._weather_counter * 12 + 1:
                self._weather_counter += 1
                self.populate_weather()
            self.populate_bikes()     

   
    def build_static_data(self):
        self.insert_to_db("staticdata", Scraper.STATIC_PATH)


    def populate_weather(self):
        print("WEATHER COUNTER AT START: ", self._weather_counter)
        data = self.get_weather_json()
        self.build_weather_csv(data, self._weather_counter)
        self.insert_to_db("weatherdata", Scraper.WEATHER)
        print("Weather successfully inserted")
        print("WEATHER COUNTER AT END: ", self._weather_counter)
        
    def populate_bikes(self):
        print("WEATHER COUNTER AT BIKES START: ", self._weather_counter)
        data = self.get_bike_json()
        print(self._weather_counter, self._jcd_counter, "here!!")
        self.build_bike_csv(data, self._weather_counter, self._jcd_counter)
        self.insert_to_db("dynamicdata", Scraper.STATIONS)
        print("successfully populated bikes")
        self._jcd_counter += 1
        time.sleep(5*60)

    def get_bike_json(self):
        while True:
            try: 
                r = requests.get(Scraper.JCD_URL, params={"apiKey": Scraper.JCD_API,"contract": Scraper.NAME})
                print("bikes received")
                self._bike_json = json.loads(r.text)
                return self._bike_json
            except: 
                pass
        

    def get_weather_json(self):
        while True:
            try:
                r = requests.get(Scraper.WEATHER_URL, params={"apikey": Scraper.YVETTE_WEATHER_API, "language": Scraper.LANGUAGE,"details": Scraper.DETAILS,"metric": Scraper.METRIC})
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
        f.writerow(["WeatherText", "HasPrecip", "PrecipType", "IsDay", "TempC","FRTempC","FRTempShadeC",
        "RelatHum","DewPointC","WindDir","WindSpeedV", "WindSpeedU","WindGustV", "WindGustU","UVIndex",
        "UVText","VisibilityV","VisibilityU","CloudCover","CeilingV", "CeilingU","PressureV","PressureU",
        "PressTendC", "WindChillC", "Precip1V","Precip1U","timestamp"])
        for x in json:
            f.writerow([ 
                time,
                x["WeatherText"],
                x["HasPrecipitation"],
                x["PrecipitationType"], 
                x["IsDayTime"],
                x["Temperature"]['Metric']['Value'],
                x["RealFeelTemperature"]['Metric']['Value'],
                x["RealFeelTemperatureShade"]['Metric']['Value'],
                x["RelativeHumidity"],
                x["DewPoint"]['Metric']['Value'], 
                x["Wind"]['Direction']['English'],
                x["Wind"]["Speed"]['Metric']['Value'],
                x["Wind"]["Speed"]['Metric']['Unit'],
                x["WindGust"]["Speed"]['Metric']['Value'],
                x["WindGust"]["Speed"]['Metric']['Unit'],
                x["UVIndex"],
                x["UVIndexText"],
                x["Visibility"]['Metric']['Value'],
                x["Visibility"]['Metric']['Unit'],
                x["CloudCover"],
                x["Ceiling"]['Metric']['Value'],
                x["Ceiling"]['Metric']['Unit'],
                x["Pressure"]['Metric']['Value'],
                x["Pressure"]['Metric']['Unit'],
                x["PressureTendency"]['Code'],
                x["WindChillTemperature"]['Metric']['Value'],
                x["Precip1hr"]['Metric']['Value'],
                x["Precip1hr"]['Metric']['Unit'],
                x["EpochTime"],
                ])        

    def drop_and_restart(self):
        cnx = pymysql.connect(host=Scraper.KIERAN_RDS_HOST, user=Scraper.KIERAN_RDS_USER, password=Scraper.KIERAN_RDS_PW,
                                database='comp30830', local_infile=1)
        cursor = cnx.cursor()
        script = """
        drop table if exists dynamicdata; 
        """
        cursor.execute(script)
        script = """
        drop table weatherdata;
        """
        cursor.execute(script)
        
        script = """
        CREATE TABLE weatherdata (
        id INT PRIMARY KEY,
        weather_text VARCHAR(50),
        hasprecip VARCHAR(5),
        preciptype VARCHAR(20),
        isday VARCHAR(5),
        tempc DECIMAL(7,2),
        rftempc DECIMAL(7,2),
        rftempshadec DECIMAL(7,2),
        relathum INT,
        dewpointc DECIMAL(7,2),
        winddir VARCHAR(6),
        windspeedv DECIMAL(7,2), 
        windspeedu VARCHAR(6),
        windgustv DECIMAL(7,2),
        windgustu VARCHAR(6),
        uvindex INT,
        uvtext VARCHAR(15),
        visibilityv DECIMAL(7,2),
        visibilityu VARCHAR(6),
        cloudCover INT(3),
        ceilingv DECIMAL(7,2),
        Ceilingu VARCHAR(6),
        pressurev DECIMAL(7,2),
        pressureu VARCHAR(6),
        presstendc VARCHAR(1),
        windchillc DECIMAL(7,2),
        precipval DECIMAL(10,2),
        precipunit VARCHAR(6),
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
        cnx = pymysql.connect(host=Scraper.KIERAN_RDS_HOST, user=Scraper.KIERAN_RDS_USER, password=Scraper.KIERAN_RDS_PW,
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