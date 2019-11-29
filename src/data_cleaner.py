import pandas
import json
import variables
import os
import shutil
import sys


# variables
next_event = variables.NEXT_EVENT
all_seasons = variables.ALL_SEASONS


def get_data(season):
	'''
	Gets the data for the given season for each player.
	'''
	
	df = pandas.read_csv(f'raw_data/{season}/players_raw.csv')
	headers = ['first_name', 'second_name', 'minutes', 'total_points', 'points_per_game', 'team', 'element_type', 'now_cost', 'status', 'id']
	data = df[headers]
	total_players = len(data)
	players = []
	i = 0
	for i in range(total_players):
		player = {}
		for header in headers:
			try:
				player[header] = data[header][i].item()
			except:
				player[header] = data[header][i]

		player_name = player['first_name'] + ' ' +  player['second_name']
		player['full_name'] = player_name.lower()

		stats_headers = ['minutes', 'total_points', 'points_per_game', 'now_cost']
		player_season_stats = {"season": season}
		for header in stats_headers:
			player_season_stats[header] = player[header]
			del player[header]
		player['seasons'] = [player_season_stats]
		players.append(player)

	# only retain the players who have played atleast one game in the season
	players = [player for player in players if player['seasons'][0]['points_per_game'] > 0]
	
	with open(f'data/{season}_players_cleaned.json', 'w', encoding='utf-8') as f:
		json.dump(players, f, ensure_ascii=True, indent=2)


# change the folder names of players gameweek data to the player's name and copy the data to `data` folder
if not os.path.exists('data'):
	os.mkdir('data')

print('Collecting player data')
for season in all_seasons:
	if len(os.listdir(f'raw_data/{season}/players')) > 0:
		try:
			shutil.rmtree(f'data/players{season}')
		except:
			pass
		finally:
			os.mkdir(f'data/players{season}')
			
		for filename in os.listdir(f'raw_data/{season}/players'):
			new = filename.split('_')
			new = f'{new[0].lower()} {new[1].lower()}'
			try:
				os.rename(f'raw_data/{season}/players/{filename}', f'data/players{season}/{new}')
			except:
				os.rename(f'raw_data/{season}/players/{filename}', f'data/players{season}/{new}{new[-1]}')


# players data for all the seasons
for season in all_seasons:
	get_data(season)


# update players data for season 2019-20
with open('data/2019-20_players_cleaned.json', 'r') as f:
    players1920 = json.load(f)

# with open('data/2018-19_players_cleaned.json', 'r') as f:
#     players1819 = json.load(f)


# # add the data from previous seasons if available
# for cur_player in players1920:
# 	for for_player in players1819:
# 		if cur_player['full_name'] == for_player['full_name']:
# 			cur_player['seasons'].append(for_player['seasons'][0])
# 			break


# get the gameweek history of each player for each season
for player in players1920:
	for season in player['seasons']:
		df = pandas.read_csv(f'data/players{season["season"]}/{player["full_name"]}/gw.csv')
		headers = ['total_points', 'minutes']
		data = df[headers]
		player_gw_history = []
		for i in range(len(data)):
			if data['minutes'][i] >= 60:
				player_gw_history.append(data['total_points'][i].item() - 2)
			elif 0 < data['minutes'][i] < 60:
				player_gw_history.append(data['total_points'][i].item() - 1)
			else:
				player_gw_history.append(data['total_points'][i].item())
		season['gw_history'] = player_gw_history

with open(f'data/players.json', 'w', encoding='utf-8') as f:
    json.dump(players1920, f, ensure_ascii=True, indent=2)

# move gameweeks.json to `data` folder from `raw_data` folder
try:
	os.remove('data/gameweeks.json')
except Exception as e:
	pass
os.rename('raw_data/gameweeks.json', 'data/gameweeks.json')

# get the cleaned data for fixtures
print('Collecting fixtures data')
df = pandas.read_csv('raw_data/fixtures.csv')

headers = ['event', 'finished', 'team_a', 'team_a_difficulty', 'team_h', 'team_h_difficulty']
data = df[headers]
total_fixtures = len(data)
fixtures = []
i = 0
for i in range(total_fixtures):
	fixture = {}
	for header in headers:
		try:
			fixture[header] = data[header][i].item()
		except:
			fixture[header] = data[header][i]
	fixtures.append(fixture)

# only retain the upcoming fixtures
fixtures = [fixture for fixture in fixtures if fixture['event'] >= next_event]

with open('data/fixtures_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(fixtures, f, ensure_ascii=True, indent=2)


# get the cleaned data for teams
print('Collecting teams data')
df = pandas.read_csv('raw_data/teams.csv')

headers = ['id', 'name']
data = df[headers]
total_teams = len(data)
teams = []
i = 0
for i in range(total_teams):
	team = {}
	for header in headers:
		try:
			team[header] = data[header][i].item()
		except:
			team[header] = data[header][i]
	teams.append(team)


with open('data/teams.json', 'w', encoding='utf-8') as f:
    json.dump(teams, f, ensure_ascii=True, indent=2)
