import requests
import json
import cPickle
import csv

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
errorout = open("errors.log", "w")

for in in range(600):
    playerurl = "https://fantasy.premierleague.com/drf/bootstrap-static"
    r = requests.get(playerurl)
    if r.status_code != 200: continue

    all[i] = r.json()

cPickle.dump(all, outfile)
