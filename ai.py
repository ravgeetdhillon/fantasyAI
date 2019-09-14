import json
import variables
import numpy as np


# initialize the global variables
next_event = variables.next_event()
configuration = variables.configuration()
budget = variables.budget()
team_players_selected = variables.team_players_selected()
limit = 10
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
        composition[player['position']].append([player["full_name"], player['seasons'][0]['now_cost']])
    result = ''
    for position in composition:
        result += f'\n{position}: '
        # result += ', '.join(composition[position])
        result += str(composition[position])
    # print(inBudget(team))
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
    if ans <= limit:
        return True
    else:
        return False


# compare the `final_value_per_cost` of two players
def valuePerCostInRange(player1, player2):
    a = max(player1['final_value_per_cost'], player2['final_value_per_cost'])
    b = min(player1['final_value_per_cost'], player2['final_value_per_cost'])
    ans = (a - b) * 100 / a
    if ans <= limit:
        return True
    else:
        return False


# compare the `final_value_per_cost` of two players
def budgetInRange(amount1, amount2):
    if amount2 < 0:
        return False
    elif amount2 < amount1:
        a = max(amount1, amount2)
        b = min(amount1, amount2)
        ans = (a - b) * 100 / a
        if ans <= limit:
            return True
        else:
            return False
    elif amount2 > amount1:
        return True
    

# compare the product of `final_value` and `value_points` of two players
def valueAndValuePointsInRange(player1, player2):
    a = max(player1['final_value'] * player1['value_points'], player2['final_value'] * player2['value_points'])
    b = min(player1['final_value'] * player1['value_points'], player2['final_value'] * player2['value_points'])
    ans = (a - b) * 100 / a
    if ans <= limit:
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


def getCover(player_type, new_player=''):
    forward_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Forward' and player not in final_team])
    midfielder_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Midfielder' and player not in final_team])
    defender_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Defender' and player not in final_team])
    goalkeeper_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Goalkeeper' and player not in final_team])

    cover = 0
    for position in configuration:
        if position == 'Goalkeeper':
            cover += configuration[position]['left'] * goalkeeper_cost
        elif position == 'Defender':
            cover += configuration[position]['left'] * defender_cost
        elif position == 'Midfielder':
            cover += configuration[position]['left'] * midfielder_cost
        elif position == 'Forward':
            cover += configuration[position]['left'] * forward_cost
    
    if player_type == 'Goalkeeper':
        cover -= goalkeeper_cost
    elif player_type == 'Defender':
        cover -= defender_cost
    elif player_type == 'Midfielder':
        cover -= midfielder_cost
    elif player_type == 'Forward':
        cover -= forward_cost
    return cover

donot_consider = []

# selects the players from a given lot based on the `final_value`
def selectPlayersBasedOnValue(position, picks=0):
    for _ in range(picks):
        selected_players = []
        i = 0
        while len(selected_players) < 2 and i < len(position):
            cover = getCover(position[0]['position'])
            b = budget - position[i]['seasons'][0]['now_cost']
            print(f'---c{cover}, b{budget}, after{b}, {position[i]["full_name"]}')
            # if cover <= budget - position[i]['seasons'][0]['now_cost']:
            if budgetInRange(cover, budget - position[i]['seasons'][0]['now_cost']):
                if position[i] not in final_team and budget > position[i]['seasons'][0]['now_cost'] and configuration[position[i]['position']]['left'] > 0 and team_players_selected[position[i]['team_name']] < 3 and position[i]['status'] == 'a' and position[i] not in donot_consider and position[i] not in selected_players:
                    selected_players.append(position[i])
                    print(position[i]['full_name'])
            else:
                donot_consider.append(position[i])
            i += 1
        print(f'--{displayTeam(selected_players)}')
        
        if len(selected_players) == 1:
            addPlayerToFinalTeam( selected_players[0] )
        elif len(selected_players) == 0:
            position = sorted(position, key=lambda k: (k['seasons'][0]['now_cost'], -k['final_value']))
            i = 0
            while position[i] in final_team:
                i += 1
            addPlayerToFinalTeam( position[i] )
        else:
            if valueInRange( selected_players[0], selected_players[1] ):
                if valueAndValuePointsInRange( selected_players[0], selected_players[1] ):
                    addPlayerToFinalTeam( playerWithEasyFixtures(selected_players[0], selected_players[1]) )
                else:
                    addPlayerToFinalTeam(selected_players[0])
            else:
                addPlayerToFinalTeam(selected_players[0])
    
    print(displayTeam(final_team))
    b = budget - position[i]['seasons'][0]['now_cost']
    print(f'{cover}, {budget}, {b}, {position[i]["full_name"]}')
    print('------------------')


