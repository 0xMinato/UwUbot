from typing import final
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.pages import Paginator, Page, PaginatorMenu
from config import TOKEN
import requests
import json
import math
from bs4 import BeautifulSoup
import re

intents = discord.Intents()
intents.messages = True 
intents.message_content = True
bot = commands.Bot(command_prefix='!',intents=intents)

ses=[]
anime_posters=[]
anime_titles=[]
anime_desc=[]
season_url = 'https://animepahe.com/api?m=release&sort=episode_asc'
total_ep = 0
anime_sess_id = ""
dlink={}
final_anime_link = ""
author = ""

def anime_fun(message):
    global ses, anime_posters, anime_titles, anime_desc, total_ep, anime_sess_id, dlink, final_anime_link
    ses=[]
    anime_posters=[]
    anime_titles=[]
    anime_desc=[]
    total_ep = 0
    anime_sess_id = ""
    dlink={}
    final_anime_link = ""
    anime = ' '.join(message.split()[1:])
    url = 'https://animepahe.com/api?m=search&q='
    author=""
    response = json.loads(requests.get(url+anime).text)
    for dict in response['data']:
        ses.append(dict["session"])
        anime_posters.append(dict["poster"])
        anime_titles.append(dict["title"])
        anime_desc.append("**Episodes: " + str(dict["episodes"])+'\nStatus: '+dict["status"]+'\nYear: '+str(dict["year"])+'\nScore: '+str(dict["score"])+ '**')

def all_episodes(anime_no):
    global total_ep, anime_sess_id
    anime_sess = ses[(int(anime_no)-1)]
    anime_sess_id = "&id=" + anime_sess
    ep_response = json.loads(requests.get(season_url + anime_sess_id).text)
    total_ep = ep_response['total']
    total_pg = math.ceil(total_ep / 30)

def episode_fun(ep_input):
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
    eps_response = json.loads(requests.get(eps_url).text)
    return eps_response

def quality(eps_response):
    dlink = {}
    for eps in eps_response['data']:
        for key in eps:
            dlink[key+eps[key]['audio']] = eps[key]['kwik_pahewin']
    return dlink

def final_link_fun(quality):
    global final_anime_link
    link_response=requests.get(dlink[quality]).text
    soup = BeautifulSoup(link_response,"html.parser")
    soup_find = soup.find('script')
    string = re.search('https://kwik.cx/f/.*"\)\.',str(soup_find))
    final_anime_link = string.group(0).split('"')[0]

class AnimeButton(Button):
    def __init__(self,label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
    async def callback(self, interaction):
        all_episodes(self.label)
        await interaction.response.edit_message(content="Anime selected!" , view=None)
        await interaction.followup.send("**_Select_ Episode _from:_ 1-"+ str(total_ep)+'**')
          
class AnimeView(View):
    def __init__(self,n):
        super().__init__()
        for i in range(1,(n+1)):
            button = AnimeButton(str(i))
            self.add_item(button)

class QualityButton(Button):
    def __init__(self,label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
    async def callback(self, interaction):
        final_link_fun(self.label)
        await interaction.response.edit_message(content="Quality selected!" , view=None)
        await interaction.followup.send("**_Here's your_ Download _link:_**")

class QualityView(View):
    def __init__(self):
        super().__init__()
        for i in dlink:
            button = QualityButton(str(i))
            self.add_item(button)

class UrlButton(Button):
    def __init__(self,final_anime_link):
        super().__init__(label="Watch/Download Anime", style=discord.ButtonStyle.secondary, url=final_anime_link)

class UrlView(View):
    def __init__(self,final_anime_link):
        super().__init__()
        button = UrlButton(final_anime_link)
        self.add_item(button)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")



@bot.command()
async def weeb(ctx):
    anime_fun(ctx.message.content)
    pages = []
    for i in range(len(anime_posters)):
        pages.append(discord.Embed(title=anime_titles[i],description=anime_desc[i]))
        pages[i].set_image(url=anime_posters[i])
        paginator = Paginator(pages=pages,timeout=180.0, author_check=True, disable_on_timeout=True)   
    await paginator.send(ctx=ctx)

    view = AnimeView(len(anime_posters))
    await ctx.send("Select Anime: ",view=view)
    
    def check_episode(m):
        print(m.author)
        if not m.author.bot:
            return (0 < int(m.content) <= total_ep)
    msg = await bot.wait_for('message', check=check_episode)
    #await ctx.edit_message("asfasfaf")
    ep_input = msg.content 

    eps_response = episode_fun(int(ep_input))
    global dlink
    dlink = quality(eps_response)

    view = QualityView()
    await ctx.send("Select Quality: ",view=view)

    global final_anime_link
    def check_final_link(m):
        if m.content == "**_Here's your_ Download _link:_**":
            return final_anime_link
    msg = await bot.wait_for('message', check=check_final_link)
    view = UrlView(final_anime_link)
    await ctx.send("",view=view)

from config import TOKEN
bot.run(TOKEN)
