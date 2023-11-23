from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json 
import pandas as pd 



options = Options() 
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get("https://www.flashscore.com/football/ethiopia/premier-league-2022-2023/standings/")

table = driver.find_element(By.CLASS_NAME,"ui-table__body")
rows = table.find_elements(By.TAG_NAME,"div")

print (driver.current_url)
data=[]
headers = ["Rank", "Team", "MP", "Wins", "Draws", "Losses", "Goals", "GD", "Pts"]

for row in rows:

    rank = row.find_elements(By.CLASS_NAME,"table__cell--rank")
    rank_text=[r.text for r in rank if r.text]

    team= row.find_elements(By.CLASS_NAME,"table__cell--participant")
    team_text=[t.text for t in team if t.text]

    cells = row.find_elements(By.TAG_NAME,"span")
    cell_texts = [cell.text for cell in cells if cell.text]  # Only include cells with text

    if cell_texts:  # Only print rows with non-empty cells
        print (rank_text+ team_text+ cell_texts)
        row_data = dict(zip(headers, rank_text+team_text + cell_texts)) 
        data.append(row_data)
 
    
    
driver.quit()

df = pd.DataFrame(data) 

# Fix headers
df.columns = ["Rank","Team", "MP", "Wins", "Draws", "Losses", "Goals","GD", "Points"]  


json_data=df.to_json(orient='records')

final_json = {
  "season": "2023-2024", 
  "league": "Ehiopian Preimer League",
  "standings": json.loads(json_data)
}

with open('data.json', 'w') as f:
    json.dump(final_json, f)