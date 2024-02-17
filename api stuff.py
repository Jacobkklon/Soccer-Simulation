import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import sys, getopt
import csv

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
    elif statmode == True and i >= name_ind and rawd[i] != ">": #bc entries go ">50< then we can directly used the name_ind to help

        stat += rawd[i] #Adding to send of string

        if rawd[i + 1] == "<": #This means we are at the final value before the end of the stat
            
            statmode = False
            stat_list.append(stat) #Add the stat to the end of the player list
            stat = "" #Reset stat value
        
#Writing Excel to spot-check data quality
minl = min(len(colnames), len(stat_list))
output = pd.DataFrame(colnames[:minl], stat_list[:minl])
output.to_csv('out.csv')


        

    


        

        

    
        



 



#The next step is to use the fact that "data-stat" goes in front of any statistic and then the number to extract
#all the data into a pandas DF 

