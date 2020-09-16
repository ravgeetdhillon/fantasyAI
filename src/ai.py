from helpers import load_data, get_next_gameweek_id
from notify import send_email, html_response
from random import shuffle
from time import time
import json
import variables
import numpy as np


# initialize the global variables
next_event = get_next_gameweek_id()
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


def get_main_players():
    """
    Returns the players that a manager is interested in.
    """

    return INTERESTED


def get_not_interested():
    """
    Returns the players that a manager is not interested in.
    """

    return NOT_INTERESTED


def display_team(team):
    """
    Writes the team onto a file or command line.
    """

    composition = {
        "Goalkeeper": [],
        "Defender": [],
        "Midfielder": [],
        "Forward": []
    }

    for player in team:
        composition[player["position"]].append(
            [player["full_name"], player["seasons"][0]["now_cost"]])

    result = ""
    for position in composition:
        result += f"\n{position}: "
        result += str(composition[position])

    print(result)
    return None


def get_estimated_points(team):
    """
    Gets estimated total points based on the previous history of players.
    """

    points = 0
    for player in team:
        points += player["seasons"][0]["total_points"]

    return CURRENT_POINTS + round(points * (38 - (next_event-1)) / (next_event-1))


def get_team_cost(team):
    """
    Gets the team"s cost.
    """

    cost = 0
    for player in team:
        cost += player["seasons"][0]["now_cost"]

    return round(cost, 2)


def get_formation(team):
    """
    Gets the formation of the team.
    """

    formation = [0, 0, 0]
    for player in team:
        if player["position"] == "Defender":
            formation[0] += 1
        elif player["position"] == "Midfielder":
            formation[1] += 1
        elif player["position"] == "Forward":
            formation[2] += 1

    formation = [str(x) for x in formation]

    return "-".join(formation)


def value_in_range(player1, player2):
    """
    Compares the `final_value` of two players and returns True if they are within a calculated range.
    """

    a = max(player1["final_value"], player2["final_value"])
    b = min(player1["final_value"], player2["final_value"])

    ans = (a - b) * 100 / a

    if ans <= limit["final_value_limit"]:
        return [True, player1 if max(player1["final_value"], player2["final_value"]) == player1["final_value"] else player2]
    else:
        return [False, player1 if max(player1["final_value"], player2["final_value"]) == player1["final_value"] else player2]


def budget_in_range(amount1, amount2):
    """
    Checks whether the player is in budget and returns True if so.
    """

    if amount2 < 0:
        return False
    elif amount2 < amount1:
        a = max(amount1, amount2)
        b = min(amount1, amount2)
        ans = (a - b) * 100 / a
        if ans <= limit["cost_limit"]:
            return True
        else:
            return False
    elif amount2 > amount1:
        return True


def value_points_in_range(player1, player2):
    """
    Compares the `value_points` of two players and returns True if they are within a calculated range.
    """

    a = max(player1["value_points"], player2["value_points"])
    b = min(player1["value_points"], player2["value_points"])

    ans = (a - b) * 100 / a

    if ans <= limit["value_points_limit"]:
        return [True, player1 if max(player1["value_points"], player2["value_points"]) == player1["value_points"] else player2]
    else:
        return [False, player1 if max(player1["value_points"], player2["value_points"]) == player1["value_points"] else player2]


def consistency_in_range(player1, player2):
    """
    Compares the `consistency` of two players and returns True if they are within a calculated range.
    """

    a = max(player1["consistency_overall"], player2["consistency_overall"])
    b = min(player1["consistency_overall"], player2["consistency_overall"])

    ans = (a - b) * 100 / a

    if ans <= limit["consistency_limit"]:
        return [True, player1 if max(player1["consistency_overall"], player2["consistency_overall"]) == player1["consistency_overall"] else player2]
    else:
        return [False, player1 if max(player1["consistency_overall"], player2["consistency_overall"]) == player1["consistency_overall"] else player2]


def player_with_easy_fixtures(player1, player2):
    """
    Gets the player with easier upcoming fixtures.
    """

    if player1["fer"] >= player2["fer"]:
        return player1
    else:
        return player2


