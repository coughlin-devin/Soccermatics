import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)

# %% markdown
# ### Preparing the data
# Take succesful passes from England Women excluding Throw-ins, Free-kicks, etc.
# Need the passing position data and player names. We will annotate by surname.

# %% codecell
# check for inedx of first substitution
sub = df.loc[(df['type_name'] == 'Substitution') & (df['team_name'] == "England Women's")].iloc[0]['index']
# mask for England's successful passes (assuming unsuccesful passes not recorded in pass data)
mask_england = (df.type_name == 'Pass') & (df.team_name == "England Women's") & (df.index < sub) & (df.outcome_name.isnull()) & (df.sub_type_name != 'Throw-in')
england_passes = df.loc[mask_england, ['x','y','end_x','end_y','player_name','pass_recipient_name']]

# only want to display player surnames
england_passes['surname'] = england_passes['player_name'].apply(lambda x: x.split()[-1])
england_passes['pass_recipient_surname'] = england_passes['pass_recipient_name'].apply(lambda x: x.split()[-1])

# %% markdown
# ### Calculating vertices size and location
# For each player calculate the average location of passes made by each player.
# Calculate the vertice size to be proportional to the number of passes.

# %% codecell
# group by passer and reciever
pass_location = england_passes.groupby('surname').mean()
recieve_location = england_passes.groupby('pass_recipient_surname').mean()

# calculate pass counts
pass_count = england_passes.groupby('surname').count().iloc[:,1].rename('pass_count')

# join into one dataframe
mean_location = pass_location.join(recieve_location, on=None, how='inner', rsuffix='_recieve')
mean_location = mean_location.join(pass_count, on=None, how='inner').reset_index()

# calculate average of passing position and recieving position for each player
# this give an idea of average position while participating in the passing network
mean_location['mean_x'] = mean_location[['x','end_x_recieve']].mean(axis=1)
mean_location['mean_y'] = mean_location[['y','end_y_recieve']].mean(axis=1)

# normalize vertice size
mean_location['vertice_size'] = mean_location['pass_count'] / mean_location['pass_count'].max() * 1500

# %% markdown
# ### Calculating edge widths
# Count passes between each pair of players
# Set threshold ignoring players that made fewer than N number of passes.

# %% codecell
# NOTE create a key-pair column by sorting by each key (surnames) and combining them into one
england_passes['pair_key'] = england_passes.apply(lambda x: "_".join(sorted([x.surname, x.pass_recipient_surname])), axis=1)
passing_pairs = england_passes.groupby('pair_key', as_index=False).count().iloc[:,:2].rename({'x':'pass_count'}, axis=1)
passing_pairs['line_width'] = passing_pairs['pass_count'] / passing_pairs['pass_count'].max() * 10
passing_pairs = passing_pairs.loc[passing_pairs['pass_count'] > 2]

# %% markdown
# ### Plotting Vertices
# ### Plotting Edges
# For each pair of players who passed to each other get start and end of the edge.
# Then adjust the line width so that is is proportional to the number of passes between them.
# It looks better if the zorder of the edge is below the vertice.

# %% codecell
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.scatter(mean_location.mean_x, mean_location.mean_y, s=mean_location.vertice_size, zorder=2,
                color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax['pitch'])
for player in mean_location.itertuples():
    pitch.annotate(player.surname, xy=(player.mean_x,player.mean_y), zorder=3, c='black',
                    va='center', ha='center', weight='bold', size=16, ax=ax['pitch'])

for pair in passing_pairs.itertuples():
    players = pair.pair_key.split("_")
    passer = players[0]
    recipient = players[1]
    passer_x = mean_location.loc[mean_location['surname'] == passer].mean_x.iloc[0]
    passer_y = mean_location.loc[mean_location['surname'] == passer].mean_y.iloc[0]
    recipient_x = mean_location.loc[mean_location['surname'] == recipient].mean_x.iloc[0]
    recipient_y = mean_location.loc[mean_location['surname'] == recipient].mean_y.iloc[0]
    pitch.lines(passer_x, passer_y, recipient_x, recipient_y, alpha=1, lw=pair.line_width, zorder=1, color='red', ax=ax['pitch'])

fig.suptitle("England Passing Network against Sweden", fontsize = 30)
plt.show()

# %% markdown
# ### Plotting a directed passing network.
# The advantage of this graph is it shows the direction of the pass between two players, who passes more often and who recieves more often.
# However, it is not reccomended to make inferences about how positive each players distribution was from this graph because each player's position is
# their average position when making or recieving a pass. A 'forward' pass here is not gauranteed to actually have been a forward pass in the game.
# Using individual pass maps will give a more accurate depiction of where each player passes the ball.

# %% codecell
directed_pairs = england_passes.groupby(['surname', 'pass_recipient_surname'], as_index=False).count().iloc[:,:3].rename({'x':'pass_count'}, axis=1)
directed_pairs['arrow_width'] = directed_pairs['pass_count'] / directed_pairs['pass_count'].max() * 20

pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box')
fig, ax = pitch.draw(figsize=(20,14))

