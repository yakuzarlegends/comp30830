# Import pandas, numpy and matplotlib libraries
import math
import pandas as pd
import numpy as np
import requests
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pymysql
from sklearn.externals import joblib
import os
import csv


KIERAN_RDS_HOST = os.environ['KIERAN_RDS_HOST']
KIERAN_RDS_USER = os.environ['KIERAN_RDS_USER']
KIERAN_RDS_PW = os.environ['KIERAN_RDS_PW']

# Don't run this unless you have to. It takes a long time.
# This function fetches the SQL information and creates CSV files

def SQLtoCSV():

    def execute(c, command):
        c.execute(command)
        return c.fetchall()

    # Change these to environmental variables
    db = pymysql.connect(host=KIERAN_RDS_HOST, port=3306, user=KIERAN_RDS_USER, passwd=KIERAN_RDS_PW, db='comp30830') #, charset='utf8')

    c = db.cursor()

    for table in execute(c, "show tables;"):
        table = table[0]
        cols = []
        for item in execute(c, "show columns from " + table + ";"):
            cols.append(item[0])
        data = execute(c, "select * from " + table + ";")
        with open(table + ".csv", "w", encoding="utf-8") as out:
            out.write(",".join(cols) + "\n")
            for row in data:
                out.write(",".join(str(el) for el in row) + "\n")
        print(table + ".csv written")

    createDynamicWeather()

    df=cleanCSV()

    buildModel(df)

# This function joins the dynmaicdata CSV and weatherdata CSV into one new CSV: DynamicWeather

def createDynamicWeather():
    dynamicdata = pd.read_csv('dynamicdata.csv',  keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    weatherdata = pd.read_csv('weatherdata.csv',  keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    df=dynamicdata.merge(weatherdata, left_on='weather_id', right_on='id', how='inner')
    df.to_csv('dynamic_weather.csv', index=False)



def cleanCSV():
    df = pd.read_csv('dynamic_weather.csv',  keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    df=df[['station_id','weekday','hour_and_minute', 'weather_text','hasprecip','isday','tempc','rftempc', 'windspeedv','available_bikes']]
    
    df['hour'] = df['hour_and_minute'] // 100
    
    categorical_columns = df[['station_id', 'weekday','weather_text','hour']].columns
    
    for column in categorical_columns:
        df[column] = df[column].astype('category')
    df=df.drop(['hour_and_minute'], axis=1)
    return df


def buildModel(df):
    df_dummies = pd.get_dummies(df)
    # equiv to dfohe 

    dependent_variable = 'available_bikes'
    x = df_dummies[df_dummies.columns.difference([dependent_variable])]
    y = df_dummies[dependent_variable]
    rf = RandomForestRegressor(n_estimators = 10, random_state = 66)
    rf.fit(x,y)
    joblib.dump(rf, 'model.pkl')
    
    model_columns = list(x.columns)
    joblib.dump(model_columns, 'model_columns.pkl')


SQLtoCSV()

