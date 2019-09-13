#!/usr/bin/env python
# coding: utf-8

# In[18]:


import json
import numpy as np
import pandas as pd
import plotly.express as px
import variables
import plotly.graph_objects as go


# In[19]:


# load players for data visualisation
with open(f'data/final_players_sorted.json', 'r') as f:
    org_players = json.load(f)
with open(f'data/teams_cleaned.json', 'r') as f:
    org_teams = json.load(f)
    
players = org_players[:]
for player in players:
    player['points'] = 0
    for season in player['seasons']:
        player['points'] += season['effective_total_points'] * season['season_factor']
    player['cost'] = player['seasons'][0]['now_cost']
    player['pc'] = player['points'] / player['seasons'][0]['now_cost']
    if player['pc'] < 0:
        player['pc'] = 0
        
        


# In[20]:


# load players for data visualisation
with open(f'data/final_players_sorted.json', 'r') as f:
    org_players = json.load(f)
    
players = org_players[:]
for player in players:
    player['points'] = 0
    for season in player['seasons']:
        player['points'] += season['effective_total_points'] * season['season_factor']
    player['cost'] = player['seasons'][0]['now_cost']
    player['pc'] = player['points'] / player['seasons'][0]['now_cost']
    if player['pc'] < 0:
        player['pc'] = 0


# In[21]:


# calculate some entities to compare
forward_effective_points = np.mean([player['points'] for player in players if player['position'] == 'Forward'])
forward_effective_points_per_cost = np.mean([player['pc'] for player in players if player['position'] == 'Forward'])
forward_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Forward'])

midfielder_effective_points = np.mean([player['points'] for player in players if player['position'] == 'Midfielder'])
midfielder_effective_points_per_cost = np.mean([player['pc'] for player in players if player['position'] == 'Midfielder'])
midfielder_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Midfielder'])

defender_effective_points = np.mean([player['points'] for player in players if player['position'] == 'Defender'])
defender_effective_points_per_cost = np.mean([player['pc'] for player in players if player['position'] == 'Defender'])
defender_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Defender'])

goalkeeper_effective_points = np.mean([player['points'] for player in players if player['position'] == 'Goalkeeper'])
goalkeeper_effective_points_per_cost = np.mean([player['pc'] for player in players if player['position'] == 'Goalkeeper'])
goalkeeper_cost = np.mean([player['seasons'][0]['now_cost'] for player in players if player['position'] == 'Goalkeeper'])


# In[22]:


# load players into a dataframe
players = pd.DataFrame(players)
# players based on effective points for each team
fig = px.scatter(players, y='team_name', x='points', color='position', hover_data=['full_name'], size = 'pc', labels={'team_name':'Teams', 'points':'Points', 'position':'Position', 'pc':'Points per Cost'})
fig.update_layout(title='Teams and their points')
fig.show()


# In[23]:


# players based on effective points per cost for each team
fig = px.scatter(players, y='team_name', x='pc', color='position', hover_data=['full_name','value_points'], size = 'pc', labels={'team_name':'Teams', 'points':'Points', 'position':'Position', 'pc':'Points per Cost'})
fig.update_layout(title='Teams and their points per cost')
fig.show()


# In[24]:


# which type of players are better based on effective points
fig = px.scatter(players, y='points', x='position', color='team_name', hover_data=['full_name'], size = 'pc', labels={'points':'Points', 'position':'Position', 'pc':'Points per Cost'})
fig.update_layout(title='Positions and their points')
fig.show()


# In[25]:


# which type of players are better based on effective points per cost
fig = px.scatter(players, y='pc', x='position', color='team_name', hover_data=['full_name'], size = 'pc', labels={'points':'Points', 'position':'Position', 'pc':'Points per Cost'})
fig.update_layout(title='Positions and their points per cost')
fig.show()


# In[26]:


positions = [
    {
        'type': 'Forward',
        'mean_points': forward_effective_points,
        'mean_points_per_cost': forward_effective_points_per_cost,
        'mean_cost': forward_cost,
    },
    {
        'type': 'Midfielder',
        'mean_points': midfielder_effective_points,
        'mean_points_per_cost': midfielder_effective_points_per_cost,
        'mean_cost': midfielder_cost,
    },
    {
        'type': 'Defender',
        'mean_points': defender_effective_points,
        'mean_points_per_cost': defender_effective_points_per_cost,
        'mean_cost': defender_cost,
    },
    {
        'type': 'Goalkeeper',
        'mean_points': goalkeeper_effective_points,
        'mean_points_per_cost': goalkeeper_effective_points_per_cost,
        'mean_cost': goalkeeper_cost,
    }
]


# In[27]:


# compare positions based on average effective points
positions = pd.DataFrame(positions)
fig = px.bar(positions, x='type', y='mean_points', color='type', labels={'mean_points':'Avg. Points', 'type':'Position'}, height=500)
fig.update_layout(title='Positions and their Avg. Points')
fig.show()


# In[28]:


# compare positions based on their average effective points per cost
fig = px.bar(positions, x='type', y='mean_points_per_cost', color='type', labels={'mean_points_per_cost':'Avg. Points per Cost', 'type':'Position'}, height=500)
fig.update_layout(title='Positions and their Avg. Points per Cost')
fig.show()


# In[29]:


# compare positions based on average cost
fig = px.bar(positions, x='type', y='mean_cost', color='type', labels={'mean_cost':'Avg. Cost', 'type':'Position'}, height=500)
fig.update_layout(title='Positions and their Avg. Cost')
fig.show()


# In[35]:


# compare your progress
progress = variables.progress()
fig = go.Figure()
for p in progress:
    fig.add_trace(go.Scatter(x=p['gameweek'], y=p['points'], mode='lines', name=p['type']))
fig.update_layout(yaxis_title='Points', xaxis_title='Gameweek', title='Performance Comparison')
fig.show()


# In[31]:


# distribution of players' effective points vs cost
fig = px.scatter(players, y='points', x='cost', color='position', size='pc', hover_data=['full_name'], labels={'full_name':'Full Name', 'points':'Points', 'cost':'Cost', 'pc':'Points per Cost', 'position':'Position'})
fig.update_layout(title='Effective Points vs Cost')
fig.show()


# In[32]:


players = players.to_json(orient='records')
players = json.loads(players)


# In[41]:


teams = []
for team in org_teams:
    t = {'name': team['name'], 'points': 0, 'cost': 0}
    teams.append(t)
for player in players:
    for team in teams:
        if player['team_name'] == team['name']:
            team['points'] += player['points']
            team['cost'] += player['cost']

for team in teams:
    team['pc'] = team['points'] / team['cost']
            
teams = sorted(teams, key=lambda k: -k['pc'])
teams = pd.DataFrame(teams)
fig = go.Figure(data=[
    go.Bar(name='Points', x=teams['name'], y=teams['points']),
    go.Bar(name='Cost', x=teams['name'], y=teams['cost']),
])
fig.update_layout(xaxis_title='Teams', title='Teams\' Total Effective Points and Cost', barmode='group')
fig.show()

