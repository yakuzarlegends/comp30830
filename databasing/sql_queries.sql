-- CREATE dynamicdata table

CREATE TABLE dynamicdata (number INT,contract_name VARCHAR(30), address VARCHAR(30),latitude DECIMAL(10,8),longitude DECIMAL(11,8), banking BOOL,bonus BOOL, bike_stands INT, available_bike_stands INT, available_bikes INT, status VARCHAR(10),last_update TIMESTAMP);

-- ----------------------------------

-- CSV FILE ENTRY

LOAD DATA LOCAL INFILE '{path}'
INTO TABLE dynamicdata 
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
IGNORE 1 LINES;


-- CREATE STATIC DATA

CREATE TABLE staticdata (
number INT PRIMARY KEY, 
name VARCHAR(255) NOT NULL, 
address VARCHAR(255) NOT NULL, 
latitude DECIMAL(10,8) NOT NULL, 
longitude DECIMAL(11,8) NOT NULL);

-- CREATE WEATHER DATA

CREATE TABLE weatherdata (
id INT PRIMARY KEY,
weather_text VARCHAR(255),
temperature DECIMAL(3,1)
)

-- CREATE DYNAMIC DATA

CREATE TABLE dynamicdata (
counter_id INT,
station_id INT,
timestamp INT(15),
weather_id INT,
banking VARCHAR(10),
bonus VARCHAR(10),
total_bike_stands INT,
available_bike_stands INT,
available_bikes INT,
status VARCHAR(10),
weekday VARCHAR(20),
hour_and_minute TIME,

CONSTRAINT pk_station PRIMARY KEY (station_id, timestamp),

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