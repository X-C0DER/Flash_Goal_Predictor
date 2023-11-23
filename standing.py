import requests
from bs4 import BeautifulSoup

url = "https://www.sofascore.com/tournament/football/ethiopia/premier-league/16601#45663"


response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("div", class_="sc-jlZhew kgghii")
rows = table.find_all("div", class_="sc-fqkvVR sc-dcJsrY gBgQbz fFmCDf sc-4d3c2798-0 bwDcrj")

for row in rows:
    cells = row.find_all("span", class_="sc-jEACwC eqJzpy")
    rank = row.find("div", class_="sc-jEACwC hfBmZi").text.strip()
    team = row.find("span", class_="sc-jEACwC hKLQGc").text.strip()
    matches_played = cells[0].text.strip()
    wins = cells[1].text.strip()
    draws = cells[2].text.strip()
    losses = cells[3].text.strip()
    goals = cells[4].text.strip()
    points = row.find("div", class_="sc-fqkvVR byYarT sc-4d3c2798-3 fgLhKq").text.strip()

    print(f"{rank} {team} {matches_played} {wins} {draws} {losses} {goals} {points}")