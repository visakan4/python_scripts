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


def getRuns(season_data,ball_by_ball_data,team_id,season_id):
    team_ball_by_ball = ball_by_ball_data.groupby('Team_Batting_Id').get_group(team_id)
    for over in range(1,21):
        over_details = {}
        no_of_fours_in_a_over = 0
        no_of_sixes_in_a_over = 0
        get_over_data = team_ball_by_ball.groupby('Over_Id').get_group(over)
        for header, ball in get_over_data.iterrows():
            if (int(getSeason(season_data,ball['Match_Id']))==season_id):
                if (ball['Batsman_Scored']=='4'):
                    no_of_fours_in_a_over+=1
                elif (ball['Batsman_Scored']=='6'):
                    no_of_sixes_in_a_over+=1
            over_details['over_number'] = over
            over_details['no_of_fours_in_a_over'] = no_of_fours_in_a_over
            over_details['no_of_sixes_in_a_over'] = no_of_sixes_in_a_over
        main_data.append(over_details)


main_data = []
season_data, teams_data,ball_by_ball_data = readFiles()
getRuns(season_data,ball_by_ball_data,1,1)

print json.dumps(main_data)