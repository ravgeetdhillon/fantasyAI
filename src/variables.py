from helpers import load_data
from datetime import datetime, timedelta
import json
import os


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
ALL_SEASONS = ["2020-21"]

# ongoing season
CURRENT_SEASON = "2020-21"

# number of random teams to search
ITERATIONS = 1

# credentails for email
SENDER_EMAIL = os.environ.get("GMAIL_SENDER")
RECEIVER_EMAIL = os.environ.get("GMAIL_RECEIVER")
PASSWORD = os.environ.get("GMAIL_PASS")

# number of hours before which user is notified about transfers
NOTIFY_BEFORE = 4

# user's team id
TEAM_ID = 2087820
