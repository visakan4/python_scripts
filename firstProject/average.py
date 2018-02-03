import json
import pandas as ps

def getSeasonId(match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Season_Id']

def getYear(match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Match_Date'].split("-")[2]

def isOut(match_id):
    out = False
    match_value = group_by_matches.get_group(match_id)
    player_value = match_value.groupby('Player_dissimal_Id')
    try:
        value = player_value.get_group(str(playerId))
        out = True
    except KeyError, key:
        out = False
    return out


def getAverage():
    for name,group in strikerGroup:
        if (name == playerId):
            match_groups = group.groupby('Match_Id')
            no_of_out = 0
            runsScored = 0
            for match_id, match_group in match_groups:
                matchDetails = {}
                runsScored_in_match = 0
                for index, row in match_group.iterrows():
                    if not (row['Batsman_Scored']=='Do_nothing'):
                        if not (row['Batsman_Scored'] == ' '):
                            runsScored_in_match+=int(row['Batsman_Scored'])
                            runsScored+=int(row['Batsman_Scored'])
                if (isOut(match_id)):
                    no_of_out += 1
                if (no_of_out == 0):
                    average = runsScored
                else:
                    average = float(runsScored)/float(no_of_out)
                matchDetails['match_id'] = int(match_id)
                matchDetails['runs_scored_in_match'] = runsScored_in_match
                matchDetails['average'] = average
                matchDetails['no_of_times_got_out'] = no_of_out
                matchDetails['runs_scored'] = runsScored
                matchDetails['season_id'] = int(getSeasonId(match_id))
                matchDetails['season_year'] = "20"+getYear(match_id)
                playerDetails.append(matchDetails)


def workFlow():
    global playerId
    global ball_by_ball_data
    global season_data
    global playerDetails
    global strikerGroup
    global group_by_matches

    playerId = 4

    ball_by_ball_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Ball_by_Ball.csv',
        sep=',')
    season_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv', sep=',')

    playerDetails = []

    strikerGroup = ball_by_ball_data.groupby('Striker_Id')
    group_by_matches = ball_by_ball_data.groupby('Match_Id')
    getAverage()
    playerDetailsJSON = json.dumps(playerDetails)
    print (playerDetailsJSON)


workFlow()