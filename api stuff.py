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

print(player_table)

#The next step is to use the fact that "data-stat" goes in front of any statistic and then the number to extract
#all the data into a pandas DF 

