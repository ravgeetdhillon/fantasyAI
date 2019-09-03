import json
import os
import variables
import numpy as np


# global variables
all_seasons = variables.all_seasons()
positions = variables.positions()

league_data = {}
for season in all_seasons:
    league_data[season] = {
        'all_players_effective_points': 0,
        'all_players_minutes': 0
    }
    

# read files for getting the data about players, teams and fixtures
with open('data/players_cleaned.json', 'r') as f:
    players = json.load(f)

with open('data/teams_cleaned.json', 'r') as f:
    teams = json.load(f)

with open('data/fixtures_cleaned.json', 'r') as f:
    fixtures = json.load(f)


# get the fixture easiness rating for each team for the next five matches
avg_fer_points = 0
for team in teams:
	fer = []
	for fixture in fixtures:
		if fixture['team_a'] == team['id']:
			fer.append(1 - 0.1 * fixture['team_a_difficulty'])
		elif fixture['team_h'] == team['id']:
			fer.append(1 - 0.1 * fixture['team_h_difficulty'])
		if len(fer) == 5:
			break
	team['fer'] = fer
	team['fer_points'] = np.mean(fer) * (1 - np.var(fer))
	avg_fer_points += team['fer_points']

avg_fer_points /= len(teams)
for team in teams:
	team['fer_points'] /= avg_fer_points

teams = sorted(teams, key=lambda k: k['fer_points'], reverse=True)
with open('data/teams_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(teams, f, ensure_ascii=True, indent=2)


# generate the desired data for each player for each season
for player in players:    
    # get player's position
    player['position'] = positions[player['element_type']]
    player['value_points'] = 0
    
    # get player's team and next fixture difficulty rating
    for team in teams:
        if team['id'] == player['team']:
            player['team_name'] = team['name']
            player['fer'] = team['fer_points']
            if team['fer_points'] >= 1:
                player['value_points'] += 1
            break

    # get player's data for each season
    total_career_games = 0
    for season in player['seasons']:
        season['total_games'] = round(season['total_points'] / season['points_per_game'])
        total_career_games += season['total_games']
        app_points = season['effective_points'] = round(season['minutes'] / 90) * 2
        season['effective_points'] = season['total_points'] - app_points

        # rectify the player cost
        season['now_cost'] /= 10

    # assign season factor weightage for each season
    for season in player['seasons']:
        if season['season'] == variables.current_season():
            # season['season_factor'] = season['total_games'] / total_career_games
            season['season_factor'] = ((season['total_games'] / total_career_games) + 1.2) / 2
        else:
            season['season_factor'] = ((season['total_games'] / total_career_games) - 0.2) / 2


# get total number of players in each season from the cleaned data
for season in all_seasons:
    with open(f'data/{season}_players_cleaned.json', 'r') as f:
        league_data[season]['total_players'] = len(json.load(f))


# get some important league data for each season
for player in players:
    for season in player['seasons']:
        league_data[season['season']]['all_players_effective_points'] += season['effective_points']
        league_data[season['season']]['all_players_minutes'] += season['minutes']


# calculate all the required season stats for player comparison
for season in all_seasons:
    league_data[season]['avg_effective_points_per_player'] = league_data[season]['all_players_effective_points'] / league_data[season]['total_players']
    league_data[season]['avg_minutes_per_player'] = league_data[season]['all_players_minutes'] / league_data[season]['total_players']
    if season == variables.current_season():
        league_data[season]['avg_minutes_per_player'] /= (variables.next_event() - 1)
    else:
        league_data[season]['avg_minutes_per_player'] /= 38


# calculate value points for each player in terms of amount of time they played, upcoming fixtures
for player in players:
    for season in player['seasons']:
        if season['minutes'] / season['total_games'] >= league_data[season['season']]['avg_minutes_per_player']:
            player['value_points'] += 1
    if len(player['seasons']) == 1:
            player['value_points'] += 1


# calculate value for each player for each season
for player in players:
    value_overall = 0
    for season in player['seasons']:
        season['value'] = season['effective_points'] / league_data[season['season']]['avg_effective_points_per_player']
        value_overall += season['value'] * season['season_factor']

    player['value_overall'] = value_overall
    player['value_per_cost'] = player['value_overall'] / player['seasons'][0]['now_cost']


# store the entire data to the json files
with open('data/players_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=True, indent=2)

with open('data/league_stats.json', 'w', encoding='utf-8') as f:
    json.dump(league_data, f, ensure_ascii=True, indent=2)


# sort the players according to their value
players_sortedby_value = sorted(players, key=lambda k: (-k['value_points'], -k['value_overall']))
players_sortedby_value_per_cost = sorted(players, key=lambda k: (-k['value_points'], -k['value_per_cost']))


with open('data/players_sortedby_value.json', 'w', encoding='utf-8') as f:
    json.dump(players_sortedby_value, f, ensure_ascii=True, indent=2)

with open('data/players_sortedby_value_per_cost.json', 'w', encoding='utf-8') as f:
    json.dump(players_sortedby_value_per_cost, f, ensure_ascii=True, indent=2)
