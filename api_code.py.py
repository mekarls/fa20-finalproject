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
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Weather' 
    ('location' TEXT UNIQUE, 
    FOREIGN KEY (location_id) REFERENCES ISS_Data (location_id),
    'temp' TEXT, 'humidity' TEXT', 'windspeed' TEXT, 'cloudcover' TEXT, 'visibility' TEXT)''')
    # not sure I did the foreign key right, we can ask Fernando during discussion tmw maybe
    
    conn.commit()
  

def weather(cur, conn):

    api_key = '97H6P669AZU5PIG16JBC5N4ES'
    base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

    #get information about avg1
    cur.execute('SELECT avg_lat, avg_long, date FROM Avg_ISS WHERE id = 1')
    avg1 = cur.fetchone()
    lat1 = str(avg1[0])
    long1 = str(avg1[1])
    date1 = str(avg1[2])

    r = requests.get(base_url + lat1 + ',' + long1 + '/' + date1 + "?key=" + api_key)
    data = r.json()
    avg1_json = json.dumps(data)
    print(avg1_json)
   
    

    
    

    #get information about avg2
    cur.execute('SELECT avg_lat, avg_long, date FROM Avg_ISS WHERE id = 2')
    avg2 = cur.fetchone()
    lat2 = str(avg2[0])
    long2 = str(avg2[1])
    date2 = str(avg2[2])

    #get information about avg3
    cur.execute('SELECT avg_lat, avg_long, date FROM Avg_ISS WHERE id = 3')
    avg3 = cur.fetchone()
    lat3 = str(avg3[0])
    long3 = str(avg3[1])
    date3 = str(avg3[2])


    #get information about avg4
    cur.execute('SELECT avg_lat, avg_long, date FROM Avg_ISS WHERE id = 4')
    avg4 = cur.fetchone()
    lat4 = str(avg4[0])
    long4 = str(avg4[1])
    date4 = str(avg4[2])
    pass


 
   

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
   
    create_iss_table(cur, conn)
    
    #create_weather_table(cur, conn)
    # create_weather_table(cur, conn)
    #weather(cur, conn) DO NOT UNCOMMENT UNTIL ABSOLUTELY GOOD AND SURE AND READY

    # create_daylight_table(cur, conn)
if __name__ == '__main__':
    main()