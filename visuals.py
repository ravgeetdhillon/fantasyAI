import json
import numpy as np
import pandas as pd
import plotly.express as px
import variables
import plotly.graph_objects as go

# # load players for data visualisation
with open(f'data/final_players_sorted.json', 'r') as f:
    players = json.load(f)


# calculate some entities to compare
forward_value = np.mean([player['final_value'] for player in players if player['position'] == 'Forward'])
forward_value_per_cost = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Forward'])
forward_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Forward'])

midfielder_value = np.mean([player['final_value'] for player in players if player['position'] == 'Midfielder'])
midfielder_value_per_cost = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Midfielder'])
midfielder_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Midfielder'])

defender_value = np.mean([player['final_value'] for player in players if player['position'] == 'Defender'])
defender_value_per_cost = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Defender'])
defender_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Defender'])

goalkeeper_value = np.mean([player['final_value'] for player in players if player['position'] == 'Goalkeeper'])
goalkeeper_value_per_cost = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Goalkeeper'])
goalkeeper_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Goalkeeper'])


# load players into a dataframe
players = pd.DataFrame(players)
# # players based on value for each team
fig = px.scatter(players, y="team_name", x="final_value", color="position", hover_data=['full_name'], size = "value_points", labels={'team_name':'Teams', 'final_value':'Value', 'position':'Position'})
fig.show()


# players based on value_per_cost for each team
fig = px.scatter(players, y="team_name", x="final_value_per_cost", color="position", hover_data=['full_name'], size = "value_points", labels={'team_name':'Teams', 'final_value_per_cost':'Value per Cost', 'position':'Position'})
fig.show()


# which type of players are better based on `final_value`
fig = px.scatter(players, y="final_value", x="position", color="team_name", hover_data=['full_name'], size = "value_points", labels={'final_value':'Value', 'position':'Position'})
fig.show()


# which type of players are better based on `final_value_per_cost`
fig = px.scatter(players, y="final_value_per_cost", x="position", color="team_name", hover_data=['full_name'], size = "value_points", labels={'final_value_per_cost':'Value per Cost', 'position':'Position'})
fig.show()


positions = [
    {
        'type': 'Forward',
        'mean_value': forward_value,
        'mean_value_per_cost': forward_value_per_cost,
        'mean_cost': forward_cost,
    },
    {
        'type': 'Midfielder',
        'mean_value': midfielder_value,
        'mean_value_per_cost': midfielder_value_per_cost,
        'mean_cost': midfielder_cost,
    },
    {
        'type': 'Defender',
        'mean_value': defender_value,
        'mean_value_per_cost': defender_value_per_cost,
        'mean_cost': defender_cost,
    },
    {
        'type': 'Goalkeeper',
        'mean_value': goalkeeper_value,
        'mean_value_per_cost': goalkeeper_value_per_cost,
        'mean_cost': goalkeeper_cost,
    }
]

# compare positions based on value per cost
positions = pd.DataFrame(positions)
fig = px.bar(positions, x='type', y='mean_value_per_cost', color='type', labels={'mean_value_per_cost':'Avg. Value per Cost', 'type':'Position'}, height=500)
fig.show()


# compare positions based on cost
fig = px.bar(positions, x='type', y='mean_value', color='type', labels={'mean_value':'Avg. Value', 'type':'Position'}, height=500)
fig.show()


# compare positions based on cost
fig = px.bar(positions, x='type', y='mean_cost', color='type', labels={'mean_cost':'Avg. Cost', 'type':'Position'}, height=500)
fig.show()


# compare your progress
progress = variables.progress()
fig = go.Figure()
for p in progress:
    fig.add_trace(go.Scatter(x=p['gameweek'], y=p['points'], mode='lines', name=p['type']))
fig.update_layout(yaxis_title='Points', xaxis_title='Gameweek')
fig.show()