# selects the players from a given lot based on the `final_value_per_cost`
def selectPlayersBasedOnValuePerCost(position, picks=0):
    position = sorted(position, key=lambda k: -k['final_value_per_cost'])
    for _ in range(picks):
        selected_players = []
        i = 0
        while len(selected_players) < 3 and i < len(position):
            cover = getCover(position[0]['position'])
            b = budget - position[i]['seasons'][0]['now_cost']
            print(f'{cover}, {budget}, {b}, {position[i]["full_name"]}')
            if budgetInRange(cover, budget - position[i]['seasons'][0]['now_cost']):
                if position[i] not in final_team and budget > position[i]['seasons'][0]['now_cost'] and configuration[position[i]['position']]['left'] > 0 and team_players_selected[position[i]['team_name']] < 3 and position[i]['status'] == 'a' and position[i] not in selected_players:
                    selected_players.append(position[i])
            else:
                donot_consider.append(position[i])
            i += 1
        print(f'ravgeet{displayTeam(selected_players)}')
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

        print(displayTeam(final_team))
        b = budget - position[i]['seasons'][0]['now_cost']
        print(f'{cover}, {budget}, {b}, {position[i]["full_name"]}')
        print('------------------')


# load the all the players for team selection
with open(f'data/final_players_sorted.json', 'r') as f:
    players = json.load(f)


# add players that are most integral to the squad
main_players = variables.main_players()
for player in players:
    if player['full_name'] in main_players:
        addPlayerToFinalTeam(player)


# select players according to their playing positions
goalkeepers = [player for player in players if player['position'] == 'Goalkeeper']
forwards = [player for player in players if player['position'] == 'Forward']
midfielders = [player for player in players if player['position'] == 'Midfielder']
defenders = [player for player in players if player['position'] == 'Defender']


# select players in following rounds
# round 1 - 7 players
# selectPlayersBasedOnValue(goalkeepers, 1)
# selectPlayersBasedOnValue(forwards, 2)
# selectPlayersBasedOnValue(defenders, 1)
# selectPlayersBasedOnValue(midfielders, 2)

# round 2 - 5 players
# selectPlayersBasedOnValue(goalkeepers, 1)
# selectPlayersBasedOnValue(defenders, 2)
# selectPlayersBasedOnValue(midfielders, 2)

# round 3 - 3 players
# selectPlayersBasedOnValue(forwards, 1)
# selectPlayersBasedOnValue(defenders, 1)
# selectPlayersBasedOnValue(midfielders, 1)

print('-----donot_consider')
print(displayTeam(donot_consider))
# select the best playing eleven with the most suitable formation
final_team = sorted(final_team, key=lambda k: k['final_value'], reverse=True)
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
    f.write(f'Cost in Hand:\n{round(variables.budget() - getTeamCost(final_team),1)}\n\n')
    f.write(f'Team\'s Strength:\n{len(final_team)}\n\n')
    f.write(f'Estimated Points:\n{round(max_points * 38 / (next_event-1))}\n\n')
    f.write('Final Team:')
    f.write(f'{displayTeam(final_team)}')
    f.write(f'\n\nFormation:\n{getFormation(final_playing_team)}')
    f.write('\n\nPlaying Team:')
    f.write(f'{displayTeam(final_playing_team)}')
    f.write(f'\n\nCaptain:\n{final_playing_team[0]["full_name"]}')
