import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# def retrieve_pick_ban(Tournament):

import sys
sys.path.append('c:/Users/jasen/Documents/League-of-Graphs/Python_Code/funcs')

from data_retrieval import get_pick_ban_data

parser = argparse.ArgumentParser(description="Tourney Name.")

parser.add_argument('--tourney', type=str, required=True, help='Name of Tourney')
    
# Parse the arguments
args = parser.parse_args()
print(args)

def analyze_fearless(df):

    '''
    Utilize the number of games in the series
    '''

    N_matches = max(df['N MatchInPage'])
    

if __name__ == '__main__':

    print(1+1)

    df = get_pick_ban_data(f"{args.tourney}") #LCK Cup 2025

    N_matches = len(df['MatchId'].unique())
    champions_dict = {}

    #debugging 
    print(df.shape)
    df.to_csv('output.csv', index=False)

    

    # for i in range(N_matches):
    for i in df['MatchId'].unique():

        # match_df = df[df['N MatchInPage'] == i+1]
        match_df = df[df['MatchId'] == i]    
        N_games = max(match_df['N GameInMatch']) # number of games in the match


        fearless_banned = []
        prev_picked = []

        for j in range(N_games): #for each game in the match

            # update fearless_banned list
            fearless_banned += prev_picked
            for champion in fearless_banned:
                if champion not in champions_dict:
                    champions_dict[champion] = {'picked': 0, 'banned': 0, 'fearless_banned': 0}
                champions_dict[champion]['fearless_banned'] += 1    

            # get this game's data
            game_df = match_df[match_df['N GameInMatch'] == j+1]
            picked = game_df['Team1Picks'].str.split(',') + game_df['Team2Picks'].str.split(',')
            banned = game_df['Team1Bans'].str.split(',') + game_df['Team2Bans'].str.split(',')

            # update pick and banned lists

            for champion in picked.tolist()[0]:
                if champion not in champions_dict:
                    champions_dict[champion] = {'picked': 0, 'banned': 0, 'fearless_banned': 0}
                champions_dict[champion]['picked'] += 1

            for champion in banned.tolist()[0]:
                if champion not in champions_dict:
                    champions_dict[champion] = {'picked': 0, 'banned': 0, 'fearless_banned': 0}
                champions_dict[champion]['banned'] += 1


            prev_picked = picked.tolist()[0]


    sorted_champions = sorted(champions_dict.items(), key=lambda x: sum(x[1].values()), reverse=True)
    # Sort the dictionary by the sum of values (picked + banned + other_metric)
    sorted_champions = sorted(
        champions_dict.items(),
        key=lambda x: (
            -sum(x[1].values()),       # Sort by total sum (picked + banned + other_metric)
            -x[1]['banned'],         # If tied, sort by banned (descending, hence the negative)
            -x[1]['picked'],         # If still tied, sort by picked (descending, hence the negative)
            x[0]                     # If still tied, sort alphabetically by champion name (ascending)
        ),
        reverse=False  # We want the total sum to be sorted in descending order (so reverse=False)
    )

    # Convert the sorted result back into a dictionary
    sorted_champions_dict = dict(sorted_champions)

    # graph

    champions = list(sorted_champions_dict.keys())
    picked = [sorted_champions_dict[champion]['picked'] for champion in champions]
    banned = [sorted_champions_dict[champion]['banned'] for champion in champions]
    fearless_banned = [sorted_champions_dict[champion]['fearless_banned'] for champion in champions]


    fig, ax = plt.subplots(figsize=(10, 6))

    # Creating stacked bar chart
    ax.bar(champions, banned, label='Banned', color='red')
    ax.bar(champions, picked, bottom=banned, label='Picked', color='green')
    ax.bar(champions, fearless_banned, bottom=[i+j for i,j in zip(picked, banned)], label='fearless_banned', color='blue')

    # Adding labels and title
    ax.set_ylabel('Count')
    ax.set_title('Champion Pick, Ban, and Fearless Ban Counts')
    ax.legend()

    # Adjusting y-axis limits to ensure no truncation
    max_total = [sum(x) for x in zip(picked, banned, fearless_banned)]
    ax.set_ylim(0, max(max_total) + 5)  # Set the upper limit slightly higher than the highest total


    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    plt.tight_layout()
    plt.show()    



    