def get_cover(player_type, final_team, configuration, new_player=""):
    """
    Checks whether a whole team can be bought in the budget if a buy is made that is bit costly but valuable to the team.
    """

    forward_cost = np.mean([player["seasons"][0]["now_cost"]
                            for player in players if player["position"] == "Forward" and player not in final_team])
    midfielder_cost = np.mean([player["seasons"][0]["now_cost"]
                               for player in players if player["position"] == "Midfielder" and player not in final_team])
    defender_cost = np.mean([player["seasons"][0]["now_cost"]
                             for player in players if player["position"] == "Defender" and player not in final_team])
    goalkeeper_cost = np.mean([player["seasons"][0]["now_cost"]
                               for player in players if player["position"] == "Goalkeeper" and player not in final_team])

    cover = 0
    for position in configuration:
        if position == "Goalkeeper":
            cover += configuration[position]["left"] * goalkeeper_cost
        elif position == "Defender":
            cover += configuration[position]["left"] * defender_cost
        elif position == "Midfielder":
            cover += configuration[position]["left"] * midfielder_cost
        elif position == "Forward":
            cover += configuration[position]["left"] * forward_cost

    if player_type == "Goalkeeper":
        cover -= goalkeeper_cost
    elif player_type == "Defender":
        cover -= defender_cost
    elif player_type == "Midfielder":
        cover -= midfielder_cost
    elif player_type == "Forward":
        cover -= forward_cost
    return cover


def select_player_from(position, final_team, configuration, budget, team_players_selected, donot_consider, picks=0):
    """
    Selects the players from a given lot based on the `final_value`.
    """

    if position == "Goalkeeper":
        global goalkeepers
        position = goalkeepers
    if position == "Defender":
        global defenders
        position = defenders
    if position == "Midfielder":
        global midfielders
        position = midfielders
    if position == "Forward":
        global forwards
        position = forwards

    for _ in range(picks):

        selected_players = []

        i = 0
        while len(selected_players) < 2 and i < len(position):

            cover = get_cover(position[0]["position"],
                              final_team, configuration)
            b = budget - position[i]["seasons"][0]["now_cost"]

            if budget_in_range(cover, budget - position[i]["seasons"][0]["now_cost"]):
                if position[i] not in final_team and budget > position[i]["seasons"][0]["now_cost"] and configuration[position[i]["position"]]["left"] > 0 and team_players_selected[position[i]["team_name"]] < 3 and position[i]["status"] == "a" and position[i] not in donot_consider and position[i] not in selected_players:

                    selected_players.append(position[i])

            else:
                donot_consider.append(position[i])

            i += 1

        if len(selected_players) == 1:
            return selected_players[0]

        elif len(selected_players) == 0:

            position = sorted(position, key=lambda k: (
                k['seasons'][0]['now_cost'], -k['final_value']))

            i = 0
            while position[i] in final_team:
                i += 1

            return selected_players[i]

        else:
            if value_in_range(selected_players[0], selected_players[1])[0]:
                if value_points_in_range(selected_players[0], selected_players[1]):

                    if consistency_in_range(selected_players[0], selected_players[1]):
                        return player_with_easy_fixtures(selected_players[0], selected_players[1])

                    else:
                        return consistency_in_range(selected_players[0], selected_players[1])[1]

                else:
                    return value_points_in_range(selected_players[0], selected_players[1])[1]

            else:
                return value_in_range(selected_players[0], selected_players[1])[1]


# load the all the players for team selection
players = load_data("final_players_sorted.json", "data")


# get range limits for each kind of variable
limit = {
    "cost_limit": np.var([player["seasons"][0]["now_cost"] for player in players]),
    "consistency_limit": np.var([player["consistency_overall"] for player in players]) * 100,
    "final_value_limit": np.var([player["final_value"] for player in players]) / 1000,
    "value_points_limit": np.var([player["value_points"] for player in players]) * 100,
    "variance_points_limit": np.var([player["fer"] for player in players]) * 100,
}


# select players according to their playing positions
goalkeepers = [
    player for player in players if player["position"] == "Goalkeeper"]
