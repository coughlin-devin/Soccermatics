# %% markdown
# ### Opening the data.
# We will use 2017/18 Premiere League season data.

# %% codecell
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# %% codecell
#open events
# get current working directory
cwd = os.getcwd()

# import event data
path = os.path.join(cwd, 'data', 'Wyscout', 'events', 'events_England.json')
with open(path) as f:
    events = pd.read_json(f)

# import player data
path = os.path.join(cwd, 'data', 'Wyscout', 'teams.json')
with open(path) as f:
    teams = pd.read_json(f)
teams = teams.rename(columns={'wyId': 'teamId'})

# %% markdown
# ### Preparing the data.
# We will look at corners taken for each team.

# %% codecell
# get corners
corners = events[events["subEventName"] == 'Corner']
# count corners by team
corners_by_team = corners.groupby('teamId').size().reset_index(name='counts')
# merge with team names
summary = corners_by_team.merge(teams[['name', 'teamId']], how='left', on='teamId')
# count corners by team by game
corners_by_game = corners.groupby(['teamId', 'matchId']).size().reset_index(name='counts')
summary2 = corners_by_game.merge(teams[['name', 'teamId']], how='left', on='teamId')

# %% markdown
# ### One-sample one-sided t-test
# Assume teams typically get 6 corners per game. Let's see if Man City, and attacking minded team, typically get more.

# %% codecell
from scipy.stats import ttest_1samp
team_name = 'Manchester City'
man_city_corners = summary2.loc[summary2['name'] == team_name]

def FormatFigure(ax):
    ax.legend(loc='upper left')
    ax.set_ylim(0,0.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel('')
    ax.set_xlabel('Corners')
    ax.set_ylabel('Proportion of games')
    ax.set_xticks(np.arange(0,21,step=1))


fig,ax1=plt.subplots(1,1)
ax1.hist(man_city_corners.counts, np.arange(0.01,20.5,1), color='lightblue', edgecolor = 'white',linestyle='-',alpha=0.5, label=team_name, density=True,align='right')
FormatFigure(ax1)

mean = man_city_corners.counts.mean()
std = man_city_corners.counts.std()

print('City typically had %.2f  plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))

t, pvalue = ttest_1samp(man_city_corners.counts, popmean=6, alternative='greater')
alpha = 0.05
print("The t-staistic is %.2f and the P-value is %.2f."%(t,pvalue))
if pvalue < alpha:
    print("We reject null hypothesis - " + team_name + " typically take more than 6 corners per match.")
else:
    print("We cannot reject null hypothesis - " + team_name + " do not typically take more than 6 corners per match.")

# %% markdown
# ### Two-sample two-sided t-test.
# We compare Liverpool and Everton in terms of corners per match.

# %% codecell
liverpool_corners = summary2.loc[summary2['name'] == 'Liverpool']
everton_corners = summary2.loc[summary2['name'] == 'Everton']

mean = liverpool_corners.counts.mean()
std = liverpool_corners.counts.std()
print("Liverpool typically had %.2f plus/minus %.2f corners per match in the 2017/18 season."%(mean,std))
std_error=std/np.sqrt(len(liverpool_corners))
print('The standard error in the number of corners per match is %.4f'%std_error)

mean = everton_corners.counts.mean()
std = everton_corners.counts.std()
print('Everton typically had %.2f plus/minus %.2f corners per match in the 2017/18 season.'%(mean,std))
std_error=std/np.sqrt(len(everton_corners))
print('The standard error in the number of corners per match is %.4f'%std_error)

fig,ax=plt.subplots(1,1)
ax.hist(liverpool_corners.counts, np.arange(0.01,15.5,1), color='red', edgecolor = 'white',linestyle='-',alpha=1.0, label="Liverpool", density=True,align='right')
ax.hist(everton_corners.counts, np.arange(0.01,15.5,1), alpha=0.25, color='blue', edgecolor = 'black', label='Everton',  density=True,align='right')
FormatFigure(ax)

from scipy.stats import ttest_ind

t, pvalue = ttest_ind(liverpool_corners.counts, everton_corners.counts, equal_var=False, alternative='two-sided')
alpha = 0.05
print("The t-staistic is %.2f and the P-value is %.2f."%(t,pvalue))
if pvalue < alpha:
    print("We reject null hypothesis - Liverpool took different number of corners per game than Everton")
else:
    print("We cannot reject the null hypothesis that Liverpool took the same number of corners per game as Everton")
