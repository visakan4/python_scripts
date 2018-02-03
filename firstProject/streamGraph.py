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
    season_runs_by_team = []
    for season in range(1,9):
        runs_by_team = []
        for team in team_list:
            team_ball_by_ball = ball_by_ball_data.groupby('Team_Batting_Id').get_group(team)
            runs_by_over =[]
            for over in range(1,21):
                runs_scored_in_over = 0
                get_over_data = team_ball_by_ball.groupby('Over_Id').get_group(over)
                for header, ball in get_over_data.iterrows():
                    if (int(getSeason(season_data,ball['Match_Id']))==season):
                        if not (ball['Batsman_Scored'] == 'Do_nothing'):
                            if not (ball['Batsman_Scored'] == ' '):
                                runs_scored_in_over += int(ball['Batsman_Scored'])
                        if not (ball['Extra_Runs'] == ' '):
                            runs_scored_in_over += int(ball['Extra_Runs'])
                runs_by_over.append(runs_scored_in_over)
            runs_by_team.append(runs_by_over)
        season_runs_by_team.append(runs_by_team)
    return season_runs_by_team


def writeToFile(data,team_list):
    for i in range(0, len(data)):
        fileName = 'season' + str(i) + '.csv'
        with open(fileName, "wb") as f_obj:
            header = ['teamID', 'runs', 'over']
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