pitch.scatter(mean_location.mean_x, mean_location.mean_y, s=mean_location.vertice_size, zorder=3,
                color='gold', linewidth=1, alpha=1, ax=ax)
for player in mean_location.itertuples():
    pitch.annotate(player.surname, xy=(player.mean_x,player.mean_y), zorder=4, c='black',
                    va='center', ha='center', weight='bold', size=16, ax=ax)

for passer in directed_pairs.itertuples():
    passer_x = mean_location.loc[mean_location['surname'] == passer.surname].mean_x.iloc[0]
    passer_y = mean_location.loc[mean_location['surname'] == passer.surname].mean_y.iloc[0]
    recipient_x = mean_location.loc[mean_location['surname'] == passer.pass_recipient_surname].mean_x.iloc[0]
    recipient_y = mean_location.loc[mean_location['surname'] == passer.pass_recipient_surname].mean_y.iloc[0]
    # NOTE Indicates direction of the pass between players only. Actual direction of passing is uncertain because player position is
    #      mean position when making or recieving a pass.
    if (passer_x < recipient_x):
        forward = pitch.lines(passer_x, passer_y, recipient_x, recipient_y, alpha=0.5, lw=passer.arrow_width, zorder=2, color='yellow', label='Forward Pass', ax=ax)
    else:
        backward = pitch.lines(passer_x, passer_y, recipient_x, recipient_y, alpha=1, lw=passer.arrow_width, zorder=1, color='maroon', label='Backward Pass', ax=ax)

plt.title("England Passing Network against Sweden")
plt.legend(handles=[backward, forward])
plt.show()

# %% markdown
# ### Centralisation
# The centralisation index numerator is calculated by taking the sum of the difference between
# maximal number of successful passes by one player and the number of succesful passes by each player.
# The denominator is the sum of all passes multiplied by (number of players - 1).
# Thomas Grund (2012) defines the index as: C = SUM<i-11>(P_max - P_i) / (N-1)SUM<i-11>(P_i)
# where N = number of players (11). Read more at
# Grund, Thomas U. “Network structure and team performance: The case of English Premier League soccer teams.” Social Networks 34.4 (2012): 682–690.

# %% codecell
def centralisation(passing_data, players=11):
    max_passes = max(passing_data)
    numerator = (max_passes - passing_data).sum()
    denominator = (players-1) * pass_count.sum()
    centralisation_index = numerator / denominator
    return centralisation_index

centralisation_index = centralisation(pass_count)
print("Centralisation index is ", centralisation_index)

pairs = england_passes.groupby('pair_key', as_index=False).count().iloc[:,:2].rename({'x':'pass_count'}, axis=1)
pairs_no_keeper = pairs.loc[pairs['pair_key'].str.contains('Telford') == False]
centralisation_no_keeper = centralisation(pairs_no_keeper.pass_count, 10)
print("Centralisation index excluding the goalkeeper is ", centralisation_no_keeper)

# %% markdown
# ### Network Density
# Exploring the density of the passing network as both a directed and undirected graph.
# Literature states teams with more dense networks tend to perform better.
# I will look at the networks both including and excluding the goalkeeper.
# ## Directed Network

# %% codecell
N = 11 # number of players

# Directed Potential Network Density
fully_connected = N*(N-1)
field_10 = (N-1)*(N-2)
directed_pairs = england_passes.groupby(['surname', 'pass_recipient_surname'], as_index=False).count().iloc[:,:3].rename({'x':'pass_count'}, axis=1)
density = directed_pairs.pass_count.count()/fully_connected

exclude_keeper = directed_pairs.loc[(directed_pairs['surname'] != 'Telford') & (directed_pairs['pass_recipient_surname'] != 'Telford')]
field_10_density = exclude_keeper.pass_count.count()/field_10

print(f"Directed network density is: {density}")
print(f"Directed network density without the goalkeeper is: {field_10_density}")

# %% markdown
# ## Undirected Network

# %% codecell
# Undirected Potential Network Density
fully_connected = directed_fully_connected/2
field_10 = directed_no_goalkeeper/2
undirected_pairs = england_passes.groupby('pair_key', as_index=False).count().iloc[:,:2].rename({'x':'pass_count'}, axis=1)
density = undirected_pairs.pass_count.count()/fully_connected

exclude_keeper = undirected_pairs.loc[undirected_pairs['pair_key'].str.contains('Telford') == False]
field_10_density = exclude_keeper.pass_count.count() / field_10

print(f"Undirected network density is: {density}")
print(f"Undirected network density without the goalkeeper is: {field_10_density}")

# %% markdown
# ### Who is the Hub
# Which player(s) is the most connected passer?

# %% codecell
passing_involvments = {}
for player in directed_pairs.surname.unique():
    passing_involvments.update({player:directed_pairs.loc[(directed_pairs['surname'] == player) | (directed_pairs['pass_recipient_surname'] == player)].pass_count.sum()})
print(f"Passing involvments by each player {passing_involvments}")

# %% markdown
# ### Challenge
# Make a passing network of only forward passes for England

# %% codecell
