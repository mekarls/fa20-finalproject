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
    cur.execute('''DROP TABLE IF EXISTS 'ISS_Data_1'''')
    cur.execute('''CREATE TABLE 'ISS_Data_1' 
    ('unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')
    
    cur.execute('''DROP TABLE IF EXISTS 'ISS_Data_2'''')
    cur.execute('''CREATE TABLE 'ISS_Data_2' 
    ('unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    cur.execute('''DROP TABLE IF EXISTS 'ISS_Data_3'''')
    cur.execute('''CREATE TABLE 'ISS_Data_3' 
    ('unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    cur.execute('''DROP TABLE IF EXISTS 'ISS_Data_4'''')
    cur.execute('''CREATE TABLE  'ISS_Data_4' 
    ('unix' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

def insert_iss_data(cur, conn):    
    with open('iss_pos.csv', 'r') as fhand:
    #with open('iss_pos2.csv', 'r') as fhand:
    #with open('iss_pos3.csv', 'r') as fhand:
    # with open('iss_pos4.csv', 'r') as fhand:
    
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

            cur.execute('INSERT INTO ISS_Data_1 (unix, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            #cur.execute('INSERT INTO ISS_Data_2 (unix, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            #cur.execute('INSERT INTO ISS_Data_3 (unix, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            # cur.execute('INSERT INTO ISS_Data_4 (unix, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            conn.commit()

        t = sum(times)/float(len(times))
        t_update = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S') #returns date, time
        la = round(sum(lats)/float(len(lats)), 4)
        lo = round(sum(longs)/float(len(longs)), 4)
        
        cur.execute('''CREATE TABLE IF NOT EXISTS 'Avg_ISS'
        (id INTEGER PRIMARY KEY, avg_unix NUMBER, date TEXT, time TEXT, avg_lat NUMBER, avg_long NUMBER)''')

        cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (1, t, t_update[0], t_update[1], la, lo))
        #cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (2, t, t_update[0], t_update[1], la, lo))
        #cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (3, t, t_update[0], t_update[1], la, lo))
        # cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (4, t, t_update[0], t_update[1], la, lo))
        conn.commit()
     
# def time_converstion(cur, conn):
#     cur.execute('SELECT avg_time FROM Avg_ISS')
#     times = cur.fetchall()
#     update_times = []
#     t = [''.join(str(time)) for time in times]
#     tim = [ti.strip('(),') for ti in t]
#     print(tim)
    # update_times = [datetime.utcfromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S') for ts in tim]
    # for time in update_times:
    #     time = time.split()
    #     d = time[0]
    #     t = time[1]
        # cur.execute('ALTER TABLE Avg_ISS ADD date TEXT')
        # cur.execute('ALTER TABLE Avg_ISS ADD time TEXT')
        # cur.execute('''UPDATE Avg_ISS SET 
        # date = d
        # time = t
        # FROM Avg_ISS
        # WHERE id = 1''')
        # conn.commit()
    pass

def create_weather_table(cur, conn):
    """make sure to commit new data"""
    pass

def weather(params):
    # api_key = '97H6P669AZU5PIG16JBC5N4ES'
    # base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/history/'
    # [location]/[date1]/[date2]?key=YOUR_API_KEY 
    # req = requests.get(base_url, )
    #[key]/[latitude],[longitude],[time]'
    # select data from Avg_ISS to input into requests
    pass

def create_daylight_table(cur, conn):
    """make sure to commit new data"""
    pass

def daylight(params):
    #select data from Avg_ISS to input into requests
    pass

# ------------------WEDNESDAY, NOV 25------------------
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
    # create_iss_table(cur, conn)
    # insert_iss_data(cur, conn)
    # create_weather_table(cur, conn)

    # create_daylight_table(cur, conn)
if __name__ == '__main__':
    main()