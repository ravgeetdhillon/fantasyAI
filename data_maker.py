import json
import os
import variables


# global variables
all_seasons = variables.all_seasons()
positions = variables.positions()

league_data = {}
for season in all_seasons:
    league_data[season] = {
        'all_players_value_season': 0,
        'all_players_bps': 0,
        'all_players_threat': 0,
        'all_players_creativity': 0,
    }


# read files for getting the data about players, teams and fixtures
with open('data/players_cleaned.json', 'r') as f:
    players = json.load(f)

with open('data/teams_cleaned.json', 'r') as f:
    teams = json.load(f)

with open('data/fixtures_cleaned.json', 'r') as f:
    fixtures = json.load(f)


# generate the desired data for each player for each season
for player in players:    
    # get player's position
    player['position'] = positions[player['element_type']]
    
    # get player's team and next fixture difficulty rating
    for team in teams:
        if team['id'] == player['team']:
            player['team_name'] = team['name']
            player['fixture_easiness'] = 1 - 0.1 * team['fixture_difficulty']
            break

    # get player's data for each season
    for season in player['seasons']:
        # rectify the player cost
        season['now_cost'] /= 10

        # assign season factor weightage for a season
        index = all_seasons.index(season['season'])
        season['season_factor'] = 0.25 * (index ** 2) - 1 * index + len(all_seasons) - 1


# get total number of players in each season from the cleaned data
for season in all_seasons:
    with open(f'data/{season}_players_cleaned.json', 'r') as f:
        league_data[season]['total_players'] = len(json.load(f))


# get some important league data for each season
for player in players:
    for season in player['seasons']:
        league_data[season['season']]['all_players_value_season'] += season['value_season']
        league_data[season['season']]['all_players_bps'] += season['bps']
        league_data[season['season']]['all_players_threat'] += season['threat']
        league_data[season['season']]['all_players_creativity'] += season['creativity']


# calculate all the required season stats for player comparison
for season in all_seasons:
    player = league_data[season]
    player['avg_value_season_per_player'] = player['all_players_value_season'] / player['total_players']
    player['avg_bps_per_player'] = player['all_players_bps'] / player['total_players']
    player['avg_threat_per_player'] = player['all_players_threat'] / player['total_players']
    player['avg_creativity_per_player'] = player['all_players_creativity'] / player['total_players']
    

# calculate value for each player for each season
for player in players:
    value_overall = 0
    season_factors_sum = 0
    for season in player['seasons']:
        value = 0
        value += 1 * season['value_season'] / league_data[season['season']]['avg_value_season_per_player']
        value += 0.9 * season['bps'] / league_data[season['season']]['avg_bps_per_player']
        value += 0.75 * season['threat'] / league_data[season['season']]['avg_threat_per_player']
        value += 0.55 * season['creativity'] / league_data[season['season']]['avg_creativity_per_player']
        season['value'] = value
        value_overall = (value_overall * season_factors_sum) + (value * season['season_factor'])
        season_factors_sum += season['season_factor']
        value_overall = value_overall / season_factors_sum
    value_overall += 0.3 * player['fixture_easiness']
    player['value_overall'] = value_overall
    player['value_per_cost'] = player['value_overall'] / player['seasons'][0]['now_cost'] 


# store the entire data to the json files
with open('data/players_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=True, indent=2)

with open('data/league_stats.json', 'w', encoding='utf-8') as f:
    json.dump(league_data, f, ensure_ascii=True, indent=2)


# sort the players according to their value
players_sortedby_value = sorted(players, key=lambda k: k['value_overall'], reverse=True)
players_sortedby_value_per_cost = sorted(players, key=lambda k: k['value_per_cost'], reverse=True)


with open('data/players_sortedby_value.json', 'w', encoding='utf-8') as f:
    json.dump(players_sortedby_value, f, ensure_ascii=True, indent=2)

with open('data/players_sortedby_value_per_cost.json', 'w', encoding='utf-8') as f:
    json.dump(players_sortedby_value_per_cost, f, ensure_ascii=True, indent=2)
