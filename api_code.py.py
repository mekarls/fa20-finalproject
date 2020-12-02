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
  
    cur.execute("DROP TABLE IF EXISTS 'ISS_Data'")
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data' 
    ('location_id' INTEGER PRIMARY KEY, 'unix' TEXT, 'date' TEXT, 'time' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    for _ in range(10):
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


def create_weather_tables(cur, conn): #should create a new table 
    #wdir, temp, maxt, wspd, precip, dew, humidity, conditions, time zone
    
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Time_Zones'
    ('id' INTEGER PRIMARY KEY, 'time_zone' TEXT)''')

    # cur.execute('''CREATE TABLE IF NOT EXISTS 'Weather' 
    # ('wind_dir' REAL, 'temp' REAL, 'max_temp' REAL, 'windspeed' REAL, 'precipitation' REAL, 'dew' REAL, 'humidity' REAL, 'conditions' TEXT)''')
    
    # conn.commit()


    pass

def weather(cur, conn):

    api_key = '97H6P669AZU5PIG16JBC5N4ES'
    base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history/'

    cur.execute('SELECT latitude, longitude, date, time FROM ISS_Data')
    data1 = cur.fetchall()

    time_zones = []

    for i in data1:
        lat = i[0]
        lon = i[1]
        dat = i[2]
        tim = i[3]
        # print(tim)
        req = requests.get(f'{base_url}?&aggregateHours=1&startDateTime={dat}T{tim}&contentType=json&location={lat},{lon}&key={api_key}')
        resp = req.json()
        print(resp)
        # obj = json.dumps(resp)
        # # print(type(obj))
        # print(resp['location'])
        # #wdir, temp, maxt, wspd, precip, dew, humidity, conditions, time zone
        # wdir = resp['locations'][f'{lat},{lon}']['values'][0]['wdir']
        # temp = resp['locations'][f'{lat},{lon}']['values'][0]['temp']
        # maxt = resp['locations'][f'{lat},{lon}']['values'][0]['maxt']
        # wspd = resp['locations'][f'{lat},{lon}']['values'][0]['wspd']
        # precip = resp['locations'][f'{lat},{lon}']['values'][0]['precip']
        # dew = resp['locations'][f'{lat},{lon}']['values'][0]['dew']
        # humidity= resp['locations'][f'{lat},{lon}']['values'][0]['humidity']
        # conditions = resp['locations'][f'{lat},{lon}']['values'][0]['conditions']
        # time_zone = resp['locations'][f'{lat},{lon}']['tz']
        # print(time_zone)
        
        # concise_data.append((wdir, temp, maxt, wspd, precip, dew, humidity, conditions))
        # if time_zone not in time_zones:
        #     time_zones.append(time_zone)
        
        # for tz in time_zones:
        #     cur.execute('INSERT INTO Time_Zones (time_zone) VALUES (?)', (tz,))
    # print(time_zones) 
        # cur.execute('''INSERT INTO Weather (wind_dir, temp, max_temp, windspeed, precipitation, dew, humidity, conditions) 
        # VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (wdir, temp, maxt, wspd, precip, dew, humidity, conditions)) #put in time_zone id
    # pass
    

'''             things to ask at office hours:
1) x
2) how to create one table with location_id and time zone (as part of weather tables) that we can then use as foreign keys for the daylight table
3) how do we pull from the database in one file to make the visualizations if it's created in a different file
'''  

def create_daylight_table(cur, conn):
    """make sure to commit new data"""
    
    cur.execute("DROP TABLE IF EXISTS 'Daylight'")
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Daylight' 
    ('sunrise' TEXT, 'sunset' TEXT, 'solar_noon' TEXT, 'day_length' TEXT)''')
    #{'results': {'sunrise': '1:14:49 PM', 'sunset': '9:39:33 PM', 'solar_noon': '5:27:11 PM', 'day_length': '08:24:44', 'civil_twilight_begin': '12:37:37 PM', 'civil_twilight_end': '10:16:46 PM', 'nautical_twilight_begin': '11:56:55 AM', 'nautical_twilight_end': '10:57:28 PM', 'astronomical_twilight_begin': '11:18:02 AM', 'astronomical_twilight_end': '11:36:21 PM'}, 'status': 'OK'}

    cur.execute('SELECT latitude, longitude, date FROM ISS_Data')
    data = cur.fetchall()
    # print(data)
    for d in data[:5]: #increment manually
        lat, long, date = d[0], d[1], d[2]
    
    #important to note for calculations- given in UTC (coordinated universal time)
        base_url = 'https://api.sunrise-sunset.org/json'
        req = requests.get(f'{base_url}?lat={lat}&lng={long}&date={date}')
        resp = req.json()
        resp_dict = resp['results']

        rise, set, solar, length = resp_dict['sunrise'], resp_dict['sunset'], resp_dict['solar_noon'], resp_dict['day_length']
       
        cur.execute('INSERT INTO Daylight (sunrise, sunset, solar_noon, day_length) VALUES (?, ?, ?, ?)', (rise, set, solar, length))
        conn.commit()

    pass





def main():

    # Database and Tables
    cur, conn = setUpDatabase('API_Data.db')
   
    # create_iss_table(cur, conn)

    # create_weather_tables(cur, conn)
    # weather(cur, conn)
    # create_daylight_table(cur, conn)

if __name__ == '__main__':
    main()


'''             here's what we need to do
1) collect lots of iss data 25 at a time
2) call it all through the weather api (sorry julia, will help pay !)
3) if it does not return an error, we add it to a new iss_data table
4) if it does return an error, we do nothing special with it
5) we keep going until the iss_data table has 100 items that will run properly through the weather api
'''
