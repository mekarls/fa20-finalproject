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

    cur.execute("SELECT strftime('%m-%d',ISS_Data.date) FROM ISS_Data WHERE ISS_Data.date LIKE '%12-03%'")
    # cur.execute('SELECT date FROM ISS_')
    dec3 = cur.fetchall()
    index3 = len(dec3)
    
    data3 = data[:index3]

    cond3 = []
    timezone3 = []

    for day in data3:
        cond3.append(day[0])
        timezone3.append(day[1])


    labels = np.array((timezone3))
    sizes = np.array((cond3))
    #colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    #explode = (0.1, 0, 0, 0)  # explode 1st slice
 
# Plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
 
    plt.axis('equal')
    plt.show()
    #labels = ['Overcast','Clear','Partially_Cloudy']
    #values = ['Asia/Dushanbe', 'Asia/Kathmandu', 'Europe/London', 'Etc/GMT', 'Europe/Paris', 'Europe/Zurich', 'Europe/Rome', 'Etc/GMT-1', 'Europe/Zagreb', 'Europe/Athens', 'Asia/Riyadh', 'Africa/Brazaville', 'Africa/Douala', 'America/Detroit', 'America/Toronto']
    #labels = (cond3)
    #values = (timezone3)
    
    #color_list = ['CornflowerBlue', 'YellowGreen', 'Orange', 'Yellow', 'Coral', 'Palegreen', 'Midnightblue', 'Slateblue', 'Royalblue', 'Mediumpurple', 'Violet', 'Deeppink', 'Crimson', 'Pink', 'Hotpink']

    #fig = go.Figure(data=[go.Pie(values=values, labels=labels)])
    #fig.update_traces(hoverinfo='label+value', textfont_size=10, marker=dict(colors=color_list))
    #df1 = px.cond3
    #df2 = px.timezone3
    #fig = px.pie(df1, df2, values='condition', labels='timezone')
    #fig.show()    
    #labels = list(cond3)
    #values = list(timezone3)
    #df = px.cond3.timezone3()
    #fig = px.pie(df, values='timezone', names='weather condition')
    #fig.show()
    
    #print(labels)
    #print(values)

    cur.execute("SELECT strftime('%m-%d',ISS_Data.date) FROM ISS_Data WHERE ISS_Data.date LIKE '%12-04%'")
    dec4 = cur.fetchall()
    index4 = index3 + len(dec4)
    
    data4 = data[index3:index4]
    # print(len(data4))

    cond4 = []
    timezone4 = []

    for day in data4:
        cond4.append(day[0])
        timezone4.append(day[1])

    #print(cond4)
    #print(timezone4)

    cur.execute("SELECT strftime('%m-%d',ISS_Data.date) FROM ISS_Data WHERE ISS_Data.date LIKE '%12-05%'")
    dec5 = cur.fetchall()
    index5 = index4 + len(dec5)

    data5 = data[index4:index5]
    
    cond5 = []
    timezone5 = []

    for day in data5:
        cond5.append(day[0])
        timezone5.append(day[1])

    #print(cond5)
    #print(timezone5)

    cur.execute("SELECT strftime('%m-%d',ISS_Data.date) FROM ISS_Data WHERE ISS_Data.date LIKE '%12-06%'")
    dec6 = cur.fetchall()
    index6 = index5 + len(dec6)
    # print(index6)

    data6 = data[index5:index6]
    
    cond6 = []
    timezone6 = []

    for day in data6:
        cond6.append(day[0])
        timezone6.append(day[1])

    #print(cond6)
    #print(timezone6)

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