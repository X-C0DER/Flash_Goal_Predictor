from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import re
import glob
import time



def get_standing(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)


    match = re.search(r'/football/([^/]*)/([^/]*)/', url)

    League = match.group(1)
    year = match.group(2)
    driver.get(url + "standings/")

    table = driver.find_element(By.CLASS_NAME, "ui-table__body")
    rows = table.find_elements(By.TAG_NAME, "div")

    print(driver.current_url)
    data = []
    headers = ["Rank", "Team", "MP", "Wins", "Draws", "Losses", "Goals", "GD", "Pts"]

    for row in rows:
        rank = row.find_elements(By.CLASS_NAME, "table__cell--rank")
        rank_text = [r.text for r in rank if r.text]

        team = row.find_elements(By.CLASS_NAME, "table__cell--participant")
        team_text = [t.text for t in team if t.text]

        cells = row.find_elements(By.TAG_NAME, "span")
        cell_texts = [cell.text for cell in cells if cell.text]  # Only include cells with text

        if cell_texts:  # Only print rows with non-empty cells
            print(rank_text + team_text + cell_texts)
            row_data = dict(zip(headers, rank_text + team_text + cell_texts))
            data.append(row_data)

    driver.quit()

    df = pd.DataFrame(data)

    # Fix headers
    df.columns = ["Rank", "Team", "MP", "Wins", "Draws", "Losses", "Goals", "GD", "Points"]

    json_data = df.to_json(orient='records')

    final_json = {
        "season": year,
        "league": League,
        "standings": json.loads(json_data)
    }
    filename=f"{League}_{year}_standings.json"
    with open(filename, 'w') as f:
        json.dump(final_json, f)
  

def get_result(url):
    match = re.search(r'/football/([^/]*)/([^/]*)/', url)

    League = match.group(1)
    year = match.group(2)

    driver = webdriver.Chrome()
    driver.get(url+"results/")

    consent = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    consent.click() 

    # Wait for banner to be gone
    WebDriverWait(driver, 3).until(EC.invisibility_of_element(consent))

    while True:
        try:
            # Now click the link  
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR , "a.event__more.event__more--static"))
            )
            button.click()
            time.sleep(2)
        except:
            break

    # Wait for matches to load
    matches = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[title='Click for match detail!']"))
    )

    match_details_dict = {}
    for match in matches:
        # Find round element for the current match
        round = match.find_element(By.XPATH, "./preceding-sibling::div[contains(@class, 'event__round')][1]")
        
        # Get match and round details 
        match_info = match.text 
        round_info = round.text
        
        # Add round and other details to match_details_dict
        if round_info in match_details_dict:
            match_details_dict[round_info].append({
                "Date": match_info.split("\n")[0],
                "Home Team": match_info.split("\n")[1],
                "Away Team": match_info.split("\n")[2],
                "Home Score": match_info.split("\n")[3],
                "Away Score": match_info.split("\n")[4]
                
            })
        else:
            match_details_dict[round_info] = [{
                "Date": match_info.split("\n")[0],
                "Home Team": match_info.split("\n")[1],
                "Away Team": match_info.split("\n")[2],
                "Home Score": match_info.split("\n")[3],
                "Away Score": match_info.split("\n")[4]
               
            }]

    driver.quit()

    # Save the match_details_dict to a JSON file
    with open(f'{League}_{year}_result.json', 'w') as f:
        json.dump(match_details_dict, f, indent=2)

def process_file(file):
    print("Getting Data From " + file)
    print("------------------------------------------------")
    with open(file) as fp:
        content = fp.read()
        lines = content.split("\n")
        for line in lines:
            if line.strip():
                print (line)
                get_result(line)
                # with ThreadPoolExecutor() as executor:
                    # executor.submit(get_standing, line)
                    # executor.submit(get_result,line)
                  

    print("------------------------------------------------")

def get_lines(fname):
    line_count = 0
    with open(fname) as fp:
        content = fp.read()
        lines = content.splitlines()
        for line in lines:
            if line.strip():  # Check if the line is not empty after stripping whitespace
                line_count += 1
    return line_count
  