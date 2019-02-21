import csv
import sys
import private
import mysql.connector

fileName = sys.argv[1]
fileNameStr = str(fileName)


mydb = mysql.connector.connect(user=private.currentUser, password=private.mypassword,
                              host=private.myhost,
                              database=private.myDB)

cursor = mydb.cursor()

with open(fileNameStr) as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')

    for row in csv_data:
        cursor.execute('INSERT INTO alldata(number, contract_name, address, latitude, longitude, banking, bonus, bike_stands, available_bike_stands, available_bikes, status, last_update) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       row)
    # close the connection to the database.
    mydb.commit()
    cursor.close()
print("Done")
