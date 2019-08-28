import json

# global variables
all_seasons = ['2019-20', '2018-19']

positions = {
    1: 'Goalkeeper',
    2: 'Defender',
    3: 'Midfielder',
    4: 'Forward'
}

league_data = {}
for season in all_seasons:
    league_data[season] = {
        'all_players_points': 0,
        'all_players_minutes': 0,
        'all_players_games': 0,
        'all_players_cost': 0
    }

# read files for getting the data about players, teams and fixtures
with open('data/final_players_cleaned_data.json', 'r') as f:
    players = json.load(f)

with open('data/final_teams_cleaned_data.json', 'r') as f:
    teams = json.load(f)

with open('data/final_fixtures_cleaned_data.json', 'r') as f:
    fixtures = json.load(f)


for player in players:
    
    # get player's position
    player['position'] = positions[player['element_type']]
    
 
    # get player's team and next fixture difficulty rating
    for team in teams:
        if team['id'] == player['team']:
            player['team_name'] = team['name']
            player['fixture_easiness'] = 1 / team['fixture_difficulty']
            break


    # get player's data for each season
    for season in player['seasons']:
        # find total games player played in a season
        try:
            season['total_games'] = int(round(season['total_points'] / season['points_per_game']))
        except:
            season['total_games'] = 0

        
        # find total minutes per game player played ins a season
        try:
            season['minutes_per_game'] = round(season['minutes'] / season['total_games'], 2)
        except:
            season['minutes_per_game'] = 0

        
        # find points per minute a player got in a season
        try:
            season['points_per_minute'] = round(season['total_points'] / season['minutes'], 2)
        except:
            season['points_per_minute'] = 0

        
        # rectify the player cost
        season['now_cost'] /= 10
        
        
        # find points per cost given by the player in a season
        try:
            season['points_per_cost'] = round(season['total_points'] / season['now_cost'], 2)
        except:
            season['points_per_cost'] = 0

        
        # assign season factor weightage for a season
        index = all_seasons.index(season['season'])
        season['season_factor'] = -0.1 * (index ** 2) + len(all_seasons) - 1
        

        # get some important season data
        league_data[season['season']]['all_players_cost'] += season['now_cost']
        league_data[season['season']]['all_players_games'] += season['total_games']
        league_data[season['season']]['all_players_points'] += season['total_points']
        league_data[season['season']]['all_players_minutes'] += season['minutes']


# calculate some basic season stats
for season in all_seasons:
    league_data[season]['avg_minutes_per_game'] = league_data[season]['all_players_minutes'] / league_data[season]['all_players_games']
    league_data[season]['avg_points_per_minute'] = league_data[season]['all_players_points'] / league_data[season]['all_players_minutes']
    league_data[season]['avg_points_per_cost'] = league_data[season]['all_players_points'] / league_data[season]['all_players_cost']


# calculate the play factor weightage to for a player in the current season
for player in players:
    for season in player['seasons']:
        if season['minutes_per_game'] >= league_data[season['season']]['avg_minutes_per_game']:
            season['play_factor'] = 1
        elif 45 <= season['minutes_per_game'] < league_data[season['season']]['avg_minutes_per_game']:
            if season['points_per_minute'] > league_data[season['season']]['avg_points_per_minute']:
                season['play_factor'] = 0.75
            else:
                season['play_factor'] = 0.5
        else:
            season['play_factor'] = 0.25


for player in players:
    value = 0
    for season in player['seasons']:
        value += season['points_per_cost'] * season['season_factor'] * season['play_factor']
    # value *= player['fixture_easiness']
    player['value'] = value


# store the entire data to the json files
with open('data/final_players_cleaned_data.json', 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=True, indent=4)


with open('data/final_league_data.json', 'w', encoding='utf-8') as f:
    json.dump(league_data, f, ensure_ascii=True, indent=4)
