import json


BUDGET = 101.2
NEXT_EVENT = 9
ALL_SEASONS = ['2019-20']
CURRENT_SEASON = '2019-20'
INTERESTED = [
    'tom heaton',
    'nick pope',
    'fikayo tomori',
    'joel ward',
    'trent alexander-arnold',
    'john lundstram',
    'erik pieters',
    'kevin de bruyne',
    'todd cantwell',
    'mason mount',
    'sadio man\u00e9',
    'mark noble',
    'sergio ag\u00fcero',
    'tammy abraham',
    'teemu pukki',
]
NOT_INTERESTED = [

]


def progress():
    '''
    Track progress for data visualisation.
    '''

    gameweek = [f'gw{i}' for i in range(1, NEXT_EVENT)]
    return [
        {    
            'type': 'Mine',
            'points': [63,95,149,199,242,308,363,405],
            'gameweek': gameweek
        },
        {    
            'type': 'Best',
            'points': [65,106,171,240,301,393,455,504],
            'gameweek': gameweek
        },
        {
            'type': 'Highest',
            'points' : [142,224,286,358,421,489,530,587],
            'gameweek': gameweek
        },
        {    
            'type': 'Average',
            'points': [65,106,150,207,259,311,362,398],
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
