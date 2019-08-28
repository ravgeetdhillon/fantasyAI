import pandas
import numpy as np
import json

# global variables
next_event = 3

def get_clean_data(season):
	df = pandas.read_csv(f'raw_data/{season}/players_raw.csv')

	headers = ['first_name', 'second_name', 'minutes', 'total_points', 'points_per_game', 'team', 'element_type', 'now_cost']
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

	with open(f'data/{season}_players_cleaned_data.json', 'w', encoding='utf-8') as f:
		json.dump(players, f, ensure_ascii=True, indent=4)


# players data for season 2018-19
get_clean_data('2018-19')


# players data for season 2019-20
get_clean_data('2019-20')


# update players data for season 2019-20
with open('data/2019-20_players_cleaned_data.json', 'r') as f:
    players1920 = json.load(f)

with open('data/2018-19_players_cleaned_data.json', 'r') as f:
    players1819 = json.load(f)

for cur_player in players1920:
	for for_player in players1819:
		if cur_player['full_name'] == for_player['full_name']:
			cur_player['seasons'].append(for_player['seasons'][0])

with open(f'data/final_players_cleaned_data.json', 'w', encoding='utf-8') as f:
    json.dump(players1920, f, ensure_ascii=True, indent=4)


# get the fixtures
df = pandas.read_csv('raw_data/2019-20/fixtures.csv')

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

with open('data/final_fixtures_cleaned_data.json', 'w', encoding='utf-8') as f:
    json.dump(fixtures, f, ensure_ascii=True, indent=4)


# get the teams
df = pandas.read_csv('raw_data/2019-20/teams.csv')

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

for fixture in fixtures:
	if fixture['event'] == next_event:
		teams[fixture['team_a'] - 1]['fixture_difficulty'] = fixture['team_a_difficulty']
		teams[fixture['team_h'] - 1]['fixture_difficulty'] = fixture['team_h_difficulty']
	elif fixture['event'] > next_event:
		break

with open('data/final_teams_cleaned_data.json', 'w', encoding='utf-8') as f:
    json.dump(teams, f, ensure_ascii=True, indent=4)
