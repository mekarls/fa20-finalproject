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
    f = open('iss_pos.csv', 'w')
    f.write(header+'\n')
    f.close()
    for _ in range(25):
        iss_data = iss_position()
        f = open('iss_pos.csv', 'a')
        f.write(iss_data+'\n')
        f.close()
# write_iss_csv() 

# step 4: read csv file into database

def create_iss_table(cur, conn):
    """make sure to commit new data"""
    cur.execute('''CREATE TABLE IF NOT EXISTS 'ISS_Data_1' 
    ('timestamp' TEXT, 'latitude' TEXT, 'longitude' TEXT)''')
    
def insert_iss_data(cur, conn):    
    with open('iss_pos.csv', 'r') as fhand:
        lines = fhand.readlines()
        for line in lines[1:]:
            line = line.strip().split(',')
            time = line[0]
            lat = line[1]
            long = line[2]
            # print(type(time), type(lat), type(long))
            cur.execute('INSERT INTO ISS_Data_1 (timestamp, latitude, longitude) VALUES (?, ?, ?)', (time, lat, long))
            conn.commit()
    # conn.close()
    # pass

# for x in range(1,26):
#     issdata[x]= iss_position()
# print(issdata, len(issdata))
# for x in range(26,51):
#     issdata[x] = iss_position()
# print(issdata, len(issdata))
# for x in range(51,76):
#     issdata[x] = iss_position()
# print(issdata, len(issdata))

# def iss_csv_file():
#     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "isspos.csv"), 'w') as f:
#         for x in issdata:
#             f.write(x + "\n")


def create_weather_table(cur, conn):
    """make sure to commit new data"""
    pass

def weather(params):
    pass

def create_daylight_table(cur, conn):
    """make sure to commit new data"""
    pass

def daylight(params):
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

    create_iss_table(cur, conn)
    insert_iss_data(cur, conn)
    
    # create_weather_table(cur, conn)

    # create_daylight_table(cur, conn)
if __name__ == '__main__':
    main()