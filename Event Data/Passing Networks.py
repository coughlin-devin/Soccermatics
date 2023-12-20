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

# WARNING using apply with lambda function may have poor performance
# only want to display player surnames
england_passes['surname'] = england_passes['player_name'].apply(lambda x: x.split()[-1])
england_passes['pass_recipient_surname'] = england_passes['pass_recipient_name'].apply(lambda x: x.split()[-1])

# %% markdown
# ### Calculating vertices size and location
# For each player calculate the average location of passes made by each player.
# Calculate the marker size to be proportional to the number of passes.

# %% codecell
# group by passer and reciever
pass_location = england_passes.groupby('surname').mean()
recieve_location = england_passes.groupby('pass_recipient_surname').mean()

# calculate pass counts
pass_count = england_passes.groupby('surname').count().iloc[:,1].rename('pass_count')

# join into one dataframe
mean_location = pass_location.join(recieve_location, on=None, how='inner', rsuffix='_recieve')
mean_location = mean_location.join(pass_count, on=None, how='inner')

# calculate average of passing position and recieving position for each player
# this give an idea of average position while participating in the passing network
mean_location['mean_x'] = mean_location[['x','end_x_recieve']].mean(axis=1)
mean_location['mean_y'] = mean_location[['y','end_y_recieve']].mean(axis=1)

# normalize marker size
mean_location['marker_size'] = mean_location['pass_count'] / mean_location['pass_count'].max() * 1500

# %% markdown
# ### Calculating edge widths
# Count passes between each pair of players
# Set threshold ignoring players that made fewer than N number of passes.

# %% codecell
# df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
# lines_df = df_pass.groupby(["pair_key"]).x.count().reset_index()
# lines_df.rename({'x':'pass_count'}, axis='columns', inplace=True)
# #setting a treshold. You can try to investigate how it changes when you change it.
# lines_df = lines_df[lines_df['pass_count']>2]

passing_pairs = england_passes.groupby(['player_name', 'pass_recipient_name'], as_index=False).count().iloc[:,:3].rename({'x':'pass_count'}, axis=1)
# TODO Combine passing pairs so Bronze-Houghton and Houghton-Bronze are a directionless pass count
# NOTE This is essentially how to turn a weighted directed graph into an undirected graph
# IDEA Could plot a directed graph instead of an undirected graph
passing_pairs


# %% markdown
# ### Plotting Vertices

# %% codecell
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.scatter(mean_location.mean_x, mean_location.mean_y, s=mean_location.marker_size,
                color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax['pitch'])
for player in mean_location.itertuples():
    pitch.annotate(player.Index, xy=(player.mean_x,player.mean_y), c='black', va='center', ha='center', weight='bold', size=16, ax=ax['pitch'])

fig.suptitle("Nodes location - England", fontsize=30)
plt.show()

# %% markdown
# ### Plotting Edges
