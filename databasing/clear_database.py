
import pymysql
  
import private

SQL_USER = private.raph_rds_user
SQL_HOST = private.raph_rds_host
PASSWORD = private.raph_rds_pw


import pymysql

import private

SQL_USER = private.raph_rds_user
SQL_HOST = private.raph_rds_host
PASSWORD = private.raph_rds_pw

def drop_and_restart():
        cnx = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=PASSWORD,
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
        print("tables dropped and remade")

drop_and_restart()
