from helpers import save_data, load_data, get_next_gameweek_id
import numpy as np
import json
import os
import variables
import sys


# global variables
all_seasons = variables.ALL_SEASONS
next_event = get_next_gameweek_id()
positions = variables.positions()


league_data = {}
for season in all_seasons:
    league_data[season] = {
        "all_players_effective_total_points": 0,
        "all_players_minutes": 0
    }
    

# read files for getting the data about players, teams and fixtures
teams = load_data("filtered_teams.json", "data")
fixtures = load_data("filtered_fixtures.json", "data")
players = load_data("filtered_players.json", "data")


# assign the fixture easiness rating for each team for the next five matches.
max_fer_points = 0
avg_fer_points = 0

for team in teams:
    fer = []
    for fixture in fixtures:
        if fixture["team_a"] == team["id"]:
            fer.append(1 - 0.1 * fixture["team_a_difficulty"])
        elif fixture["team_h"] == team["id"]:
            fer.append(1 - 0.1 * fixture["team_h_difficulty"])
        if len(fer) == 5:
            break
    
    team["fer"] = fer
    team["fer_points"] = np.mean(fer) * (1 - np.var(fer))
    avg_fer_points += team["fer_points"]

avg_fer_points /= len(teams)
for team in teams:
    team["fer_points"] = round(team["fer_points"] / avg_fer_points, 3)
    if team["fer_points"] > max_fer_points:
        max_fer_points = team["fer_points"]

teams = sorted(teams, key=lambda k: k["fer_points"], reverse=True)
save_data(teams, "teams_cleaned.json", "data")


# generate the desired data for each player for each season.
max_consistency= {}
for season in all_seasons:
    max_consistency[season] = 0


for player in players:    
    # get player's position
    player["position"] = positions[player["element_type"]]
    player["value_points"] = 0

    # get player's team and next fixture difficulty rating
    for team in teams:
        if team["id"] == player["team"]:
            player["team_name"] = team["name"]
            player["fer"] = team["fer_points"]
            if team["fer_points"] >= 1:
                player["value_points"] += 10
            else:
                player["value_points"] += 8
            break

    # get player's data for each season
    total_career_games = 0
    for season in player["seasons"]:
        season["effective_total_points"] = np.sum(season["gw_history"]).item()
        season["gw_avg_points"] = np.mean(season["gw_history"]).item()
        season["variance"] = np.var(season["gw_history"]).item()
        season["consistency_factor"] = season["gw_avg_points"] * (100 - season["variance"])
        if season["consistency_factor"] > max_consistency[season["season"]]:
            max_consistency[season["season"]] = season["consistency_factor"]
        del season["gw_history"]

        season["total_games"] = round(season["total_points"] / season["points_per_game"])
        total_career_games += season["total_games"]

        # rectify the player cost
        season["now_cost"] /= 10

    # assign season factor weightage for each season
    for season in player["seasons"]:
        if season["season"] == variables.CURRENT_SEASON:
            season["season_factor"] = ((season["total_games"] / total_career_games) + 1) / 2
        else:
            season["season_factor"] = (season["total_games"] / total_career_games) / 2


# normalize the season consistency factor and award the value points
for index, player in enumerate(players):
    player["consistency_overall"] = 0
    for season in player["seasons"]:
        season["consistency_factor"] /= max_consistency[season["season"]]
        player["consistency_overall"] += season["consistency_factor"] * season["season_factor"]
        if season["consistency_factor"] >= 0.8:
            player["value_points"] += 8 * season["season_factor"]
        elif 0.8 > season["consistency_factor"] >= 0.6:
            player["value_points"] += 7 * season["season_factor"]
        elif 0.6 > season["consistency_factor"] >= 0.4:
            player["value_points"] += 6 * season["season_factor"]
        elif 0.4 > season["consistency_factor"] >= 0.2:
            player["value_points"] += 5 * season["season_factor"]
        elif 0.2 > season["consistency_factor"] > 0:
            player["value_points"] += 4 * season["season_factor"]


# get total number of players in each season from the cleaned data
for season in all_seasons:
    league_data[season]["total_players"] = len(load_data("filtered_players.json", "data"))


# get some important league data for each season
for player in players:
    for season in player["seasons"]:
        league_data[season["season"]]["all_players_effective_total_points"] += season["effective_total_points"]
        league_data[season["season"]]["all_players_minutes"] += season["minutes"]


# calculate all the required season stats for player comparison
for season in all_seasons:
    league_data[season]["avg_effective_total_points_per_player"] = league_data[season]["all_players_effective_total_points"] / league_data[season]["total_players"]
    league_data[season]["avg_minutes_per_player"] = league_data[season]["all_players_minutes"] / league_data[season]["total_players"]
    if season == variables.CURRENT_SEASON:
        league_data[season]["avg_minutes_per_player"] /= (next_event - 1)
    else:
        league_data[season]["avg_minutes_per_player"] /= 38


# calculate value points for each player in terms of amount of time they played, upcoming fixtures
max_value_points = 0
for player in players:
    for season in player["seasons"]:
        minutes_per_game = season["minutes"] / season["total_games"]
        if minutes_per_game >= 60:
            player["value_points"] += 4 * season["season_factor"]
        elif 60 > minutes_per_game >= league_data[season["season"]]["avg_minutes_per_player"]:
            player["value_points"] += 3 * season["season_factor"]
        elif 0 < minutes_per_game < league_data[season["season"]]["avg_minutes_per_player"]:
            player["value_points"] += 2 * season["season_factor"]
    if player["value_points"] > max_value_points:
        max_value_points = player["value_points"]


# normalize the fer
for player in players:
    player["fer"] /= max_fer_points


# normalize the value_points
for player in players:
    player["value_points"] /= max_value_points


# calculate value for each player for each season and then the overall value
for player in players:
    value = 0
    for season in player["seasons"]:
        season["value"] = season["effective_total_points"] / league_data[season["season"]]["avg_effective_total_points_per_player"]
        value += season["value"] * season["season_factor"]

    player["final_value"] = 53 * value + 27 * player["fer"] + 13.5 * player["consistency_overall"] + 9.5 * player["value_points"]
    player["final_value_per_cost"] = player["final_value"] / player["seasons"][0]["now_cost"]

# sort the players according to their value
final_players_sorted = sorted(players, key=lambda k: (-k["final_value"]))
save_data(final_players_sorted, "final_players_sorted.json", "data")

# save the league stats
save_data(league_data, "league_stats.json", "data")


print('Enhanced Player data.\n')
print('Enhanced Teams data.\n')
print('Enhanced Fixtures data.\n')
print('Added new stats Player\'s data.\n')
print('Extract data related to league.')