import unittest
import sqlite3
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def daylengthVSmaxtemp(cur, conn): #include join
    cur.execute('SELECT day_length FROM Daylight')
    daylength1 = cur.fetchall()
    daylight2 = []
    for x in daylength1:
        daylight2.append(x[0])

    cur.execute('SELECT max_temp FROM Weather')
    maxtemps = cur.fetchall()
    maxtemps2 = []
    for x in maxtemps:
        maxtemps2.append(x[0])

    # Create data
    colors = ['red']
    area = np.pi*3

    # Plot
    plt.scatter(daylight2, maxtemps2, s=area, c=colors, alpha=0.5)
    plt.title('Scatter Plot of Daylength VS Maximum Temperature')
    plt.xlabel('Amount of Daylight (Hours:Minutes:Seconds)')
    plt.ylabel('Maximum Temperature (Farenheit)')
    # plt.show()
    
def conditionsPiechart(cur, conn): #each timezone needs a chart

    # '''   PART 3 – Process the data (50 points)
# ● You must select some data from all of the tables in your database and calculate
# something from that data (20 points). You could calculate the count of how many items
# occur on a particular day of the week or the average of the number of items per day.
# ● You must do at least one database join to select your data (20 points).
# ● Write out the calculated data to a file as text (10 points) '''

# create calculation csv file
    with open('percentages.csv', 'w') as f:
        header = 'time_zone, overcast, clear, partially cloudy\n'
        f.write(header)

        cur.execute('SELECT Weather.conditions, Time_Zones.time_zone FROM Weather INNER JOIN Time_Zones ON Weather.time_zone = Time_Zones.id')
        data = cur.fetchall() #list of tuples, [0] = condition, [1] = time_zone
        # print(data) 

        d = {}
        for tup in data:
            d[tup[1]] = d.get(tup[1], 0) + 1
        most_common_tz = sorted(d, key=d.get, reverse=True)
        # print(most_common_tz) #paris, toronto, riyadh
        
        #above functions were used to find the most frequently found timezones in our data
        #below functions were used to plot the three pie charts 
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
            
        #print(paris)
        #print(toronto)
        #print(riyadh)

        # --------------------- PARIS ---------------------
        
        paris_s = []
        paris_c = []
        
        for i in paris.items():
            paris_c.append(i[0])
            
            i = i[1]/p_count * 100
            i_dec = "{:.2f}".format(i)
            paris_s.append(float(i_dec))
                
        #print(paris_s)
        #print(paris_c)

        colors = ['PaleGreen', 'CornflowerBlue', 'DeepPink']
        explode = (0, 0, 0.25)  # explode 1st slice
    
    # Plot
        patches = plt.pie(paris_s, colors=colors, autopct='%1.1f%%', shadow=True, startangle=155, explode=explode)
        plt.tight_layout()
        plt.legend(patches, labels=paris_c)
        plt.axis('equal')
        plt.title('Weather Conditions in Paris')
        plt.show()
        
         # insert into csv
        
        ind = 0
        while len(paris_s) != 3:
            paris_s.append(0.00)

        f.write(f'paris, {paris_s[0]}, {paris_s[1]}, {paris_s[2]}\n')

        # ----------------------Toronto-----------------------------
        
        toronto_s = []
        toronto_c = []
       
        for i in toronto.items():
            toronto_c.append(i[0])

            i = i[1]/t_count * 100
            i_dec = "{:.2f}".format(i)
            toronto_s.append(float(i_dec))
       
        # print(toronto_c)
        # print(toronto_s)

        colors = ['CornflowerBlue', 'DeepPink']
        explode = (0, 0.1)  # explode 1st slice

        patches = plt.pie(toronto_s, colors=colors, autopct='%1.1f%%', shadow=True, startangle=155, explode=explode)
        plt.tight_layout()
        plt.legend(patches, labels=toronto_c)
        plt.axis('equal')
        plt.title('Weather Conditions in Toronto')
        plt.show()

         # insert into csv
        
        ind = 0
        while len(toronto_s) != 3:
            toronto_s.append(0.00)

        f.write(f'toronto, {toronto_s[0]}, {toronto_s[1]}, {toronto_s[2]}\n')

        #-----------------------Riyadh----------------------

        riyadh_s = []
        riyadh_c = []
        
        for i in riyadh.items():
            riyadh_c.append(i[0])
            
            i = i[1]/r_count * 100
            i_dec = "{:.2f}".format(i)
            riyadh_s.append(float(i_dec))

        #print(riyadh_c)
        #print(riyadh_s)
        colors = ['DeepPink']
        #explode = (0,)  # explode 1st slice

        patches = plt.pie(riyadh_s, colors=colors, autopct='%1.1f%%', shadow=True, startangle=155)
        plt.tight_layout()
        plt.legend(patches, labels=riyadh_c)
        plt.axis('equal')
        plt.title('Weather Conditions in Riyadh')
        plt.show()

         # insert into csv
        
        ind = 0
        while len(riyadh_s) != 3:
            riyadh_s.append(0.00)

        f.write(f'riyadh, {riyadh_s[0]}, {riyadh_s[1]}, {riyadh_s[2]}')
        f.close()

def dewpointVShumidity(cur, conn): #3 axis line chart
    cur.execute("SELECT dew FROM Weather")
    dew = cur.fetchall()
    dewpoint = []
    for x in dew:
        dewpoint.append(x[0])
    
    data = list(range(103))
    data = data[1:103]


    cur.execute("SELECT humidity FROM Weather")
    humid = cur.fetchall()
    humidity = []
    for x in humid:
        humidity.append(x[0])

    fig, ax = plt.subplots()
 
    ax.plot(data,dewpoint)
    ax.plot(data,humidity)
    ax.set_title('Line Graph of Dewpoint VS Humidity')
    ax.set_xlabel('International Space Station Location ID')
    ax.set_ylabel('Dewpoint')

    secaxy = ax.secondary_yaxis('right')
    secaxy.set_ylabel(r'Humidity')
    ax.legend(['Dewpoint','Humidity'])

    # plt.show()
    
    
def main():
    conn = sqlite3.connect('API_Data.db')
    cur = conn.cursor()
    # conditionsPiechart(cur, conn)
    # daylengthVSmaxtemp(cur, conn)
    # dewpointVShumidity(cur, conn)




if __name__ == "__main__":
    main()
