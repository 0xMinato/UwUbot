import requests
import json
import math
from bs4 import BeautifulSoup
import re

anime = input("Enter anime name: ")
url = 'https://animepahe.com/api?m=search&q='
response = requests.get(url+anime).text
json_response = json.loads(response)
j=1
ses=[]
for dict in json_response['data']:
    print('#'+str(j),end=' ')
    j+=1
    ses.append(dict["session"])
    for key in dict:
        if key in ['episodes','title','status','year']:
            print(key.capitalize()+":" + str(dict[key]), end=', ')
        if key == "score":
            print(key.capitalize()+":" + str(dict[key]), end=' ')
    print()
num = int(input("Enter choice: "))
anime_sess = ses[num-1]

season_url = 'https://animepahe.com/api?m=release&sort=episode_asc'
anime_sess_id = "&id=" + anime_sess
ep_response = requests.get(season_url + anime_sess_id).text
json_ep = json.loads(ep_response)
total_ep = json_ep['total']
total_pg = math.ceil(total_ep / 30)

print("\nEpisodes: 1-" + str(total_ep))
ep_input = int(input("Enter episode no.: "))
pg = math.ceil(ep_input/30)
pg_response = requests.get(season_url + anime_sess_id + "&page="+str(pg)).text
pg_response = json.loads(pg_response)

ep_ses=[]
for ep in pg_response['data']:
    ep_ses.append(ep['session'])
ep_input = ep_input%30
ep_sessid = ep_ses[ep_input-1]

eps_url= 'https://animepahe.com/api?m=links&id='
eps_url = eps_url + ep_sessid
eps_response = requests.get(eps_url).text
json_eps = json.loads(eps_response)

quality = int(input("\nQuality available:\n1. 720p\n2. 1080p\nChoice: "))
quality -= 1
dlink = []
for eps in json_eps['data']:
    for key in eps:
        for key2 in eps[key]:
            if key2 in ['kwik_pahewin']:
                dlink.append(eps[key][key2])

link_response=requests.get(dlink[quality]).text
soup = BeautifulSoup(link_response,"html.parser")
soup_find = soup.find('script')
str = re.search('https://kwik.cx/f/.*"\)\.',str(soup_find))
final_link = str.group(0).split('"')[0]
print("\nHere's the link:")
print(final_link)