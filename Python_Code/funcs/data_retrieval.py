'''
functions to extract match history data
'''

from mwrogue.esports_client import EsportsClient
import pandas as pd
import numpy as np
site = EsportsClient("lol")

def get_tournament_info(Tournament):

    '''
    Extract information from the Tournaments table
    '''

    tourney = site.cargo_client.query(
        tables = "Tournaments = T",
        fields = "T.OverviewPage, T.DateStart, T.League, T.Name, T.StandardName, T.Split, T.SplitNumber",
        where = f"Name = '{Tournament}'"
    )

    return pd.DataFrame(tourney)

def get_tournament_roster_info(Tournament):

    '''
    Get all rosters for a specific tournament

    Databases: Tournaments, TournamentRosters
    '''

    # first, find the specific tournament
    tourney = site.cargo_client.query(
        tables = "Tournaments = T",
        fields = "T.OverviewPage, T.DateStart, T.League, T.Name, T.StandardName, T.Split, T.SplitNumber",
        where = f"Name = '{Tournament}'"
    )

    page_name = pd.DataFrame(tourney)['OverviewPage'].values[0]

    # then, find all the rosters in this tournament

    tourney_rosters = site.cargo_client.query(
        tables = "TournamentRosters = TR",
        fields = "TR.OverviewPage, TR.Team, TR.RosterLinks, TR.Tournament",
        where = f"OverviewPage = '{page_name}'"
    )

    # reorganize as a dataframe with two columns (team, player)

    for i in range(len(tourney_rosters)):
        players = tourney_rosters[i]['RosterLinks'].split(';;')
        team = [tourney_rosters[i]['Team']] * len(players)

        df_i = pd.DataFrame({'Team': team, 'AllName': players})

        if i == 0:
            df = df_i
        else:
            df  = pd.concat([df, df_i], axis = 0)


    return df

def get_tournament_player_info(Tournament):

    '''
    Get information about all the players from a tournament

    Databases: Tournaments, TournamentPlayers
    '''

    # first, find the specific tournament
    tourney = site.cargo_client.query(
        tables = "Tournaments = T",
        fields = "T.OverviewPage, T.DateStart, T.League, T.Name, T.StandardName, T.Split, T.SplitNumber",
        where = f"Name = '{Tournament}'"
    )

    page_name = pd.DataFrame(tourney)['OverviewPage'].values[0]
    start_date = pd.DataFrame(tourney)['DateStart'].values[0]

    # then, find all the players in this tournament

    Tournament = 'World Championship'

    TP = site.cargo_client.query(
        tables = "TournamentPlayers = TP",
        fields = "TP.Team, TP.Player, TP.OverviewPage, TP.PageAndTeam, TP.N_PlayerInTeam, TP.TeamOrder, TP.Role, TP.IsDistribution",
        where = f"OverviewPage = '{page_name}' AND TP.Role IN ('Top', 'Jungle', 'Mid', 'Bot', 'Support')"
    )

    df2 = pd.DataFrame(TP) 

    # then, retrieve personal information about all the players

    all_players = df2['Player'].values

    df3 = get_player_info(all_players)

    # which players are missing?

    df3_players = df3['AllName'].values

    return df3  

def get_player_info(IGNs):

    '''
    retrieve player-specific information from Players and PlayerRedirects tables.

    Note: IGN's are case sensitive
    '''

    formatted_IGNs = ", ".join(f"'{value}'" for value in IGNs)

    player = site.cargo_client.query(
        tables = "Players=P, PlayerRedirects = PR",
        join_on = "P.OverviewPage = PR.OverviewPage",
        fields = "P.ID, P.Age, P.Birthdate, P.Name, P.Team, PR.AllName",
        where = f"PR.AllName IN ({formatted_IGNs})"
    )

    # retrieve the player(s) of interest

    df = pd.DataFrame(player)

    return df

# test cases 

# get_player_info(['XUN'])

# df = get_player_info(['Zeus', 'Oner', 'Faker', 'gumaYusi', 'KERIA', 'Caps'])
