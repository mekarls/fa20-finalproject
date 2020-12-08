import unittest
import sqlite3
import json
import os
import plotly
#import plotly.plotly as py
import plotly.graph_objects as go
#import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# def setUpDatabase(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
#     return cur, conn



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
    pass

def conditionsPiechart(cur, conn): #each day needs one

    cur.execute('SELECT Weather.conditions, Time_Zones.time_zone FROM Weather INNER JOIN Time_Zones ON Weather.time_zone = Time_Zones.id')
    data = cur.fetchall() #list of tuples, [0] = condition, [1] = time_zone
    # print(data) 

    d = {}
    for tup in data:
        d[tup[1]] = d.get(tup[1], 0) + 1
    most_common_tz = sorted(d, key=d.get, reverse=True)
    # print(most_common_tz) #paris, toronto, riyadh
    


    # cur.execute("SELECT strftime('%m-%d',ISS_Data.date) FROM ISS_Data WHERE ISS_Data.date LIKE '%12-03%'")
    # # cur.execute('SELECT date FROM ISS_')
    # dec3 = cur.fetchall()
    # index3 = len(dec3)
    
    # data3 = data[:index3]

    paris = {}
    p_count = 0
    toronto = {}
    t_count = 0
    riyadh = {}
    r_count = 0
 
    for i in data:
        if i[1] == 'Europe/Paris':
            paris[i[0]] = paris.get(i[0], 0) + 1
            p_count += 1
        if i[1] == 'America/Toronto':
            toronto[i[0]] = toronto.get(i[0], 0) + 1
            t_count += 1
        if i[1] == 'Asia/Riyadh':
            riyadh[i[0]] = riyadh.get(i[0], 0) + 1
            r_count += 1
        
    # print(paris)
    # print(toronto)
    # print(riyadh)


    # --------------------- PARIS ---------------------
    paris_s = []
    paris_c = []
    
    for i in paris.items():
        paris_c.append(i[0])
        
        i = i[1]/p_count * 100
        i_dec = "{:.2f}".format(i)
        paris_s.append(float(i_dec))

        
    
    # print(paris_s)
    # print(paris_c)

    colors = ['PaleGreen', 'CornflowerBlue', 'DeepPink']
    explode = (0, 0, 0.25)  # explode 1st slice
  

# Plot
    patches = plt.pie(paris_s, colors=colors, autopct='%1.1f%%', shadow=True, startangle=155, explode=explode)
    # plt.tight_layout()
    plt.legend(patches, labels=paris_c)
    plt.axis('equal')
    plt.title('Weather Conditions in Paris')
    plt.show()
    



def dewpointVShumidity(cur, conn): #3 axis line chart
    pass

def main():
    # cur, conn = setUpDatabase('API_Data.db')
    conn = sqlite3.connect('API_Data.db')
    cur = conn.cursor()
    conditionsPiechart(cur, conn)
#      print('--------get time----------')
#      # print(get_one_ISS_Data(cur, conn))
#      print('--------get plot of date and time--------')
#      print(graph_data(cur, conn))
    


if __name__ == "__main__":
    main()
# graph_data()
#read_from_db()

# cur.close()
# conn.close()