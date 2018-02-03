import pandas as ps
import json

def readFiles():
    ball_by_ball_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Ball_by_Ball.csv',sep=',')
    season_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv', sep=',')
    teams_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Team.csv', sep=',')
    return ball_by_ball_data,season_data,teams_data

def getSeasonId(season_data,match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Season_Id']

def getTeamName(teams_data,team_id):
    return teams_data.at[teams_data[teams_data['Team_Id'] == team_id].index[0], 'Team_Short_Code']

def matchDetails(ball_by_ball_data,season_data,teams_data):
    matchesGroup = ball_by_ball_data.groupby('Match_Id')
    season_runs_data = []
    for name, matchGroup in matchesGroup:
        matchGroupByTeam = matchGroup.groupby('Innings_Id')
        for teamName, teamMatch in matchGroupByTeam:
            teamHash = {}
            runsScored = 0
            for index, ball in teamMatch.iterrows():
                if not (ball['Batsman_Scored'] == ' '):
                    if not (ball['Batsman_Scored'] == 'Do_nothing'):
                        runsScored += int(ball['Batsman_Scored'])
                if not (ball['Extra_Runs'] == ' '):
                    runsScored += int(ball['Extra_Runs'])
                team_id = ball['Team_Batting_Id']
                bowling_id = ball['Team_Bowling_Id']
            batting_team_name = getTeamName(teams_data, team_id)
            bowling_team_name = getTeamName(teams_data, bowling_id)
            teamHash['key'] = batting_team_name + " vs " + bowling_team_name
            teamHash['value'] = runsScored
            teamHash['region'] = int(getSeasonId(season_data,name))
            teamHash['subregion'] = getTeamName(teams_data,team_id)
            season_runs_data.append(teamHash)
    return (season_runs_data)


def getMatchDetails():
    ball_by_ball_data,season_data,teams_data = readFiles()
    matchRunDetails = matchDetails(ball_by_ball_data,season_data,teams_data)
    print(json.dumps(matchRunDetails))

getMatchDetails()