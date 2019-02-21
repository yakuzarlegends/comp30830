import mysql.connector
import private

cnx = mysql.connector.connect(user=private.currentUser, password=private.mypassword,
                              host=private.myhost,
                              database=private.myDB)
cursor = cnx.cursor()
cursor.execute("""

 CREATE TABLE IF NOT EXISTS alldata (
data_id INT AUTO_INCREMENT,
number INT, 
contract_name VARCHAR(255), 
address VARCHAR(255), 
latitude FLOAT, 
longitude FLOAT, 
banking VARCHAR(255), 
bonus VARCHAR(255), 
bike_stands INT, 
available_bike_stands INT,
available_bikes INT, 
status VARCHAR(255), 
last_update VARCHAR(255),
PRIMARY KEY (data_id)
)  ENGINE=INNODB;

""")

cnx.close()