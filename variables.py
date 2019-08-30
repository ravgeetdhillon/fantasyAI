import json

# team's budget
def budget():
    return 99.4

# next gameweek id
def next_event():
    return 4

# all the seasons whose data is to be considered
def all_seasons():
    return ['2019-20', '2018-19']

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