# SI 206 Final Project - STE(a)Migos
# Names: Michelle Karls, Selin Fidan, Julia Couch

import requests
import json
import os
import unittest
import sqlite3
import urllib.request
from datetime import datetime

# ------------------TUESDAY, NOV 24------------------
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
    # return {"time": time, "lat": lat, "long": long}
    return f'{time},{lat},{long}'

# step 3: write iss_data to csv file

def write_iss_csv():
    header = 'time,latitude,longitude'
    # f = open('iss_pos.csv', 'w')
    #f = open('iss_pos2.csv', 'w')
    #f = open('iss_pos3.csv', 'w')
    # f = open('iss_pos4.csv', 'w')
    f.write(header+'\n')
    f.close()
    for _ in range(25):
        iss_data = iss_position()
        # f = open('iss_pos.csv', 'a')
        #f = open('iss_pos2.csv', 'a')
        #f = open('iss_pos3.csv', 'a')
        # f = open('iss_pos4.csv', 'a')
        f.write(iss_data+'\n')
        f.close() 

# step 4: read csv file into database

def create_iss_table(cur, conn):
    """make sure to commit new data"""
  
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_1' 
    ('avg_id' integer, 'unix' text, 'latitude' text, 'longitude' text)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_2' 
    ('avg_id' integer, 'unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_3' 
    ('avg_id' integer, 'unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_4' 
    ('avg_id' integer, 'unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

def insert_iss_data(cur, conn):    
    # with open('iss_pos.csv', 'r') as fhand:
    # with open('iss_pos2.csv', 'r') as fhand:
    # with open('iss_pos3.csv', 'r') as fhand:
    with open('iss_pos4.csv', 'r') as fhand:
    
        lines = fhand.readlines()
        
        times = []
        lats = []
        longs = []

        for line in lines[1:]:
            line = line.strip().split(',')
            time = line[0]
            lat = line[1]
            long = line[2]

            times.append(int(time))
            lats.append(float(lat))
            longs.append(float(long))

            # cur.execute('INSERT INTO ISS_Data_1 (avg_id, unix, latitude, longitude) VALUES (?, ?, ?, ?)', (1, time, lat, long))
            # cur.execute('INSERT INTO ISS_Data_2 (avg_id, unix, latitude, longitude) VALUES (?, ?, ?, ?)', (2, time, lat, long))
            # cur.execute('INSERT INTO ISS_Data_3 (avg_id, unix, latitude, longitude) VALUES (?, ?, ?, ?)', (3, time, lat, long))
            cur.execute('INSERT INTO ISS_Data_4 (avg_id, unix, latitude, longitude) VALUES (?, ?, ?, ?)', (4, time, lat, long))
            conn.commit()

        t = sum(times)/float(len(times))
        t_update = (datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')).split() #returns date, time
        la = round(sum(lats)/float(len(lats)), 4)
        lo = round(sum(longs)/float(len(longs)), 4)
        
        # cur.execute("DROP TABLE IF EXISTS 'Avg_ISS'")
        cur.execute('''CREATE TABLE IF NOT EXISTS 'Avg_ISS'
        (id INTEGER PRIMARY KEY, avg_unix NUMBER, date TEXT, time TEXT, avg_lat NUMBER, avg_long NUMBER)''')

        # cur.execute('INSERT INTO Avg_ISS (id, avg_unix, date, time, avg_lat, avg_long) VALUES (?, ?, ?, ?, ?, ?)', (1, t, t_update[0], t_update[1], la, lo))
        # cur.execute('INSERT INTO Avg_ISS (id, avg_unix, date, time, avg_lat, avg_long) VALUES (?, ?, ?, ?, ?, ?)', (2, t, t_update[0], t_update[1], la, lo))
        # cur.execute('INSERT INTO Avg_ISS (id, avg_unix, date, time, avg_lat, avg_long) VALUES (?, ?, ?, ?, ?, ?)', (3, t, t_update[0], t_update[1], la, lo))
        # cur.execute('INSERT INTO Avg_ISS (id, avg_unix, date, time, avg_lat, avg_long) VALUES (?, ?, ?, ?, ?, ?)', (4, t, t_update[0], t_update[1], la, lo))
        # conn.commit()

def create_weather_table(cur, conn):
    cur.execute('ALTER TABLE Avg_ISS ADD temp, humidity, windspeed, cloudcover, visibility')
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


 
    
    # select data from Avg_ISS to input into requests
   

def create_daylight_table(cur, conn):
    """make sure to commit new data"""
    pass

def daylight(params):
    #select data from Avg_ISS to input into requests
    pass

# ------------------Monday, Nov 30------------------
# step 1: get access to weather api
# 
# step 2: define function that selects date, time, location from table 1, returns as a nested dictionary
# 
# step 3: input date, time, location (?) into api, write resulting weather into csv file 
# 
# step 4: in a second function, write weather data from file into db table 2 (Weather)

def main():
    
    # pass
    # Database and Tables
    cur, conn = setUpDatabase('API_Data.db')
    # write_iss_csv()
    #create_iss_table(cur, conn)
    #insert_iss_data(cur, conn)
    #create_weather_table(cur, conn)
    create_weather_table(cur, conn)
    #weather(cur, conn)

    # create_daylight_table(cur, conn)
if __name__ == '__main__':
    main()