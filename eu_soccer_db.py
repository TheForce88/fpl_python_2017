# https://www.kaggle.com/ericcouto/exploring-player-stats

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
database = '.../database.sqlite'
conn = sqlite3.connect(database)

query = 'SELECT name FROM sqlite_master WHERE type="table";'
pd.read_sql(query, conn)

# look at the player table
query = "SELECT * FROM Player;"
a = pd.read_sql(query, conn)
a.head()

# look at the player_attributes table
query = "SELECT * FROM Player_Attributes;"
a = pd.read_sql(query, conn)
a.head()

# look at the team_attributes
query = "SELECT * FROM Team_Attributes;"
a = pd.read_sql(query, conn)
a.head()

# join tables
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

players.info()

players = players.fillna(0)
cols = ['player_api_id','player_name','overall_rating','potential']
stats_cols = [col for col in players.columns if col not in (cols)]

ss = StandardScaler()
tmp = ss.fit_transform(players[stats_cols])
model = TSNE(n_components=2, random_state=0)
tsne_comp = model.fit_transform

# can't get this to work
# tmp = players[cols]
# tmp['comp1'], tmp['comp2'] = tsne_comp[:,0], tsne_comp[:,1] #error; TypeError: 'method' object is not subscriptable
# tmp = tmp[tmp.overall_rating >= 80]

# _tools = 'box_zoom,pan,save,resize,reset,tab,wheel_zoom'
# fig = figure(tools=_tools, title='t-SNE of Players (FIFA stats)', responsive=True,
#             x_axis_label='Component 1', y_axis_label='Component 2')

# source = ColumnDataSource(tmp)
# hover = HoverTool
# hover.tooltips=[('Jogador','@player_name'),]
# fig.scatter(tmp['comp1'], tmp['comp2'], source=source, size=8, alpha=0.6, line_color='red'
#            fill_color='red')

# fig.add_tools(hover)

# show(fig)

###

# bell curve of overall_rating
sns.kdeplot(players.overall_rating, shade=True, color='r')

# evolution of players
players = players.sort_values('overall_rating', ascending=False)
best_players = players[['player_api_id','player_name']].head(20)
ids = tuple(best_players.player_api_id.unique())

query = '''SELECT player_api_id, date, overall_rating, potential FROM Player_Attributes WHERE player_api_id in %s''' % (ids,)

evolution = pd.read_sql(query, conn)
evolution = pd.merge(evolution, best_players)
evolution['year'] = evolution.date.str[:4].apply(int)
evolution = evolution.groupby(['year','player_api_id','player_name']).overall_rating.mean()
evolution = evolution.reset_index()
evolution.head()

a = sns.factorplot(data=evolution[evolution.player_api_id.isin(ids[0:5])], x='year',
                   y='overall_rating', hue='player_name', size=6, aspect=2)
print(a)


a = sns.factorplot(data=evolution[evolution.player_api_id.isin(ids[5:10])], x='year',
                   y='overall_rating', hue='player_name', size=6, aspect=2)
print(a)


a = sns.factorplot(data=evolution[evolution.player_api_id.isin(ids[10:15])], x='year',
                   y='overall_rating', hue='player_name', size=6, aspect=2)
print(a)


a = sns.factorplot(data=evolution[evolution.player_api_id.isin(ids[15:20])], x='year',
                   y='overall_rating', hue='player_name', size=6, aspect=2)
print(a)