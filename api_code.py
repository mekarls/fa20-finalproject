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

def create_iss_tables(cur, conn):
  
    
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data' 
    ('date' TEXT, 'time' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')
    

    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Raw' 
    ('date' TEXT, 'time' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    for _ in range(10):
        iss_data = iss_position()
        iss_data = iss_data.split(',')
        unix = iss_data[0]
        time_update = (datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')).split()
        date = time_update[0]
        t = time_update[1]
        lat = iss_data[1]
        lon = iss_data[2]
        
        cur.execute('INSERT INTO ISS_Raw (date, time, latitude, longitude) VALUES (?, ?, ?, ?)', (date, t, lat, lon))
        conn.commit()

        time.sleep(15)
        print('done')

def create_weather_tables(cur, conn): #should create a new table 
    #wdir, temp, maxt, wspd, precip, dew, humidity, conditions, time zone
    
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Time_Zones'
    ('id' INTEGER PRIMARY KEY, 'time_zone' TEXT UNIQUE)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS 'Weather' 
    ('time_zone' INTEGER, 'wind_dir' REAL, 'temp' REAL, 'max_temp' REAL, 'windspeed' REAL, 'precipitation' REAL, 'dew' REAL, 'humidity' REAL, 'conditions' TEXT)''')


def weather(cur, conn):

    api_key = '97H6P669AZU5PIG16JBC5N4ES'
    base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history/'
 
    cur.execute('SELECT * FROM ISS_Raw')
    data1 = cur.fetchall()
  
    count = 0 # prints with each 25 so we know how much we get

    for i in data1[691:707]: # x[191:216] x[216:241] x[241:266] x[266:276] x[276:286] intervals to test
        # print(i)
        dat, tim, lat, lon= i[0], i[1], i[2], i[3]
        # print(dat, tim)
        req = requests.get(f'{base_url}?&aggregateHours=1&startDateTime={dat}T{tim}&contentType=json&location={lat},{lon}&key={api_key}')
        resp = req.json()


        if 'errorCode' not in resp:

            w = []
            # wdir, temp, maxt, wspd, precip, dew, humidity, conditions, time zone
            wdir = resp['locations'][f'{lat},{lon}']['values'][0]['wdir']
            temp = resp['locations'][f'{lat},{lon}']['values'][0]['temp']
            maxt = resp['locations'][f'{lat},{lon}']['values'][0]['maxt']
            wspd = resp['locations'][f'{lat},{lon}']['values'][0]['wspd']
            precip = resp['locations'][f'{lat},{lon}']['values'][0]['precip']
            dew = resp['locations'][f'{lat},{lon}']['values'][0]['dew']
            humidity= resp['locations'][f'{lat},{lon}']['values'][0]['humidity']
            conditions = resp['locations'][f'{lat},{lon}']['values'][0]['conditions']
            time_zone = resp['locations'][f'{lat},{lon}']['tz']

            w.extend([wdir, temp, maxt, wspd, precip, dew, humidity, conditions, time_zone])
            # print(w)
            if '' not in w:
            # #     print(w)
                count += 1

                cur.execute('''INSERT INTO ISS_Data (date, time, latitude, longitude) VALUES (?, ?, ?, ?)''', (dat, tim, lat, lon))
                conn.commit()
            
                cur.execute('INSERT OR IGNORE INTO Time_Zones (time_zone) VALUES (?)', (time_zone,))
                conn.commit()

                # create time zone id dictionary
                cur.execute("SELECT * FROM Time_Zones")
                tz_ids = {}
                tzs = cur.fetchall()
                
                for t in tzs:
                    id = t[0]
                    tz = t[1]
                    tz_ids[tz] = id

                tz_id = tz_ids[time_zone]
                # print(tz_id)
                cur.execute('''INSERT INTO Weather (time_zone, wind_dir, temp, max_temp, windspeed, precipitation, dew, humidity, conditions) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (tz_id, wdir, temp, maxt, wspd, precip, dew, humidity, conditions))
                conn.commit()
    print(count)
            
    # pass


def create_daylight_table(cur, conn):
    """make sure to commit new data"""
    
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Daylight' 
    ('sunrise' TEXT, 'sunset' TEXT, 'solar_noon' TEXT, 'day_length' TEXT)''')
    #{'results': {'sunrise': '1:14:49 PM', 'sunset': '9:39:33 PM', 'solar_noon': '5:27:11 PM', 'day_length': '08:24:44', 'civil_twilight_begin': '12:37:37 PM', 'civil_twilight_end': '10:16:46 PM', 'nautical_twilight_begin': '11:56:55 AM', 'nautical_twilight_end': '10:57:28 PM', 'astronomical_twilight_begin': '11:18:02 AM', 'astronomical_twilight_end': '11:36:21 PM'}, 'status': 'OK'}

    cur.execute('SELECT latitude, longitude, date FROM ISS_Data')
    data = cur.fetchall()
    # print(data)
    for d in data[76:104]: #increment manually
        lat, long, date = d[0], d[1], d[2]
        # print(lat, long, date)
    #important to note for calculations- given in UTC (coordinated universal time)
        base_url = 'https://api.sunrise-sunset.org/json'
        req = requests.get(f'{base_url}?lat={lat}&lng={long}&date={date}')
        resp = req.json()
        resp_dict = resp['results']

        rise, set, solar, length = resp_dict['sunrise'], resp_dict['sunset'], resp_dict['solar_noon'], resp_dict['day_length']
        # print(rise, set, solar, length)
        cur.execute('INSERT INTO Daylight (sunrise, sunset, solar_noon, day_length) VALUES (?, ?, ?, ?)', (rise, set, solar, length))
        conn.commit()

    # pass





def main():

    # Database and Tables
    cur, conn = setUpDatabase('API_Data.db')
   
    # create_iss_tables(cur, conn)
    
    # create_weather_tables(cur, conn)
    
    # weather(cur, conn)
    
    # create_daylight_table(cur, conn)

# if __name__ == '__main__':
    main()





