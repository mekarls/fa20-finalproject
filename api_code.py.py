# SI 206 Final Project - STE(a)Migos
# Names: Michelle Karls, Selin Fidan, Julia Couch

import requests
import json
import os
import unittest
import sqlite3

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
    time = data['timestamp']
    lat = data['iss_position']['latitude']
    long = data['iss_position']['longitude']
    # return {"time": time, "lat": lat, "long": long}
    return f'{time},{lat},{long}'

# step 3: write iss_data to csv file

def write_iss_csv():
    header = 'time,latitude,longitude'
    # f = open('iss_pos.csv', 'w')
    f = open('iss_pos2.csv', 'w')
    # f = open('iss_pos3.csv', 'w')
    # f = open('iss_pos4.csv', 'w')
    f.write(header+'\n')
    f.close()
    for _ in range(25):
        iss_data = iss_position()
        # f = open('iss_pos.csv', 'a')
        f = open('iss_pos2.csv', 'a')
        # f = open('iss_pos3.csv', 'a')
        # f = open('iss_pos4.csv', 'a')
        f.write(iss_data+'\n')
        f.close() 

# step 4: read csv file into database

def create_iss_table(cur, conn):
    """make sure to commit new data"""
    # cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_1' 
    # ('timestamp' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_2' 
    ('timestamp' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    # cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_3' 
    # ('timestamp' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

    # cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_4' 
    # ('timestamp' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')

def insert_iss_data(cur, conn):    
    # with open('iss_pos.csv', 'r') as fhand:
    with open('iss_pos2.csv', 'r') as fhand:
    # with open('iss_pos3.csv', 'r') as fhand:
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

            # cur.execute('INSERT INTO ISS_Data_1 (timestamp, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            cur.execute('INSERT INTO ISS_Data_2 (timestamp, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            # cur.execute('INSERT INTO ISS_Data_3 (timestamp, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            # cur.execute('INSERT INTO ISS_Data_4 (timestamp, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            conn.commit()

        t = sum(times)/float(len(times))
        la = round(sum(lats)/float(len(lats)), 4)
        lo = round(sum(longs)/float(len(longs)), 4)
        
        cur.execute('''CREATE TABLE IF NOT EXISTS 'Avg_ISS'
        (id INTEGER PRIMARY KEY, avg_time NUMBER, avg_lat NUMBER, avg_long NUMBER)''')

        # cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (1, t, la, lo))
        cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (2, t, la, lo))
        # cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (3, t, la, lo))
        # cur.execute('INSERT INTO Avg_ISS (id, avg_time, avg_lat, avg_long) VALUES (?, ?, ?, ?)', (4, t, la, lo))
        conn.commit()
     

def create_weather_table(cur, conn):
    """make sure to commit new data"""
    pass

def weather(params):
    # api_key = '1bc5438768mshc8ba727986a1b1ap18522ejsnd016edc7cb65'
    # base_url = 'https://api.darksky.net/forecast/'
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
    create_iss_table(cur, conn)
    insert_iss_data(cur, conn)
    
    # create_weather_table(cur, conn)

    # create_daylight_table(cur, conn)
if __name__ == '__main__':
    main()