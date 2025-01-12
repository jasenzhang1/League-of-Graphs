
# GOAL: AVERAGE AGE OF EACH TEAM IN A TOURNAMENT

'''
Get each roster at a tournament
Get all the players participating in the tournament
Extract the players in each roster and their birthdates
Calculate the average age of each team
'''



from datetime import datetime
import sys
import seaborn as sns
import pandas as pd
import numpy as np
from importlib import reload
import matplotlib.pyplot as plt
reload(data_retrieval)

sys.path.append('c:/Users/jasen/Documents/League-of-Graphs/Python_Code/funcs')

import data_retrieval

tournament = 'Worlds 2024 Main Event'

# 1) get info about the tournament itself (start date)
tourney_start_date = data_retrieval.get_tournament_info(tournament)['DateStart']
tourney_start_date = datetime.strptime(tourney_start_date.values[0], "%Y-%m-%d")

# 2) get the tournament roster information
df2 = data_retrieval.get_tournament_roster_info(tournament)

# 3) get information about each of the players
df3 = data_retrieval.get_tournament_player_info(tournament)

# 4) merge the two dataframes
df_final = pd.merge(df2, df3[['AllName', 'Birthdate']], on = 'AllName', how = 'right')

# now, we have all the information we need to do calculations. 
 
# 5) calculations
df_final['Birthdate'] = pd.to_datetime(df_final['Birthdate'], format="%Y-%m-%d")

df_final['Age_At_Tourney'] = ((tourney_start_date - df_final['Birthdate']).dt.days) / 365.25

# now average the age for each team



grouped_avg = df_final.groupby('Team')[['Age_At_Tourney']].mean().sort_values(by='Age_At_Tourney', ascending=True)

grouped_avg['Age_At_Tourney'] = grouped_avg['Age_At_Tourney'].round(2)

grouped_avg2 = grouped_avg.reset_index()

# 6) Plot


# Create the bar chart
sns.barplot(x='Team', y='Age_At_Tourney', data=grouped_avg2, palette='Blues_d')

# Add title
plt.title('Average Age of Teams at Worlds 2024')

# Show the chart
plt.show()