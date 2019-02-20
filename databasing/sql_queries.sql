-- CREATE dynamicdata table

CREATE TABLE dynamicdata (number INT,contract_name VARCHAR(30), address VARCHAR(30),latitude DECIMAL(10,8),longitude DECIMAL(11,8), banking BOOL,bonus BOOL, bike_stands INT, available_bike_stands INT, available_bikes INT, status VARCHAR(10),last_update TIMESTAMP);

-- ----------------------------------

-- CSV FILE ENTRY

LOAD DATA LOCAL INFILE '{path}'
INTO TABLE dynamicdata 
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
IGNORE 1 LINES;


-- test