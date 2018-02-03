import pandas as ps
import json

def readFiles():
    player_details = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Player.csv',sep=',')
    return player_details


def getDetails(player_details,player_id):
    detailshash = {}
    detailshash['name'] = player_details.at[player_details[player_details['Player_Id'] == player_id].index[0], 'Player_Name']
    detailshash['country'] = player_details.at[player_details[player_details['Player_Id'] == player_id].index[0], 'Country']
    detailshash['age'] = 2017 - int("19"+player_details.at[player_details[player_details['Player_Id'] == player_id].index[0], 'DOB'].split('-')[2])
    return detailshash


def getPlayerDetails(player_id):
    player_details = readFiles()
    print(json.dumps(getDetails(player_details,player_id)))


getPlayerDetails(4)