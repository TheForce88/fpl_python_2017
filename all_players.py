import requests
import json
import _pickle as cPickle
import csv

import requests, shutil, time

FPL_URL = "https://fantasy.premierleague.com/drf/"
USER_SUMMARY_SUBURL = "element-summary/"
LEAGUE_STANDING_SUBURL = "leagues-classic-standings/"
TEAM_ENTRY_SUBURL = "entry/"
GW_NUMBER = 1
EVENT_SUBURL = "event/" + str(GW_NUMBER) + "/picks"
USER_SUMMARY_URL = FPL_URL + USER_SUMMARY_SUBURL
LEAGUE_STANDING_URL = FPL_URL + LEAGUE_STANDING_SUBURL
ID_TEST = 1

yala_on_scasse_league_id = 336217
reddit_pl_url = 1459
test_entry_id = 2677936


def getUserEntryIds(league_id, ls_page):
    league_url = LEAGUE_STANDING_URL + str(league_id) + "?phase=1&1e-page=1&ls-page=" + str(ls_page)
    r = requests.get(league_url)
    jsonResponse = r.json()
    standings = jsonResponse["standings"]["results"]
    if not standings:
        pring("no more standings found")
        return None

    entries = []

    for player in standings:
        entries.append(player["entry"])

    return entries

# get fpl data from site, load it as json file
fpl_api = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static')
fpl_players = fpl_api.json()
with open('fpl_api.json', 'w') as f:
    json.dump(fpl_players, f)

######

# Choosing a fantasy football team
all = {}
outfile = open("players.data.pickle", "w")
errorout = open("errors.log", "w")

for i in range(600):
    playerurl = "https://fantasy.premierleague.com/drf/bootstrap-static"
    r = requests.get(playerurl)

    # skip non-existent players
    if r.status_code != 200: continue

    try:
        all[i] = r.json()
    except ValueError:
        continue
# error: TypeError: 'builtin_function_or_method' object does not support item assignment


outfile = open('data.p', 'wb')
cPickle.dump(all, outfile)
outfile.close()

