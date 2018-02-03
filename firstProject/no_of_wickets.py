import pandas as ps
import json

def getSeasonId(season_data,match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Season_Id']


def readFiles():
    ball_by_ball_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Ball_by_Ball.csv',sep=',')
    season_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv', sep=',')

    return ball_by_ball_data,season_data


def getWicketCount(match_grouped_data,season_data):
    ipl_data = []
    season_list = [1, 2, 3, 4, 7, 8, 9]
    for season_id in season_list:
        season_wicket_data = {}
        no_of_wickets = 0
        no_of_wickets_bowled = 0
        no_of_wickets_caught = 0
        no_of_wickets_caught_and_bowled = 0
        no_of_wickets_hitwicket = 0
        no_of_wickets_lbw = 0
        no_of_wickets_stumped = 0
        for match_id, match_details in match_grouped_data:
            if (getSeasonId(season_data,match_id) == season_id):
                for index, match_detail in match_details.iterrows():
                    if not (match_detail['Player_dissimal_Id']==' '):
                        if not ((match_detail['Dissimal_Type'] == 'run out') | (match_detail['Dissimal_Type'] == 'retired hurt') | (match_detail['Dissimal_Type'] == 'obstructing the field')):
                            no_of_wickets+=1
                            if (match_detail['Dissimal_Type']=='caught'):
                                no_of_wickets_caught+=1
                            elif (match_detail['Dissimal_Type'] == 'bowled'):
                                no_of_wickets_bowled+=1
                            elif (match_detail['Dissimal_Type'] == 'lbw'):
                                no_of_wickets_lbw+=1
                            elif (match_detail['Dissimal_Type'] == 'stumped'):
                                no_of_wickets_stumped+=1
                            elif (match_detail['Dissimal_Type'] == 'hit wicket'):
                                no_of_wickets_hitwicket+=1
                            elif (match_detail['Dissimal_Type'] == 'caught and bowled'):
                                no_of_wickets_caught_and_bowled+=1
            season_wicket_data['no_of_wickets'] = no_of_wickets
            season_wicket_data['no_of_wickets_caught'] = no_of_wickets_caught
            season_wicket_data['no_of_wickets_bowled'] = no_of_wickets_bowled
            season_wicket_data['no_of_wickets_lbw'] = no_of_wickets_lbw
            season_wicket_data['no_of_wickets_stumped'] = no_of_wickets_stumped
            season_wicket_data['no_of_wickets_hitwicket'] = no_of_wickets_hitwicket
            season_wicket_data['no_of_wickets_caught_and_bowled'] = no_of_wickets_caught_and_bowled
            season_wicket_data['season_id'] = season_id
        ipl_data.append(season_wicket_data)
    return ipl_data


def getWicketCategoryCount(player_id):
    ball_by_ball_data,season_data = readFiles()
    player_season_wickets = getWicketCount(ball_by_ball_data.query('Bowler_Id =='+str(player_id)).groupby('Match_Id'),season_data)
    print json.dumps(player_season_wickets)


getWicketCategoryCount(71)

