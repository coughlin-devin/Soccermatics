# %% markdown
# ### Open Data

# %% codecell
# importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen

parser = Sbopen()
df, related, freeze, tactics = parser.event(69301)
passes = df.loc[(df['type_name'] == 'Pass') & (df['sub_type_name'] != 'Throw-in')].set_index('id')

# %% markdown
# ### Plotting passes iteratively
# Using a for loop to plot each pass.

# %%  codecell
#drawing pitch
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box')
fig, ax = pitch.draw(figsize=(10,7))

for thepass in passes.itertuples():
    #if pass made by Lucy Bronze
    if thepass.player_name=='Lucy Bronze':
        x=thepass.x
        y=thepass.y
        #plot circle
        passCircle=plt.Circle((x,y),2,color="blue")
        passCircle.set_alpha(.2)
        ax.add_patch(passCircle)
        dx=thepass.end_x-x
        dy=thepass.end_y-y
        #plot arrow
        passArrow=plt.Arrow(x,y,dx,dy,width=3,color="blue")
        ax.add_patch(passArrow)

ax.set_title("Lucy Bronze passes against Sweden", fontsize = 24)
fig.set_size_inches(10, 7)
plt.show()

# %% markdown
# ### Plotting passes in parallel
# Plotting all passes at once without a for loop.

# %% codecell
mask_bronze = (df.type_name == 'Pass') & (df.player_name == "Lucy Bronze")
df_pass = df.loc[mask_bronze, ['x', 'y', 'end_x', 'end_y']]

pitch = Pitch(pitch_color='grass', line_color='white', stripe=True, goal_type='box')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
pitch.arrows(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, color = "blue", ax=ax['pitch'])
pitch.scatter(df_pass.x, df_pass.y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch'])
fig.suptitle("Lucy Bronze passes against Sweden", fontsize = 30)
plt.show()

# %% markdown
# ### Plotting multiuple pass maps on one figure

# %% codecell
mask_england = (df.type_name == 'Pass') & (df.type_name == 'Pass') & (df.team_name == "England Women's") & (df.sub_type_name != "Throw-in")
df_passes = df.loc[mask_england, ['x', 'y', 'end_x', 'end_y', 'player_name']]
names = df_passes['player_name'].unique()

pitch = Pitch(line_color='black', pad_top=20)
fig, axs = pitch.grid(ncols=4, nrows=4, grid_height=0.85, title_height=0.06, axis=False,
                    endnote_height=0.04, title_space=0.04, endnote_space=0.01)

# plot pass map for each player
for player, ax in zip(names, axs['pitch'].flat[:len(names)]):
    ax.text(60, -10, player, ha='center', va='center', fontsize=14)
    player_df = df_passes.loc[df_passes['player_name'] == player]
    pitch.scatter(player_df.x, player_df.y, alpha=0.2, s=50, color='blue', ax=ax)
    pitch.arrows(player_df.x, player_df.y, player_df.end_x, player_df.end_y, color='blue', ax=ax, width=1)

# remove extra axes
for ax in axs['pitch'][-1, 16 - len(names):]:
    ax.remove()

#Another way to set title using mplsoccer
axs['title'].text(0.5, 0.5, 'England passes against Sweden', ha='center', va='center', fontsize=30)
plt.show()
