import pandas as pd
import numpy as np
import sqlite3
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.models import HoverTool
from bokeh.io import output_notebook
import matplotlib.pyplot as plt
import seaborn as sns

# enter your own file path
# database = '.../database.sqlite'
conn = sqlite3.connect(database)


# player table
query = """SELECT * FROM Player_Attributes a
        INNER JOIN (SELECT player_name, player_api_id AS p_id FROM Player)
        b ON a.player_api_id = b.p_id;"""
drop_cols = ['id','player_fifa_api_id','date','preferred_foot','attacking_work_rate','defensive_work_rate']

players = pd.read_sql(query, conn)
players['date'] = pd.to_datetime(players['date'])
players = players[players.date > pd.datetime(2016,1,1)]
players = players[~players.overall_rating.isnull()].sort_values('date', ascending=False)
players = players.drop_duplicates(subset='player_api_id', keep='first')
players = players.drop(drop_cols, axis=1)


# league table
query = "SELECT * FROM League;"
league = pd.read_sql(query, conn)
league.head()



# scraping data from website (need league, team, and position for each player)
import requests
from bs4 import BeautifulSoup

# get html
# soup 1
content1 = requests.get("http://www.futhead.com/17/players/?bin_platform=ps&league=13&club=all").content
# pass html to beautifulSoup
soup1 = BeautifulSoup(content1, "lxml")


fifa_players = soup1.find_all("span", class_="player-name")
fifa_league = soup1.find_all("span", class_="player-club-league-name")

# create and clean data frames
df = pd.DataFrame(fifa_players)
df.columns = ['name']
df['name'] = df['name'].astype('str')
df['name'] = df['name'].map(lambda x: x.lstrip('<span class="player-name">'))
df['name'] = df['name'].astype('str')
df['name'] = df['name'].map(lambda x: x.lstrip('</span>')) # this isn't removing the string

# ideally, we could create all the tables then combine before cleaning--I just need to see that the cleaning method
# works first

# soup 2
content2 = requests.get("http://www.futhead.com/17/players/?bin_platform=ps&league=13&club=all").content
# pass html to beautifulSoup
soup2 = BeautifulSoup(content1, "lxml")

fifa_players2 = soup2.find_all("span", class_="player-name")
fifa_league2 = soup2.find_all("span", class_="player-club-league-name")