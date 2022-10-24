# UwUbot
UwUbot provides you any anime you wish for in just a couple of button clicks.

### How this bot works?
- UwUbot makes use of PyCord for it's pages, button, menu and everything you see of.
- Backend code automates the whole process of watching/downloading anime from [animepahe.com](https://animepahe.com) using Requests, BeautifulSoup, Regex, JSON and Math module.

#### Logic
- Takes anime name input from User
- Searches the anime name in Animepahe API using request module and fetches the json data
- Maintains a dict to keep all session-id for anime name search output and prints title for anime, no. of episodes, status and year of release.
- Takes user input for anime name choice with a number
- Takes user input for anime episode no. 
- Fetches the episode session-id using the anime session-id
- Fetches anime episode data response from the API and loads as json
- Watch/Download link for the anime episode is in kwik_pahewin value, all the links are kept in a dict
- Takes user input for quality for the stream/download
- Fetches the specific link for the quality from the dict containing all the links
- Makes a GET request to the link, parses it in HTML using BeautifulSoup and bypasses the AD by fetching out the script tag data which contains the redirect link
- Prints the Anime Episode link.

### Releases
UwUbot is available in Discord and even Terminal. 
Here's how to use it:
#### Discord
1. Git clone the repository: `git clone https://github.com/0xMinato/UwUbot.git`
2. Install PyCord: `python3 -m pip install -U py-cord`
3. Install Requests and BeautifulSoup: `pip3 install requests bs4`
4. Create `config.py` with your Discord bot-token from [Developer Portal](https://discord.com/developers/applications):
```bash
$ echo "TOKEN=XXXX-SECRET-TOKEN-XXXX" > config.py
```
5. Run `discord-bot.py` using Python3.
6. Use `!weeb anime-name` to fetch your favorite anime Watch/Download link.

#### Terminal
1. Git clone the repository: `git clone https://github.com/0xMinato/UwUbot.git`
2. Install Requests and BeautifulSoup: `pip3 install requests bs4`
2. Run `terminal-bot.py` using Python3.
