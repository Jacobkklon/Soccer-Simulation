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


# data = []
# for row in player_rows:
#     row_data = []
#     for cell in row.find_all('td'):
#         row_data.append(cell.text)
#     data.append(row_data)

#I'm going to try the method of reading data using the 'data-stat' label, which has a length of 9
#print(player_rows)

rawd = str(player_rows)
colname = "" #Name of each column
colnames = [] #Name of the stat we are looking at
name_ind = 0 #Index that the colname starts at
colmode = False #This indicates we are looking for columns

#NOTE - to use quotes in a string you must use \"
for i in range(10,len(rawd)): #Starting at 10 to avoid index issues
    
    if rawd[i-9:i] == "data-stat":

        name_ind = i + 2
        colmode = True

    
    elif colmode == True and i >= name_ind: #If we are in column-name finding mode and the column name is present
        
        colname += (rawd[i]) #Appending next char
        if rawd[i + 1] == "\"": #A quote char indicates data-stat value is done
            
            colmode = False
            colnames.append(colname)
            colname = ""

print(colnames)

        
        

    


        

        

    
        



 



#The next step is to use the fact that "data-stat" goes in front of any statistic and then the number to extract
#all the data into a pandas DF 

