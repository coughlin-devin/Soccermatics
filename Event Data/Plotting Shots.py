import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, Sbopen

# %% markdown
# ### Opening the dataset.

# %% codecell
# Statsbomb parser
parser = Sbopen()
# get match from match id
df, related, freeze, tactics = parser.event(69301)
team1, team2 = df.team_name.unique()
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

# %% markdown
# ### EDA.

# %% codecell

shots.info()
shots.head()
shots.describe()
shots.describe(include='object')

# %% markdown
# ### Making shot map.
# In this exampel we iterate thorugh each shot and check it's x and y coordinates, team, and outcome,
# before plotting it accordingly. This is ok for a small dataset like one match,
# but iterating through dataframe rows is usually inefficient.

# %% codecell
pitch_length = 120 # x
pitch_width = 80 # y
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(10,7))

#set circlesize
circle_size=2
for shot in shots.itertuples():
    #get the information
    x=shot.x
    y=shot.y
    goal=shot.outcome_name=='Goal'
    team_name=shot.team_name
    #plot England
    if (team_name==team1):
        if goal:
            shot_circle=plt.Circle((x,y),circle_size,color="red")
            plt.text(x+1,y-2,shot.player_name)
        else:
            shot_circle=plt.Circle((x,y),circle_size,color="red")
            shot_circle.set_alpha(.2)
    #plot Sweden
    else:
        if goal:
            shot_circle=plt.Circle((pitch_length-x,pitch_width-y),circle_size,color="blue")
            plt.text(pitch_length-x+1,pitch_width-y-2 ,shot.player_name)
        else:
            shot_circle=plt.Circle((pitch_length-x,pitch_width-y),circle_size,color="blue")
            shot_circle.set_alpha(.2)
    ax.add_patch(shot_circle)
fig
#set title
fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 24)
fig.set_size_inches(10, 7)
plt.show()

# %% markdown
# ### Using mplsoccers Pitch class.
#

# %% codecell
# create pitch
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)

# query
mask_england = (df.type_name == 'Shot') & (df.team_name == team1)
# finding rows in the df and keeping only necessary columns
df_england = df.loc[mask_england, ['x', 'y', 'outcome_name', 'player_name']]

for shot in df_england.itertuples():
    if shot.outcome_name == 'Goal':
        pitch.scatter(shot.x, shot.y, alpha=1, s=500, color='red', ax=ax['pitch'])
        pitch.annotate(shot.player_name, (shot.x + 1, shot.y - 2), ax=ax['pitch'], fontsize=12)
    else:
        pitch.scatter(shot.x, shot.y, alpha=0.2, s=500, color='red', ax=ax['pitch'])

mask_sweden = (df.type_name == 'Shot') & (df.team_name == team2)
mask_sweden = df.loc[mask_sweden, ['x', 'y', 'outcome_name', 'player_name']]

for shot in mask_sweden.itertuples():
    if shot.outcome_name == 'Goal':
        pitch.scatter(pitch_length-shot.x, pitch_width-shot.y, alpha=1, s=500, color='blue', ax=ax['pitch'])
        pitch.annotate(shot.player_name, (pitch_length - shot.x + 1, pitch_width - shot.y - 2), ax=ax['pitch'], fontsize=12)
    else:
        pitch.scatter(pitch_length - shot.x, pitch_width - shot.y, alpha=0.2, s=500, color='blue', ax=ax['pitch'])

fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 30)
plt.show()

# %% markdown
# ### Plotting shots in one half of the field.
#

# %% codecell
pitch = VerticalPitch(pitch_color='grass', line_color='white', goal_type='box', stripe=True, half=True)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

#plotting all england shots
pitch.scatter(df_england.x, df_england.y, alpha = 1, s = 500, color = "red", ax=ax['pitch'], edgecolors="black")
fig.suptitle("England shots against Sweden", fontsize = 30)
plt.show()

# %% markdown
# ### Challenge.
# 1. Create a dataframe of passes which contains all the passes in the match
# 2. Plot the start point of every Sweden pass. Attacking left to right.
# 3. Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database)
# 4. Plot arrows to show where the passes went to.

# %% codecell
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(20,14))

passes = df.loc[df['type_name'] == 'Pass']
for p in passes.itertuples():
    # if Sweden pass
    if p.team_name == team2:
        if p.player_name == 'Sara Caroline Seger':
            seger = pitch.scatter(p.x, p.y, alpha=1, s=250, color='blue', ax=ax, label='Caroline')
            #pitch.annotate(p.player_name, (p.x+1, p.y-2), ax=ax, fontsize=12)
        else:
            sweden = pitch.scatter(p.x, p.y, alpha=0.5, s=250, color='yellow', ax=ax, label='Sweden')
        pitch.arrows(p.x, p.y, p.end_x, p.end_y, ax=ax, alpha=0.35, color='black', width=2, headwidth=5)

plt.title('Sweden Passes')
plt.legend(handles=[seger, sweden])
plt.show()

# %% markdown
# ### Challenge done non-iteratively (No for-loop).
# %% codecell

pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(20,14))

seger_mask = (df.type_name == 'Pass') & (df.player_name == 'Sara Caroline Seger')
seger_passes = df.loc[seger_mask, ['x', 'y', 'end_x', 'end_y']]
sweden_mask = (df.type_name == 'Pass') & (df.team_name == team2) & (df.player_name != 'Sara Caroline Seger')
sweden_passes = df.loc[sweden_mask, ['x', 'y', 'end_x', 'end_y']]

seger_plot = pitch.scatter(seger_passes.x, seger_passes.y, alpha=1, s=250, color='blue', ax=ax, label='Caroline')
seger_arrows = pitch.arrows(seger_passes.x, seger_passes.y, seger_passes.end_x, seger_passes.end_y, ax=ax, alpha=1, color='blue', width=2, headwidth=5)
sweden_plot = pitch.scatter(sweden_passes.x, sweden_passes.y, alpha=0.5, s=250, color='yellow', ax=ax, label='Sweden')
sweden_arrows = pitch.arrows(sweden_passes.x, sweden_passes.y, sweden_passes.end_x, sweden_passes.end_y, ax=ax, alpha=0.35, color='black', width=2, headwidth=5)

plt.title('Sweden Passes')
plt.legend(handles=[seger_plot, sweden_plot])
plt.show()
