from bs4 import BeautifulSoup
import requests
import json
import re 

url="https://www.flashscore.com/football/ethiopia/premier-league/archive/"
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
        'season': season,
        'winner': winner_name
    })

json_data = json.dumps(data)

with open('data2.json', 'w') as f:
     json.dump(data, f)

for l in links:
    url=requests.get(l+"standings/#/jBbIM3jE/table/overall")
    bs=BeautifulSoup(url.text,'html.parser')
    #print (url.url)
    row = soup.find('div', class_='table__cell table__cell--participant')

    mp = row.find('span', class_='table__cell table__cell--value').text.strip()
    wins = row.find_all('span', class_='table__cell table__cell--value')[2].text.strip() 
    draws = row.find_all('span', class_='table__cell table__cell--value')[3].text.strip()
    losses = row.find_all('span', class_='table__cell table__cell--value')[4].text.strip()
    goals = row.find_all('span', class_='table__cell table__cell--value')[5].text.strip()
    gd = row.find_all('span', class_='table__cell table__cell--value')[6].text.strip() 
    points = row.find_all('span', class_='table__cell table__cell--value')[7].text.strip()
    
    print(rank, name, mp, wins, draws, losses, goals, gd, points)
    # print (l+'results/')

