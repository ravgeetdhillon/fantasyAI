import json
import numpy as np
import pandas as pd
import plotly.express as px


with open(f'data/final_players_sorted.json', 'r') as f:
    players = json.load(f)


forward = np.mean([player['final_value_per_cost'] for player in players if player
['position'] == 'Forward'])

midfielder = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Midfielder'])

defender = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Defender'])

goalkeeper = np.mean([player['final_value_per_cost'] for player in players if player['position'] == 'Goalkeeper'])

positions = [
    {
        'type': 'Forwards',
        'mean': forward,
    },
    {
        'type': 'Midfielders',
        'mean': midfielder,
    },
    {
        'type': 'Defenders',
        'mean': defender,
    },
    {
        'type': 'Goalkeepers',
        'mean': goalkeeper
    }
]

players = pd.DataFrame(players)

# players that are most reliable on most of the factors
fig = px.scatter(players, y="team_name", x="final_value", color="position", hover_data=['full_name'], size = "value_points", labels={'team_name':'Teams', 'final_value':'Value'})
fig.show()

# players that are most reliable on value_per_cost
fig = px.scatter(players, y="team_name", x="final_value_per_cost", color="position", hover_data=['full_name'], size = "value_points", labels={'team_name':'Teams', 'final_value':'Value'})
fig.show()

# players according value points
fig = px.scatter(players, y="team_name", x="value_points", color="position", hover_data=['full_name'], size = "value_points", labels={'team_name':'Teams', 'value_points':'Value Points'})
fig.show()

# which type of players are better
# fig = px.scatter(players, y="final_value_per_cost", x="position", color="position", hover_data=['full_name'], size = "value_points", labels={'final_value_per_cost':'Value per cost', 'position':'Positions'})
# fig.show()

# which type has more value per cost
# positions = pd.DataFrame(positions)
# fig = px.bar(positions, x='type', y='mean', color='type', labels={'mean':'Avg. Value per cost'}, height=500)
# fig.show()
