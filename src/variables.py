from helpers import load_data
from datetime import datetime, timedelta
import json
import os


def progress():
    """
    Track progress for data visualisation.
    """

    gameweek = [f"gw{i}" for i in range(1, NEXT_EVENT)]
    return [
        {    
            "type": "Mine",
            "points": [63,95,149,199,242,308,363,405,438,475,545,614],
            "gameweek": gameweek
        },
        {    
            "type": "FantasyAI",
            "points": [65,106,171,240,301,393,455,504,542,580,670,745],
            "gameweek": gameweek
        },
        {
            "type": "Highest",
            "points" : [142,224,286,358,421,489,530,587,633,699,775,851],
            "gameweek": gameweek
        },
        {    
            "type": "Average",
            "points": [65,106,150,207,259,311,362,398,435,484,537,585],
            "gameweek": gameweek
        },
    ]


def main_players():
    """
    Returns the players that a manager is interested in.
    """

    return INTERESTED


def not_interested():
    """
    Returns the players that a manager is not interested in.
    """

    return NOT_INTERESTED


def positions():
    """
    Returns the mapping for positions.
    """

    return {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }


def formations():
    """
    returns the possible formations to choose the best team from.
    """

    return [
        {
            "Goalkeeper": 1,
            "Defender": 3,
            "Midfielder": 5,
            "Forward": 2
        },
        {
            "Goalkeeper": 1,
            "Defender": 3,
            "Midfielder": 4,
            "Forward": 3
        },
        {
            "Goalkeeper": 1,
            "Defender": 4,
            "Midfielder": 3,
            "Forward": 3
        },
        {
            "Goalkeeper": 1,
            "Defender": 4,
            "Midfielder": 4,
            "Forward": 2
        },
        {
            "Goalkeeper": 1,
            "Defender": 4,
            "Midfielder": 5,
            "Forward": 1
        },
        {
            "Goalkeeper": 1,
            "Defender": 5,
            "Midfielder": 3,
            "Forward": 2
        },
        {
            "Goalkeeper": 1,
            "Defender": 5,
            "Midfielder": 4,
            "Forward": 1
        }
    ]



def configuration():
    """
    Returns the maximum allowed players for a particular position.
    """
    
    return {
        "Goalkeeper": {
            "left": 2
        },
        "Defender": {
            "left": 5
        },
        "Midfielder": {
            "left": 5
        },
        "Forward": {
            "left": 3
        },
    }


def team_players_selected():
    """
    Players selected for each team.
    """

    with open("data/teams_cleaned.json", "r") as f:
        teams = json.load(f)

    team_players_selected = {}

    for team in teams:
        team_players_selected[team["name"]] = 0
    
    return team_players_selected


# seasons to consider for data collection
ALL_SEASONS = ["2019-20"]

# ongoing season
CURRENT_SEASON = "2019-20"

# number of random teams to search
ITERATIONS = 1

# credentails for email
SENDER_EMAIL = os.environ.get("GMAIL_SENDER")
RECEIVER_EMAIL = os.environ.get("GMAIL_RECEIVER")
PASSWORD = os.environ.get("GMAIL_PASS")

# number of hours before which user is notified about transfers
NOTIFY_BEFORE = 4

# user's team id
TEAM_ID = 4914864

team = load_data("user_team.json", "data/original")
players = load_data("filtered_players.json", "data")
INTERESTED = []
for pick in team['picks']:
    for player in players:
        if pick['element'] == player['id']:
            INTERESTED.append(player['full_name'])
            break

NOT_INTERESTED = []
BANK = team['entry_history']['bank'] / 10
RANK = team['entry_history']['overall_rank']
BUDGET = team['entry_history']['value'] / 10
CURRENT_POINTS = team['entry_history']['total_points']
