import json
import variables
import os

os.system("venv\\Scripts\\python.exe data_cleaner.py")
os.system("venv\\Scripts\\python.exe data_maker.py")

next_event = variables.next_event()

# files
with open('data/teams_cleaned.json', 'r') as f:
    teams = json.load(f)


# get a team based on a particular sorting method
def get_team_sortedby(sort_method):
    with open(f'data/players_sortedby_{sort_method}.json', 'r') as f:
        players = json.load(f)

    configuration = variables.configuration()
    budget = variables.budget()
    team_players_selected = variables.team_players_selected()

    team = []
    for player in players:
        if player['seasons'][0]['now_cost'] < budget and configuration[player['position']]['left'] > 0 and team_players_selected[player['team_name']] < 3:
            budget -= player['seasons'][0]['now_cost']
            configuration[player['position']]['left'] -= 1
            team_players_selected[player['team_name']] += 1
            team.append(player)
    return team


# gets the team setup
def displayTeam(team):
    final = []
    for player in team:
        final.append(player['full_name'])
    return ', '.join(final)


# gets estimated total_points based on the previous history of players
def getEstimatedPoints(team):
    points = 0
    for player in team:
        points += player['seasons'][0]['total_points']
    return points


# gets team's cost
def getTeamCost(team):
    cost = 0
    for player in team:
        cost += player['seasons'][0]['now_cost']
    return round(cost, 2)


# gets the formation of the team
def getFormation(team):
    formation = [0, 0, 0]
    for player in team:
        if player['position'] == 'Defender':
            formation[0] += 1
        if player['position'] == 'Midfielder':
            formation[1] += 1
        if player['position'] == 'Forward':
            formation[2] += 1
    
    formation = [str(x) for x in formation]
    return '-'.join(formation)


# get a team based on a particular sorting method
team_sortedby_value = get_team_sortedby('value')

# get a team based on a particular sorting method
team_sortedby_value_per_cost = get_team_sortedby('value_per_cost')


# start building the final team
configuration = variables.configuration()
budget = variables.budget()
team_players_selected = variables.team_players_selected()

# pick up the players which have both high value as well as high value for cost
final_team = []
for player in team_sortedby_value:
    if player in team_sortedby_value_per_cost:
        if budget > player['seasons'][0]['now_cost'] and configuration[player['position']]['left'] > 0 and team_players_selected[player['team_name']] < 3:
            budget -= player['seasons'][0]['now_cost']
            configuration[player['position']]['left'] -= 1
            team_players_selected[player['team_name']] += 1
            final_team.append(player)


# get the highest value player for each of the position irrespective of the cost
with open(f'data/players_sortedby_value.json', 'r') as f:
    players_sortedby_value = json.load(f)

position_checked = []
for player in players_sortedby_value:
    if player not in final_team and configuration[player['position']]['left'] > 0 and team_players_selected[player['team_name']] < 3 and budget > player['seasons'][0]['now_cost'] and player['position'] not in position_checked:
        budget -= player['seasons'][0]['now_cost']
        configuration[player['position']]['left'] -= 1
        team_players_selected[player['team_name']] += 1
        final_team.append(player)
        position_checked.append(player['position'])


# fill the remaining positions by getting the players with highest value for cost
with open(f'data/players_sortedby_value_per_cost.json', 'r') as f:
    players_sortedby_value_per_cost = json.load(f)

while len(final_team) < 15:
    for player in players_sortedby_value_per_cost:
        if player not in final_team and configuration[player['position']]['left'] > 0 and team_players_selected[player['team_name']] < 3 and budget > player['seasons'][0]['now_cost']:
            budget -= player['seasons'][0]['now_cost']
            configuration[player['position']]['left'] -= 1
            team_players_selected[player['team_name']] += 1
            final_team.append(player)


# pick the best 11 member squad from the available players
final_team = sorted(final_team, key=lambda k: k['value_overall'], reverse=True)
formations = variables.formations()

max_points = 0
final_playing_team = []
for formation in formations:
    playing_team = []
    for player in final_team:
        if formation[player['position']] > 0:
            playing_team.append(player)
            formation[player['position']] -= 1

    points = getEstimatedPoints(playing_team)

    if points > max_points:
        max_points = points
        prefered_formation = formation
        final_playing_team = playing_team


with open('final_results.txt', 'w', encoding='UTF-8') as f:
    f.write(f'Team\'s Budget:\n{variables.budget()}\n\n')
    f.write(f'Team\'s Cost:\n{getTeamCost(final_team)}\n\n')
    f.write(f'Estimated_points:\n{round(max_points/(next_event-1))}\n\n')
    f.write('Final Team:')
    f.write(f'\n{str(displayTeam(final_team))}')
    f.write('\n\nPlaying Team:')
    f.write(f'\n{str(displayTeam(final_playing_team))}')
    f.write(f'\n\nCaptain:\n{final_playing_team[0]["full_name"]}')
    f.write(f'\n\nFormation:\n{getFormation(final_playing_team)}')