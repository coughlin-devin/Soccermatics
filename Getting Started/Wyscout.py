#importing necessary libraries
import pathlib
import os
import pandas as pd
import json

#path to data
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'competitions.json') # put # in front if used locally
#path = os.path.join(str(pathlib.Path().resolve()), 'Wyscout', 'competitions.json') # delete #

#open data
with open(path) as f:
    data = json.load(f)
    #save it in dataframe
df_competitions = pd.DataFrame(data)
#structure of data
df_competitions.info()

#path to data
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'matches', 'matches_England.json') # put # in front if used locally
#path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'matches_England.json') # delete #
with open(path) as f:
    data = json.load(f)
#save it in a dataframe
df_matches = pd.DataFrame(data)
#structure of data
df_matches.info()

#path to data
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'players.json') # put # in front if used locally
#path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'players.json')
#open data
with open(path) as f:
    data = json.load(f)
#save it in a dataframe
df_players = pd.DataFrame(data)
#structure of data
df_players.info()

#prepare empty dataframe
df_events = pd.DataFrame() # put # in front if used locally
for i in range(13): # put # in front if used locally
    #get file name and path to it
    path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'events', 'events_England.json') # put # in front if used locally
    #open data
    with open(path) as f: # put # in front if used locally
        data = json.load(f) # put # in front if used locally
    #append data to the dataframe
    df_events = pd.concat([df_events, pd.DataFrame(data)]) # put # in front if used locally


#path = os.path.join(str(pathlib.Path().resolve()), 'Wyscout', 'events_England_.json') # delete #
#with open(path) as f: # delete #
    #data = json.load(f) # delete #
#df_events = pd.DataFrame(data) # delete #

#structure of data
df_events.info()
