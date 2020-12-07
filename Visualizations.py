import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


# def setUpDatabase(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
#     return cur, conn

conn = sqlite3.connect('API_Data.db')
cur = conn.cursor()

# def get_one_ISS_Data(cur, conn):
#     cur.execute("SELECT ISS_Data.time FROM ISS_Data",)
#     time_result = cur.fetchall()
#     return (time_result)

#def read_from_db():
#    cur.execute("SELECT strftime('%m-%d',ISS_Data.date), ISS_Data.time FROM ISS_Data",)
    #cur.execute("SELECT ISS_Data.date, ISS_Data.time FROM ISS_Data",)
#    for row in cur.fetchall():
#        print(row)
    #data = cur.fetchall()
    #print(data)



# def graph_data(cur, conn):
#     cur.execute("SELECT strftime('%m-%d',ISS_Data.date), strftime('%H:%M', ISS_Data.time) FROM ISS_Data",)
#     data = cur.fetchall()


#     dates = []
#     values = []

    
#     for row in data:
#         dates.append(row[0])
#         values.append(row[1])

#     print(dates)
#     print(values)
#     plt.plot_date(dates,values, '-')
#     plt.show()
    
#     #print(dates)
#     #print(values)

def daylengthVSmaxtemp(cur, conn): #include join

def conditionsPiechart(cur, conn): #each day needs one

def dewpointVShumidity(cur, conn): #3 axis line chart


# def main():
#      # cur, conn = setUpDatabase('API_Data.db')
#      print('--------get time----------')
#      # print(get_one_ISS_Data(cur, conn))
#      print('--------get plot of date and time--------')
#      print(graph_data(cur, conn))
    


# if __name__ == "__main__":
#     main
graph_data()
#read_from_db()
cur.close()
conn.close()