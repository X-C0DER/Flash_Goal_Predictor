import json
import os

def load_match_details(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def head_to_head(teams, match_details):
    head_to_head_data = {}

    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                head_to_head_data[f"{team1} vs {team2}"] = {
                    'Matches Played': 0,
                    'f{team1}Wins': 0,
                    'f{team2}Wins': 0,
                    'Draws': 0,
                }

                for matches in match_details.values():
                    for match in matches:
                        if match['Home Team'] == team1 and match['Away Team'] == team2:
                            head_to_head_data[f"{team1} vs {team2}"]['Matches Played'] += 1
                            if match['Home Score'] > match['Away Score']:
                                head_to_head_data[f"{team1} vs {team2}"]['Wins Team 1'] += 1
                            elif match['Home Score'] < match['Away Score']:
                                head_to_head_data[f"{team1} vs {team2}"]['Wins Team 2'] += 1
                            else:
                                head_to_head_data[f"{team1} vs {team2}"]['Draws'] += 1

    return head_to_head_data

# Specify the directory containing the result JSON files
directory = 'path/to/your/json/files'

# Get the list of result files in the specified directory
result_files = [file for file in os.listdir(directory) if file.endswith("_result.json")]

# Iterate over each result file
for result_file in result_files:
    file_path = os.path.join(directory, result_file)
    
    # Load match details from the JSON file
    match_details_dict = load_match_details(file_path)

    # Get the list of teams
    teams = set()
    for matches in match_details_dict.values():
        for match in matches:
            teams.add(match['Home Team'])
            teams.add(match['Away Team'])

    # Create head-to-head analysis
    head_to_head_data = head_to_head(teams, match_details_dict)

    # Print or further analyze head-to-head data for the current result file
    print(f"Head-to-Head Analysis for {result_file}:")
    for matchup, data in head_to_head_data.items():
        print(f"{matchup}: {data}")
    print("\n")
