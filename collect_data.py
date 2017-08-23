import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import lxml

player_dict = {}

# url = 'https://www.dreamteamfc.com/statistics/players/ALL/'
# url = 'https://www.premierleague.com/players'
url = 'http://www.futhead.com/17/players/?bin_platform=ps&league=13&club=all'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

name_list = []

for td in soup.findAll("td", {"class" : "tabName"}):
    name = td.text.split('Statistics')[-1].strip()
    if name:
        name_list.append(name)
        res = [i.text for i in td.next_siblings if isinstance(i, bs4.element.Tag)]
        position, team, vfm, value, points = res
        value = value.strip('m')
        player_dict[name] = [name, position, team, vfm, value, points]
print('Found: %s' % len(name_list))
print(name_list[-1])