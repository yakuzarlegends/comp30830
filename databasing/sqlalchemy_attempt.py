
# from numpy import genfromtxt
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, FLOAT, VARCHAR, BOOLEAN, PrimaryKeyConstraint
# from sqlalchemy.orm import sessionmaker, scoped_session
# from time import time
# from datetime import datetime
# import csv
# import json
# import pandas as pd
# import requests
# from pprint import pprint



# Base = declarative_base()

# class Record(Base):
#     __tablename__ = 'dynamicdata'
#     station_num = Column(Integer, primary_key=True)
#     contract_name = Column(VARCHAR(10))
#     name = Column(VARCHAR(40))
#     address = Column(VARCHAR(40))
#     longitude = Column(FLOAT(3,6))
#     latitude = Column(FLOAT(3,6))
#     banking = Column(BOOLEAN)
#     bonus = Column(BOOLEAN)
#     bike_stands = Column(Integer)
#     available_bikes = Column(Integer)
#     status = Column(BOOLEAN)
#     last_update = Column(Integer)
    


# session = sessionmaker(bind=engine)
# session = session()

# try:
#     file_name = "./stations.csv" 
#     data = Load_Data(file_name) 
#     for i in data:
#         record = Record(**{
#             'station_num': i[0],
#             'cn': i[1],
#             'name': i[2],
#             'add': i[3],
#             'long': i[4],
#             'lat': i[5],
#             'bank': i[6],
#             'bonus': i[7],
#             'bike_stands': i[8],
#             'av_bikes': i[9],
#             'status': i[10],
#             'last_up': i[11]
#         })
#         session.add(record)
#         session.commit() 
#         print("it worked!")
# except:
#     print("didn't work")
#     session.rollback() #Rollback the changes on error
# finally:
#     session.close() #Close the connection
    




