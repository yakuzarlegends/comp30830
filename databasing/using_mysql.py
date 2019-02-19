import MySQLdb  
# this is mysqlclient

# importing our private variables
from private import pw

path = '/Users/raph/Sites/Learning/UCD/Semester 2/Software Engineering/group_assignment/project_directory/comp30830/databasing/stations.csv'

# setting up our connection
cnx = MySQLdb.connect(user='root', password=pw,
                              host='localhost',
                              database='comp30830', local_infile=True)


# opening the cursor
cursor = cnx.cursor()


# sending in the CSV File. 
script = """
LOAD DATA LOCAL INFILE '{path}'
INTO TABLE dynamicdata 
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
IGNORE 1 LINES;
""".format(path=path)

print(script)
cursor.execute(script)

cursor.close()
cnx.commit()