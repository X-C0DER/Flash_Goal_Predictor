import json
import os

def load_match_details(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def head_to_head(teams, match_details, existing_data=None):
    head_to_head_data = existing_data or {}

    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                matchup = f"{team1} vs {team2}"
                if matchup not in head_to_head_data:
                    head_to_head_data[matchup] = {
                        'Matches Played': 0,
                        f'{team1} Home Wins': 0,
                        f'{team2} Home Wins': 0,
                        f'{team1} Away Wins': 0,
                        f'{team2} Away Wins': 0,
                        'Draws': 0,
                    }

                for matches in match_details.values():
                    for match in matches:
                        if match['Home Team'] == team1 and match['Away Team'] == team2:
                            head_to_head_data[matchup]['Matches Played'] += 1
                            if match['Home Score'] > match['Away Score']:
                                head_to_head_data[matchup][f'{team1} Home Wins'] += 1
                                head_to_head_data[matchup][f'{team2} Away Wins'] += 1
                            elif match['Home Score'] < match['Away Score']:
                                head_to_head_data[matchup][f'{team2} Home Wins'] += 1
                                head_to_head_data[matchup][f'{team1} Away Wins'] += 1
                            else:
                                head_to_head_data[matchup]['Draws'] += 1

    return head_to_head_data

# Specify the directory containing the result JSON files
directory = 'Ethiopia Premier League'

# Get the list of result files in the specified directory
result_files = [file for file in os.listdir(directory) if file.endswith("_result.json")]

# Initialize an empty dictionary to store head-to-head data across all files
cumulative_head_to_head_data = {}

# Iterate over each result file
for result_file in result_files:
    file_path = os.path.join(directory, result_file)
    
    # Load match details from the JSON file
    match_details_dict = load_match_details(file_path)

    # Print debug information for each file
    #print(f"\nDebug information for {result_file}:")
    #print(match_details_dict)  # Print loaded match details for inspection

    # Get the list of teams
    teams = set()
    for matches in match_details_dict.values():
        for match in matches:
            teams.add(match['Home Team'])
            teams.add(match['Away Team'])

    # Update head-to-head analysis with the current result file's data
    cumulative_head_to_head_data = head_to_head(teams, match_details_dict, cumulative_head_to_head_data)

# Save cumulative head-to-head data to a file (h2h.json)
output_file_path = os.path.join(directory, 'h2h.json')
with open(output_file_path, 'w') as output_file:
    json.dump(cumulative_head_to_head_data, output_file, indent=4)

print(f"\nCumulative Head-to-Head Analysis saved to h2h.json.")
