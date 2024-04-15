import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import sys, getopt
import csv
import mysql.connector
from sqlalchemy import create_engine

res = requests.get('https://fbref.com/en/comps/9/stats/Premier-League-Stats')

## The next two lines get around the issue with comments breaking the parsing.
comm = re.compile("<!--|-->")
soup = BeautifulSoup(comm.sub("",res.text),'lxml')

all_tables = soup.findAll("tbody")
team_table = all_tables[0]
player_table = all_tables[2]

pre_df_squad = dict()
features_wanted_squad = {"players_used","games"}

player_rows = player_table.find_all('tr')
rawd = str(player_rows)




colname = "" #Name of each column
colnames = [] #Name of the stat we are looking at
name_ind = 0 #Index that the colname starts at
colmode = False #This indicates we are looking for columns
statmode = False #This indicates that the column name has passed and we are going to see the stat soon in between >...<
stat = "" #This preallocates the stat we have (it's part of a big string)
stat_list = [] #Creating an empty list of player data, I'm going to create another loop after to read in stuff clearly
triangle_finder = False #Triangle finder is used to find when the ">........ part happens with the quote and triangle


#NOTE - to use quotes in a string you must use \"
for i in range(10,len(rawd)): #Starting at 10 to avoid index issues
    
    if rawd[i-9:i] == "data-stat":

        name_ind = i + 2
        colmode = True

    
    elif colmode == True and i >= name_ind: #If we are in column-name finding mode and the column name is what we are reading through
        
        colname += (rawd[i]) #Appending next char
        if rawd[i + 1] == "\"": #A quote char indicates data-stat value is done
            
            colmode = False
            statmode = True
            colnames.append(colname)
            colname = ""
    elif statmode == True and i >= name_ind and rawd[i-1:i+1] == "\">": #Any stat has "> in front
        triangle_finder = True
    elif statmode == True and i >= name_ind and triangle_finder == True: #bc entries go ">50< then we can directly used the name_ind to help

        stat += rawd[i] #Adding to send of string

        if rawd[i + 1] == "<": #This means we are at the final value before the end of the stat
            
            statmode = False
            triangle_finder = False
            stat_list.append(stat) #Add the stat to the end of the player list
            stat = "" #Reset stat value
    

        
#Writing to CSV to spot-check data quality
minl = min(len(colnames), len(stat_list))
title_stat_df = pd.DataFrame({'colnames': colnames[:minl], 'stat_list': stat_list[:minl]}) 
# title_stat_df.to_csv('out.csv')

coltitles = [] #Empty list representing headers of new df

#First I will loop through and add the column headers
for i in range(len(title_stat_df.index)):
    if title_stat_df.iloc[i,0] == 'ranker' and i > 1:
        break
    else:
        coltitles.append(title_stat_df.iloc[i,0])


#Given that I have 2 columns in a df (title_stat_df) the next step is to read it into a stat-df with the right format
#General idea: Loop through all the rows, know when to stop and append the new row
newrow = [] #This will be used to represent each new row added
stat_df = pd.DataFrame(columns = coltitles) #Final DF with stats


for i in range(len(title_stat_df.index)): #i goes through all the ROWS
    #Ranker is the first column name, so we will use it to increment
    #Col 0 is the title name, Col 1 is the stat
    if title_stat_df.iloc[i,0] == 'ranker' and i > 2:
        stat_df.loc[len(stat_df.index)] = newrow
        newrow = []
    
    # newrow.update({title_stat_df.iloc[i,0] : title_stat_df.iloc[i,1]})
    newrow.append(title_stat_df.iloc[i,1])

stat_df.to_csv('statdf.csv') #Writing finalized df with player stats to csv (I have looked at the csv and confirmed it's good!)

#Next steps - writing df to DB and doing SQL for some automated cleaning, applying ML, and then hosting it on RESTFUL API on AWS

#Connecting to the DB
mydb = mysql.connector.connect(
    host = "rds-mysql-soccer-project.cnuykwkwidxt.us-east-1.rds.amazonaws.com",
    user = "admin",
    password = "JacobKlonsky",
    database="RDS_MySQL_Soccer_Project")

#Creating the DB table
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE player_stats (ranker VARCHAR(255), player VARCHAR(255), nationality VARCHAR(255), position VARCHAR(255), team VARCHAR(255), 
                 team VARCHAR(255), age VARCHAR(255), birth_year DATE, games CHAR(3), games_starts CHAR(3), minutes CHAR(6), minutes_90s CHAR(5),
                 goals CHAR(2), assists CHAR(2), goal_assists CHAR(2), goals_pens CHAR(2), pens_made CHAR(2),
                 pens_att CHAR(2), cards_yellow CHAR(2), cards_red CHAR(2), xg CHAR(4), npxg CHAR(4), xg_assist CHAR(4),
                 npxg_xg_assist CHAR(4), progressive_carries CHAR(4), progressive_passes CHAR(4), 
                 progressive_passes_received CHAR(4), goals_per90 CHAR(3), assists_per90 CHAR(3), 
                 goal_assists_per90 CHAR(4), goal_pens_per90 CHAR(4), goal_assists_pens_per90 CHAR(4), xg_per90 CHAR(3),
                 xg_assist_per90 CHAR(3), xg_xg_assist_per90 CHAR(3), npxg_per90 CHAR(4), 
                 npxg_xg_assist_per90 CHAR(4), matches VARCHAR(255)) """)

# #Writing the CSV to DB
# with open('statdf.csv', 'r') as f:
#     reader = csv.reader(f)
#     columns = next(reader) 
#     query = 'insert into MyTable({0}) values ({1})'
#     query = query.format(','.join(columns), ','.join('?' * len(columns)))
#     cursor = connection.cursor()
#     for data in reader:
#         cursor.execute(query, data)
#     cursor.commit()

print('hi')