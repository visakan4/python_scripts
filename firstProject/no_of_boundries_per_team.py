import pandas as ps
import json
import csv

def readFiles():
    seasons_full_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv', sep=',')

    teams_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Team.csv', sep=',')

    ball_by_ball_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Ball_by_Ball.csv', sep=',')

    return seasons_full_data, teams_data,ball_by_ball_data

def isTeamPlaying(match_ball_by_ball,team):
    flag = False
    try:
        match_ball_by_ball.groupby('Team_Batting_Id').get_group(team)
        flag = True
    except KeyError:
        flag = False
    return flag


def getSeason(season_data,match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Season_Id']


def getRuns(season_data,ball_by_ball_data,teams_data):
    team_list = [1,2,3,4,5,6,7]
    season_boundries_by_team = []
    for season in range(1,9):
        boundries_by_team = []
        for team in team_list:
            team_ball_by_ball = ball_by_ball_data.groupby('Team_Batting_Id').get_group(team)
            boundries_by_over =[]
            for over in range(1,21):
                no_of_boundries = 0
                get_over_data = team_ball_by_ball.groupby('Over_Id').get_group(over)
                for header, ball in get_over_data.iterrows():
                    if (int(getSeason(season_data, ball['Match_Id'])) == season):
                        if ((ball['Batsman_Scored'] == '4') | (ball['Batsman_Scored'] == '6')):
                            no_of_boundries += 1
                boundries_by_over.append(no_of_boundries)
            boundries_by_team.append(boundries_by_over)
        season_boundries_by_team.append(boundries_by_team)
    return season_boundries_by_team


def writeToFile(data,team_list):
    for i in range(0, len(data)):
        fileName = 'boundries' + str(i) + '.csv'
        with open(fileName, "wb") as f_obj:
            header = ['key', 'value', 'date']
            writer = csv.writer(f_obj, delimiter=',')
            writer.writerow(header)
            for index, team in enumerate(team_list):
                for j in range(0, 20):
                    line = [team, data[i][index][j], j + 1]
                    writer.writerow(line)


team_id_list = [1,2,3,4,5,6,7]
season_data, teams_data,ball_by_ball_data = readFiles()
data = getRuns(season_data,ball_by_ball_data,teams_data)
writeToFile(data,team_id_list)