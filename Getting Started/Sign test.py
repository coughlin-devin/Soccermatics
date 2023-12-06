# %% markdown
# ### Opening the data.
# We will use 2017/18 Premiere League season data.

# %% codecell
import pandas as pd
import os

# get current working directory
cwd = os.getcwd()

# import event data
path = os.path.join(cwd, 'data', 'Wyscout', 'events', 'events_England.json')
with open(path) as f:
    train = pd.read_json(f)

# import player data
path = os.path.join(cwd, 'data', 'Wyscout', 'players.json')
with open(path) as f:
    players = pd.read_json(f)

# see what the data looks like
train.info()
players.info()
train.head()
players.head()

# %% markdown
# ### Filtering the data.
# Using Heung-Min Son as an example, we will check
# how many of his shots he took with his left foot
# and right foot to determine whether or not he is ambidextrous.

# %% codecell
# filter for shots
shots = train.loc[train['eventName'] == 'Shot']

# filter for Heung-Min Son
son_id = players.loc[(players['shortName'] == 'Son Heung-Min')]["wyId"].iloc[0]

# Event tags
LEFT_FOOT = {'id':401}
RIGHT_FOOT = {'id': 402}

# son's shots
son_shots = shots.loc[shots['playerId'] == son_id]
lefty_shots = son_shots.loc[son_shots.apply (lambda shot:LEFT_FOOT in shot.tags, axis = 1)]
righty_shots = son_shots.loc[son_shots.apply (lambda shot:RIGHT_FOOT in shot.tags, axis = 1)]

# %% markdown
# ### Performing the Sign Test.
# After getting left and right foot shot data,
# we will perform a sign test to see if the hypothesis Heung-Min Son
# is ambidextrous is true. We will use a significance level of 0.05.

# %% codecell
# create list with ones for lefty and -1s for righty shots
signed_list = [1] * len(lefty_shots)
signed_list.extend([-1] * len(righty_shots))

# Sign Test: non-parametric, two tailed binomial test with assumed probability=0.5
# Null hypothesis is Heung-Min Son is ambidextrous.
from statsmodels.stats.descriptivestats import sign_test
pvalue = sign_test(signed_list, mu0=0)[1]
# alpha is the significance level or probabiity of rejecting the null hypothesis when it is true, ie. alpha=0.05 means 5% risk of being wrong
alpha = 0.05
if pvalue < alpha:
    print("P-value amounts to", str(pvalue)[:5], "- We reject null hypothesis - Heung-Min Son is not ambidextrous")
else:
    print("P-value amounts to", str(pvalue)[:5], " - We do not reject null hypothesis - Heung-Min Son is ambidextrous")
