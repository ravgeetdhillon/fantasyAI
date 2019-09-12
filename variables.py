import json


# team's budget
def budget():
    return 100.1


# next gameweek id
def next_event():
    return 5


# all the seasons whose data is to be considered
def all_seasons():
    return ['2019-20', '2018-19']


# current season
def current_season():
    return '2019-20'


# mapping for positions
def positions():
    return {
        1: 'Goalkeeper',
        2: 'Defender',
        3: 'Midfielder',
        4: 'Forward'
    }


# possible formations to choose the best team from
def formations():
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


# 15 member sqaud formation for each position
def configuration():
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


# players selected for each team
def team_players_selected():
    with open('data/teams_cleaned.json', 'r') as f:
        teams = json.load(f)
    team_players_selected = {}
    for team in teams:
        team_players_selected[team['name']] = 0
    
    return team_players_selected

# progress for data visualisation
def progress():
    gameweek = [f'gw{i}' for i in range(1, next_event())]
    return [
        {    
            'type': 'Mine',
            'points': [63,95,149,199],
            'gameweek': gameweek
        },
        {
            'type': 'Highest',
            'points' : [142,224,286,358],
            'gameweek': gameweek
        },
        {    
            'type': 'Average',
            'points': [65,106,150,207],
            'gameweek': gameweek
        }
    ]