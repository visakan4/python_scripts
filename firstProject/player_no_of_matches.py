import pandas as ps
import json

def readFiles():

    player_umpire_data = ps.read_csv(filepath_or_buffer="D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Player.csv",sep=',')
    match_players_data = ps.read_csv(filepath_or_buffer="D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Player_Match.csv",sep=',')
    return player_umpire_data,match_players_data

def getNoOfMatches(player_umpire_data,match_players_data):
    players_matches_count = []
    player_data_group = player_umpire_data.query('Is_Umpire==0')
    for name, player in player_data_group.iterrows():
        player_matches = {}
        match_player_data = match_players_data.query('Player_Id==' + str(player['Player_Id']))
        player_matches['player_id'] = int(player['Player_Id'])
        player_matches['numberofMatches'] = len(match_player_data)
        players_matches_count.append(player_matches)
    return players_matches_count


def getPlayerNoOfMatches():
    player_umpire_data,match_players_data = readFiles()
    players_matches_count = getNoOfMatches(player_umpire_data,match_players_data)
    with open('player_matches_count.json','wb') as file:
        json.dump(players_matches_count,file)

getPlayerNoOfMatches()