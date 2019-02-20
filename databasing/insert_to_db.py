import MySQLdb  
import os

# this is mysqlclient

# importing our private variables
from private import pw

def insert(tablename):
    path = '/Users/raph/Sites/Learning/UCD/Semester 2/Software Engineering/group_assignment/project_directory/comp30830/databasing/weather.csv'
    # path = os.path.dirname(os.path.abspath(filename))
    cnx = MySQLdb.connect(user='root', password=pw,
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


    