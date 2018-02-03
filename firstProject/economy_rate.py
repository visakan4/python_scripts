import pandas as ps
import json

def getSeasonId(season_data,match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Season_Id']

def getYear(season_data,match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Match_Date']

def readFiles():
    ball_by_ball_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Ball_by_Ball.csv',sep=',')
    season_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv', sep=',')
    return ball_by_ball_data,season_data

def getEconomy(player_ball_by_ball_data,season_data):
    match_by_data = player_ball_by_ball_data.groupby('Match_Id')
    total_runs_conceded = 0
    total_balls_bowled = 0
    player_details =[]
    for match_id, match_details in match_by_data:
        match_details_hash = {}
        runs_conceded_in_match = 0
        balls_bowled_in_a_match = 0
        match_details_hash['seson_id'] = str(getSeasonId(season_data,match_id))
        match_details_hash['match_id'] = match_id
        match_details_hash['date'] = str(getYear(season_data,match_id))
        for index, ball_details in match_details.iterrows():
            if not ((ball_details['Batsman_Scored'] == 'Do_nothing') | (ball_details['Batsman_Scored'] == ' ')):
                    runs_conceded_in_match+=int(ball_details['Batsman_Scored'])
            if not (ball_details['Extra_Type'] == 'legbyes') | (ball_details['Extra_Type'] == 'byes') | (ball_details['Extra_Type'] == ' ') | (ball_details['Extra_Type'] == 'penalty'):
                runs_conceded_in_match += int(ball_details['Extra_Runs'])
            if not (ball_details['Extra_Type'] == 'wides') | (ball_details['Extra_Type'] == 'noballs'):
                balls_bowled_in_a_match+=1
        total_runs_conceded+=runs_conceded_in_match
        total_balls_bowled+=balls_bowled_in_a_match
        match_details_hash['runs_conceded_in_match'] = runs_conceded_in_match
        match_details_hash['balls_bowled_in_match'] = balls_bowled_in_a_match
        match_details_hash['match_economy'] = (float(runs_conceded_in_match)/float(balls_bowled_in_a_match) * 6)
        match_details_hash['overall_economy'] = (float(total_runs_conceded)/float(total_balls_bowled) * 6)
        match_details_hash['total_runs_conceded'] = total_runs_conceded
        match_details_hash['total_balls_bowled'] = total_runs_conceded
        player_details.append(match_details_hash)
    return player_details


def getPlayerEconomy(playerId):
    ball_by_ball_data,season_data = readFiles()
    player_details = getEconomy(ball_by_ball_data.query('Bowler_Id=='+str(playerId)),season_data)
    print json.dumps(player_details)


getPlayerEconomy(71)