forwards = [player for player in players if player["position"] == "Forward"]
midfielders = [
    player for player in players if player["position"] == "Midfielder"]
defenders = [player for player in players if player["position"] == "Defender"]


def get_best_playing_11_points(final_team):
    """
    Select the best playing eleven with the most suitable formation and returns the estimated points of the team at the end of the season.
    """

    final_team = sorted(
        final_team, key=lambda k: k["final_value"], reverse=True)
    formations = variables.formations()

    max_points = 0
    final_playing_team = []

    for formation in formations:

        playing_team = []
        for player in final_team:

            if formation[player["position"]] > 0:
                playing_team.append(player)
                formation[player["position"]] -= 1

        points = get_estimated_points(playing_team)

        if points > max_points:
            max_points = points

    return max_points


def get_player_cost(player_name):
    """
    Gets the player"s cost.
    """

    for player in players:
        if player["full_name"] == player_name:
            return player["seasons"][0]["now_cost"]
    return 0


def create_team(omit_player=None, iterations=variables.ITERATIONS, display=True):
    """
    Creates the final squad of 15 players and gives an estimated points at the end of the season.
    """

    positions = ["Forward"]*3 + ["Midfielder"] * \
        5 + ["Defender"]*5 + ["Goalkeeper"]*2

    main_players = get_main_players()

    for player in players:
        if player["full_name"] in main_players and player["full_name"] != omit_player:
            positions.remove(player["position"])

    best_team = []
    max_points = -1

    for x in range(iterations):

        configuration = variables.configuration()
        budget = BUDGET
        team_players_selected = variables.team_players_selected()
        final_team = []
        donot_consider = []

        # add players to the final_team that are user"s favorite
        main_players = get_main_players()
        for player in players:
            if player["full_name"] in main_players and player["full_name"] != omit_player:
                budget -= player["seasons"][0]["now_cost"]
                configuration[player["position"]]["left"] -= 1
                team_players_selected[player["team_name"]] += 1
                final_team.append(player)

        # add players, which user is not interesed in, to donot consider
        not_interested = get_not_interested()
        for player in players:
            if player["full_name"] in not_interested:
                donot_consider.append(player)

        shuffle(positions)

        for p in positions:
            player = select_player_from(
                p, final_team, configuration, budget, team_players_selected, donot_consider, 1)
            budget -= player["seasons"][0]["now_cost"]
            configuration[player["position"]]["left"] -= 1
            team_players_selected[player["team_name"]] += 1
            final_team.append(player)

        points = get_best_playing_11_points(final_team)

        if points > max_points:
            max_points = points
            best_team = final_team

    return (best_team, max_points)


def get_transfers():
    """
    Get"s the best single transfer.
    """

    current_team_expected_points = create_team(iterations=1)[1]
    main_players = get_main_players()

    max_points = -1
    best_transfers = []

    for y in range(len(main_players)):
        omit_player = main_players[y]
        best_team, points = create_team(
            omit_player, iterations=1, display=False)

        if points > max_points:
            max_points = points

        for player in best_team:
            if player["full_name"] not in main_players:
                best_transfers.append(
                    {
                        "out": {
                            "name": omit_player,
                            "cost": get_player_cost(omit_player),
                        },
                        "in": {
                            "name": player["full_name"],
                            "cost": get_player_cost(player["full_name"]),
                        },
                        "points": points,
                        "g/l": points - current_team_expected_points,
                    }
                )
                break

    best_transfers = sorted(best_transfers, key=lambda k: (-k["points"]))
    return best_transfers


def main():
    """
    Main function of ai.py
    """

    # get transfers
    transfers = get_transfers()
    print(f"Evaluated {len(transfers)} transfers.\n")

    # write a CLI response
    for transfer in transfers:
        print(transfer['out']['name'], transfer['out']['cost'])
        print(transfer['in']['name'], transfer['in']['cost'])
        print(transfer['g/l'])
        print('-------')

    # generate response to be sent
    response = html_response(transfers)

    # send email
    send_email(response)
    print(f"Email sent.")


if __name__ == "__main__":
    main()
