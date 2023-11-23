from bs4 import BeautifulSoup
import requests
import json
import re 


def get_data(url):
    print ("Getting Data for: "+ url)
    match = re.search(r'/football/([^/]*)/([^/]*)/', url)
    league=match.group(1).capitalize() + '_' + match.group(2).capitalize()

    resp=requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')

    data = []
    links = []

    for row in soup.find_all('div', class_='archive__row'):
        season = row.find('div', class_='archive__season').text.strip()
        winner = row.find('div', class_='archive__winner')

        years = re.search(r'\d{4}/\d{4}', season)
        if years:
            season = years.group()
        else:
            season = "No year"

        winner_name = 'No winner' 
        if winner.find('a'):
            winner_name = winner.find('a').text.strip()
            
        link = row.find('a')['href']
        links.append("https://www.flashscore.com" + link)
        
        data.append({
            'League':league,
            'season': season,
            'winner': winner_name
        })

    json_data = json.dumps(data)

    with open(league+'_winner.json', 'w') as f:
        json.dump(data, f)
    
    f.close()

    links.pop(0)
    with open(league+"_archive_list.txt","w") as fp:    
        for l in links:
            fp.write(l+"\n")

    fp.close()


league_url=[
    "https://www.flashscore.com/football/ethiopia/premier-league/archive/",
    "https://www.flashscore.com/football/england/premier-league/archive/",
    "https://www.flashscore.com/football/france/ligue-1/archive/",
    "https://www.flashscore.com/football/italy/serie-a/archive/",
    "https://www.flashscore.com/football/spain/laliga/archive/",
    "https://www.flashscore.com/football/netherlands/eredivisie/archive/",
    "https://www.flashscore.com/football/turkey/super-lig/archive/",

]

for url in league_url:
    get_data(url)
