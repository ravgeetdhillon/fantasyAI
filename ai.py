import json
import variables


# initialize the global variables
next_event = variables.next_event()
configuration = variables.configuration()
budget = variables.budget()
team_players_selected = variables.team_players_selected()
final_team = []


# writes the team onto a file
def displayTeam(team):
    composition = {
        'Goalkeeper': [],
        'Defender': [],
        'Midfielder': [],
        'Forward': []
    }
    for player in team:
        composition[player['position']].append(player["full_name"])
    result = ''
    for position in composition:
        result += f'\n{position}: '
        result += ', '.join(composition[position])
    return result


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


# compare the `final_value` of two players
def valueInRange(player1, player2):
    a = max(player1['final_value'], player2['final_value'])
    b = min(player1['final_value'], player2['final_value'])
    ans = (a - b) * 100 / a
    if ans <= 5:
        return True
    else:
        return False


# compare the `final_value_per_cost` of two players
def valuePerCostInRange(player1, player2):
    a = max(player1['final_value_per_cost'], player2['final_value_per_cost'])
    b = min(player1['final_value_per_cost'], player2['final_value_per_cost'])
    ans = (a - b) * 100 / a
    if ans <= 5:
        return True
    else:
        return False


# compare the product of `final_value` and `value_points` of two players
def valueAndValuePointsInRange(player1, player2):
    a = max(player1['final_value'] * player1['value_points'], player2['final_value'] * player2['value_points'])
    b = min(player1['final_value'] * player1['value_points'], player2['final_value'] * player2['value_points'])
    ans = (a - b) * 100 / a
    if ans <= 5:
        return True
    else:
        return False


# get the player with easier fixture
def playerWithEasyFixtures(player1, player2):
    if player1['fer'] >= player2['fer']:
        return player1
    else:
        return player2


# function to add the valid playyer to the final team
def addPlayerToFinalTeam(player, configuration=configuration, team_players_selected=team_players_selected, final_team=final_team):
    global budget
    budget -= player['seasons'][0]['now_cost']
    configuration[player['position']]['left'] -= 1
    team_players_selected[player['team_name']] += 1
    final_team.append(player)


# selects the players from a given lot based on the `final_value`
def selectPlayersBasedOnValue(position, picks=0):
    for _ in range(picks):
        selected_players = []
        i = 0
        while len(selected_players) < 2:
            if position[i] not in final_team and budget > position[i]['seasons'][0]['now_cost'] and configuration[position[i]['position']]['left'] > 0 and team_players_selected[position[i]['team_name']] < 3 and position[i]['status'] == 'a':
                selected_players.append(position[i])
            i += 1
        if valueInRange( selected_players[0], selected_players[1] ):
            if valueAndValuePointsInRange( selected_players[0], selected_players[1] ):
                addPlayerToFinalTeam( playerWithEasyFixtures(selected_players[0], selected_players[1]) )
            else:
                addPlayerToFinalTeam(selected_players[0])
        else:
            addPlayerToFinalTeam(selected_players[0])


# selects the players from a given lot based on the `final_value_per_cost`
def selectPlayersBasedOnValuePerCost(position, picks=0):
    position = sorted(position, key=lambda k: -k['final_value_per_cost'])
    for _ in range(picks):
        selected_players = []
        i = 0
        while len(selected_players) < 3 and i < len(position):
            if position[i] not in final_team and budget > position[i]['seasons'][0]['now_cost'] and configuration[position[i]['position']]['left'] > 0 and team_players_selected[position[i]['team_name']] < 3 and position[i]['status'] == 'a':
                if len(selected_players) == 0:
                    min_value_points = position[i]['value_points']
                    selected_players.append(position[i])
                if position[i]['value_points'] > min_value_points:
                    selected_players.append(position[i])
            i += 1

        i = 0
        while i < len(selected_players) - 1:
            if not(valuePerCostInRange( selected_players[i], selected_players[i + 1] )):
                for _ in range(i + 1, len(selected_players)):
                    del selected_players[i + 1]
                break
            i +=1

        i = 0
        while i < len(selected_players) - 1:
            if not(valueAndValuePointsInRange( selected_players[i], selected_players[i + 1] )):
                for _ in range(i + 1, len(selected_players)):
                    del selected_players[i + 1]
                break
            i +=1
        if len(selected_players) == 1:
            addPlayerToFinalTeam(selected_players[0])
        else:
            addPlayerToFinalTeam( playerWithEasyFixtures(selected_players[0], selected_players[1]) )


# load the all the players for team selection
with open(f'data/final_players_sorted.json', 'r') as f:
    players = json.load(f)


# select players according to their playing positions
goalkeepers = [player for player in players if player['position'] == 'Goalkeeper']
forwards = [player for player in players if player['position'] == 'Forward']
midfielders = [player for player in players if player['position'] == 'Midfielder']
defenders = [player for player in players if player['position'] == 'Defender']


# select players in following rounds
# round 1
selectPlayersBasedOnValue(goalkeepers, 1)
selectPlayersBasedOnValue(forwards, 2)
selectPlayersBasedOnValue(defenders, 2)
selectPlayersBasedOnValue(midfielders, 2)

# round 2
selectPlayersBasedOnValuePerCost(goalkeepers, 1)
selectPlayersBasedOnValuePerCost(defenders, 2)
selectPlayersBasedOnValuePerCost(midfielders, 2)

# round 3
selectPlayersBasedOnValue(defenders, 1)
selectPlayersBasedOnValue(forwards, 1)
selectPlayersBasedOnValue(midfielders, 1)


# select the best playing eleven with the most suitable formation
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


# write the final results onto a file
with open('final_results.txt', 'w', encoding='UTF-8') as f:
    f.write(f'Team\'s Budget:\n{variables.budget()}\n\n')
    f.write(f'Team\'s Cost:\n{getTeamCost(final_team)}\n\n')
    f.write(f'Cost in Hand:\n{variables.budget() - getTeamCost(final_team)}\n\n')
    f.write(f'Team\'s Strength:\n{len(final_team)}\n\n')
    f.write(f'Estimated_points:\n{round(max_points * 38 / (next_event-1))}\n\n')
    f.write('Final Team:')
    f.write(f'{displayTeam(final_team)}')
    f.write(f'\n\nFormation:\n{getFormation(final_playing_team)}')
    f.write('\n\nPlaying Team:')
    f.write(f'{displayTeam(final_playing_team)}')
    f.write(f'\n\nCaptain:\n{final_playing_team[0]["full_name"]}')
