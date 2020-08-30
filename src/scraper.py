from helpers import save_data, load_data, get_next_gameweek_id
import variables
import json
import requests
import sys


def download_players_data():
    """
    Downloads the players data.
    """

    # load the player specific data from the FPL RestAPI Endpoint
    data = json.loads(requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").text)
    players = data["elements"]

    for player in players:
        player_id = player["id"]
        print(f"Downloading data for player: {player_id}")
        try:
            data = json.loads(requests.get(f"https://fantasy.premierleague.com/api/element-summary/{player_id}/").text)
            player["history"] = data["history"]
        except:
            player["history"] = []

    # save the data in a JSON file
    save_data(players, f"players.json", "data/original")


def download_teams_data():
    """
    Downloads the teams data.
    """

    print(f"Downloading teams data")

    # load the team specific data from the FPL RestAPI Endpoint
    data = json.loads(requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").text)
    teams = data["teams"]

    # save the data in a JSON file
    save_data(teams, "teams.json", "data/original")


def download_fixtures_data():
    """
    Downloads the fixtures data.
    """

    print(f"Downloading fixtures data")
    
    # load the fixture specific data from the FPL RestAPI Endpoint
    fixtures = json.loads(requests.get("https://fantasy.premierleague.com/api/fixtures/").text)

    # save the data in a JSON file
    save_data(fixtures, "fixtures.json", "data/original")


def download_gameweeks_data():
    """
    Downloads the gameweeks data.
    """

    print(f"Downloading gameweeks data")
    
    # load the fixture specific data from the FPL RestAPI Endpoint
    data = json.loads(requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").text)
    gameweeks = data["events"]

    # save the data in a JSON file
    save_data(gameweeks, "gameweeks.json", "data/original")


def download_users_team_data(user_team_id, recent_gw_id):
    """
    Downloads the users team data.
    """

    print(f"Downloading {user_team_id} user team data")

    # load the fixture specific data from the FPL RestAPI Endpoint
    user_team = json.loads(requests.get(f"https://fantasy.premierleague.com/api/entry/{user_team_id}/event/{recent_gw_id}/picks/").text)

    # save the data in a JSON file
    save_data(user_team, "user_team.json", "data/original")


if __name__ == "__main__":
    # download_players_data()
    # download_fixtures_data()
    # download_teams_data()
    download_gameweeks_data()
    user_team_id = sys.argv[1]
    recent_gw_id = get_next_gameweek_id() - 1
    download_users_team_data(user_team_id, recent_gw_id)
