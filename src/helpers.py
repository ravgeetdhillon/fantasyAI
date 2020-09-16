"""
Helper functions for the AI.
"""


from datetime import datetime, timedelta
import json
import os


def load_data(file_name, directory='data'):
    """
    Load the specified file from the given directory(optional).
    """

    with open(f'{directory}/{file_name}', 'r') as f:
        data = json.load(f)

    return data


def save_data(data, file_name, directory='data'):
    """
    Save the data to the specified file.
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f'{directory}/{file_name}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=2)


def get_next_gameweek_id():
    """
    Returns the next gameweek's ID.
    """

    gameweeks = load_data('gameweeks.json', 'data/original')

    now = datetime.utcnow()
    for gameweek in gameweeks:
        next_deadline_date = datetime.strptime(gameweek['deadline_time'], '%Y-%m-%dT%H:%M:%SZ')
        if next_deadline_date > now:
            break

    return gameweek['id']


def get_users_team_stats():
    """
    Get the important attributes about the user's team.
    """

    team = load_data('user_team.json', 'data/original')

    budget = team['entry_history']['value'] / 10
    bank = team['entry_history']['bank'] / 10
    current_points = team['entry_history']['total_points']
    rank = team['entry_history']['overall_rank']

    return budget, bank, current_points, rank


def get_team():
    """
    Returns a list of all the players in the user's team.
    """

    team = load_data('user_team.json', 'data/original')
    picks = team['picks']

    players = load_data('final_players_sorted.json', 'data')
    player_names = []

    for pick in picks:
        for player in players:
            if player['id'] == pick['element']:
                player_names.append(player['full_name'])
                break

    return player_names
