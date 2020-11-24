# SI 206 Final Project - STE(a)Migos
# Names: Michelle Karls, Selin Fidan, Julia Couch


import requests
import json
import os
import unittest

# ------------------TUESDAY, NOV 24------------------
# step 1: get access to _ api

# step 2: define function to request from api
def iss_position():
    base_url = 'http://api.open-notify.org/iss-now.json'
    req = requests.get(base_url)
    data = req.json()
    time = data['timestamp']
    lat = data['iss_position']['latitude']
    long = data['iss_position']['longitude']
    return (time, lat, long)
# step 3: in same function, save _ data to a csv file 
print(iss_position())
# step 4: create database (database name: API Data)
# 
# step 5: in a second function, write data from file into db table 1 (_)


# ------------------WEDNESDAY, NOV 25------------------
# step 1: get access to weather api
# 
# step 2: define function that selects date, time, location from table 1, returns as a nested dictionary
# 
# step 3: input date, time, location (?) into api, write resulting weather into csv file 
# 
# step 4: in a second function, write weather data from file into db table 2 (Weather)

