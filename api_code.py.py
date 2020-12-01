# SI 206 Final Project - STE(a)Migos
# Names: Michelle Karls, Selin Fidan, Julia Couch

import requests
import json
import os
import unittest
import sqlite3
import urllib.request
import time
from datetime import datetime


# step 1: create database
def setUpDatabase(db_name):    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# step 2: define function to request iss_data

def iss_position():
    base_url = 'http://api.open-notify.org/iss-now.json'
    req = requests.get(base_url)
    data = req.json()
    time = data['timestamp'] #str
    lat = data['iss_position']['latitude'] #str
    long = data['iss_position']['longitude'] #str
    
    return f'{time},{lat},{long}'

# step 3: read api into database

def create_iss_table(cur, conn):
    """make sure to commit new data"""
  
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data' 
    ('location_id' INTEGER PRIMARY KEY, 'unix' TEXT, 'date' TEXT, 'time' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    for _ in range(25):
        iss_data = iss_position()
        iss_data = iss_data.split(',')
        unix = iss_data[0]
        time_update = (datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')).split()
        date = time_update[0]
        t = time_update[1]
        lat = iss_data[1]
        long = iss_data[2]
        
        cur.execute('INSERT INTO ISS_Data (unix, date, time, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (unix, date, t, lat, long))
        conn.commit()

        time.sleep(30)


def create_weather_table(cur, conn): #should create a new table 
    # cur.execute('''CREATE TABLE IF NOT EXISTS 'Weather' 
    # ('location' TEXT UNIQUE, 
    # FOREIGN KEY ('location_id') REFERENCES ISS_Data (location_id),
    # 'temp' TEXT, 'humidity' TEXT', 'windspeed' TEXT, 'cloudcover' TEXT, 'visibility' TEXT)''')
    # # not sure I did the foreign key right, we can ask Fernando during discussion tmw maybe
    
    # conn.commit()
    pass

def weather(cur, conn):

    api_key = '97H6P669AZU5PIG16JBC5N4ES'
    # base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history/'

    cur.execute('SELECT latitude, longitude, date FROM ISS_Data')
    data1 = cur.fetchall()

    data2 = []
    for i in data1[1]:
        lat = i[0]
        lon = i[1]
        dat = i[2]
        r = requests.get(base_url + '?locations=' + lat + ',' + lon + '/' + "&dayStartTime=" + dat + "&dayEndTime" + dat + "?key=" + api_key)
        a = r.text()
     
        

  

 
   

def create_daylight_table(cur, conn):
    """make sure to commit new data"""
    pass

def daylight(params):
    #select data from ISS_Data to input into requests
    pass



def main():
    
    # pass
    # Database and Tables
    cur, conn = setUpDatabase('API_Data.db')
   
    #create_iss_table(cur, conn)
    #create_weather_table(cur, conn)
    #create_weather_table(cur, conn)
    # create_weather_table(cur, conn)
    weather(cur, conn)
    # create_daylight_table(cur, conn)
if __name__ == '__main__':
    main()