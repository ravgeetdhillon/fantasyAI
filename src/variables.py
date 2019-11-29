import json
import os


def progress():
    '''
    Track progress for data visualisation.
    '''

    gameweek = [f'gw{i}' for i in range(1, NEXT_EVENT)]
    return [
        {    
            'type': 'Mine',
            'points': [63,95,149,199,242,308,363,405,438,475,545,614],
            'gameweek': gameweek
        },
        {    
            'type': 'FantasyAI',
            'points': [65,106,171,240,301,393,455,504,542,580,670,745],
            'gameweek': gameweek
        },
        {
            'type': 'Highest',
            'points' : [142,224,286,358,421,489,530,587,633,699,775,851],
            'gameweek': gameweek
        },
        {    
            'type': 'Average',
            'points': [65,106,150,207,259,311,362,398,435,484,537,585],
            'gameweek': gameweek
        },
    ]


def main_players():
    '''
    Add players to the final team that a manager is interested in.
    '''

    return INTERESTED


def not_interested():
    '''
    Doesn't considers the players that a manager is not interested in.
    '''

    return NOT_INTERESTED


def positions():
    '''
    Mapping for positions.
    '''

    return {
        1: 'Goalkeeper',
        2: 'Defender',
        3: 'Midfielder',
        4: 'Forward'
    }


def formations():
    '''
    Possible formations to choose the best team from
    '''

    return [
        {
            'Goalkeeper': 1,
            'Defender': 3,
            'Midfielder': 5,
            'Forward': 2
        },
        {
            'Goalkeeper': 1,
            'Defender': 3,
            'Midfielder': 4,
            'Forward': 3
        },
        {
            'Goalkeeper': 1,
            'Defender': 4,
            'Midfielder': 3,
            'Forward': 3
        },
        {
            'Goalkeeper': 1,
            'Defender': 4,
            'Midfielder': 4,
            'Forward': 2
        },
        {
            'Goalkeeper': 1,
            'Defender': 4,
            'Midfielder': 5,
            'Forward': 1
        },
        {
            'Goalkeeper': 1,
            'Defender': 5,
            'Midfielder': 3,
            'Forward': 2
        },
        {
            'Goalkeeper': 1,
            'Defender': 5,
            'Midfielder': 4,
            'Forward': 1
        }
    ]



def configuration():
    '''
    15 member sqaud formation for each position.
    '''
    
    return {
        'Goalkeeper': {
            'left': 2
        },
        'Defender': {
            'left': 5
        },
        'Midfielder': {
            'left': 5
        },
        'Forward': {
            'left': 3
        },
    }


def team_players_selected():
    '''
    Players selected for each team.
    '''

    with open('data/teams_cleaned.json', 'r') as f:
        teams = json.load(f)

    team_players_selected = {}


    for team in teams:
        team_players_selected[team['name']] = 0
    
    return team_players_selected


def get_team():
    '''
    Get the team's players.
    '''

    with open('raw_data/my_team.json', 'r') as f:
        team = json.load(f)[-1]

    with open('data/final_players_sorted.json', 'r') as f:
        players = json.load(f)

    player_names = []

    picks = team['picks']
    for pick in picks:
        for player in players:
            if player['id'] == pick['element']:
                player_names.append(player['full_name'])
                break

    return player_names


def get_stats():
    '''
    Get the important attributes about the team and gameweeks.
    '''

    with open('raw_data/my_team.json', 'r') as f:
        team = json.load(f)[-1]

    budget = team['entry_history']['value'] / 10
    next_event = team['entry_history']['event'] + 1
    current_points = team['entry_history']['total_points']
    rank = team['entry_history']['overall_rank']
    bank = team['entry_history']['bank'] / 10
    
    return budget, next_event, current_points, rank, bank


BUDGET, NEXT_EVENT, CURRENT_POINTS, RANK, BANK = get_stats()
ALL_SEASONS = ['2019-20']
CURRENT_SEASON = '2019-20'
ITERATIONS = 1000
INTERESTED = get_team()
NOT_INTERESTED = []
SENDER_EMAIL = os.environ.get('GMAIL_SENDER')
RECEIVER_EMAIL = os.environ.get('GMAIL_RECEIVER')
PASSWORD = os.environ.get('GMAIL_PASS')
NOTIFY_BEFORE = 4
TEAM_ID = 4914864
