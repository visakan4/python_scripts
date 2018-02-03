import pandas as ps
import json


def getYear(season_id):
    return season_data.at[season_data[season_data['Season_Id'] == season_id].index[0],'Match_Date'].split("-")[2]

def isPlaying(players_ball_by_ball,player_id):
    out = False
    try:
        value = players_ball_by_ball.get_group(player_id)
        out = True
    except KeyError:
        out = False
    return out

def modeOfDismisallCount(match_ball_by_ball,season_player_out):
    season_player_out['caught'] = 0
    try:
        dismisall_type = match_ball_by_ball.groupby('Player_dissimal_Id').get_group(str(player_id))['Dissimal_Type'].iloc[0]
        return dismisall_type
    except KeyError:
        dismisall_type = ''
        return ''

def getValues():
    for season_id, details_in_season in details_by_season:
        matches_in_season = details_in_season['Match_Id']
        season_player_out = {}
        no_of_times_got_out_below_10 = 0
        no_of_times_got_out_between_10_to_30 = 0
        no_of_times_got_out_above_30 = 0
        no_of_times_out_caught = 0
        no_of_times_out_lbw = 0
        no_of_times_out_run_out = 0
        no_of_times_out_bowled = 0
        no_of_times_out_hit_wicket = 0
        no_of_times_out_caught_bowled = 0
        no_of_times_out_stumped = 0
        no_of_times_out_obstructing_the_field = 0
        no_of_times_out_retired_hurt = 0
        for match_id in matches_in_season:
            runs_scored_in_match = 0
            match_ball_by_ball = matches_ball_by_ball.get_group(match_id)
            players_ball_by_ball = match_ball_by_ball.groupby('Striker_Id')
            if (isPlaying(players_ball_by_ball,player_id)):
                dismisall_type = modeOfDismisallCount(match_ball_by_ball, season_player_out)
                if (dismisall_type == 'caught'):
                    no_of_times_out_caught += 1
                elif (dismisall_type == 'bowled'):
                    no_of_times_out_bowled += 1
                elif (dismisall_type == 'run out'):
                    no_of_times_out_run_out += 1
                elif (dismisall_type == 'lbw'):
                    no_of_times_out_lbw += 1
                elif (dismisall_type == 'stumped'):
                    no_of_times_out_stumped += 1
                elif (dismisall_type == 'caught and bowled'):
                    no_of_times_out_caught_bowled += 1
                elif (dismisall_type == 'hit wicket'):
                    no_of_times_out_hit_wicket += 1
                elif (dismisall_type == 'obstructing the field'):
                    no_of_times_out_obstructing_the_field += 1
                elif (dismisall_type == 'retired hurt'):
                    no_of_times_out_retired_hurt += 1

                player_ball_by_ball = players_ball_by_ball.get_group(player_id)
                for index,ball in player_ball_by_ball.iterrows():
                    if not (ball['Batsman_Scored'] == 'Do_nothing'):
                        runs_scored_in_match+=int(ball['Batsman_Scored'])
                if (runs_scored_in_match >30):
                    no_of_times_got_out_above_30+=1
                elif (runs_scored_in_match <10):
                    no_of_times_got_out_below_10+=1
                elif (runs_scored_in_match >=10 & runs_scored_in_match <=30):
                    no_of_times_got_out_between_10_to_30+=1
        season_player_out['below_10_count'] = no_of_times_got_out_below_10
        season_player_out['ten_to_thirty_count'] = no_of_times_got_out_between_10_to_30
        season_player_out['thirty_plus_count'] = no_of_times_got_out_above_30
        season_player_out['season_id'] = int(season_id)
        season_player_out['season_year'] = "20"+getYear(season_id)
        season_player_out['no_of_times_out_caught'] = no_of_times_out_caught
        season_player_out['no_of_times_out_lbw'] = no_of_times_out_lbw
        season_player_out['no_of_times_out_run_out'] = no_of_times_out_run_out
        season_player_out['no_of_times_out_bowled'] = no_of_times_out_bowled
        season_player_out['no_of_times_out_hit_wicket'] = no_of_times_out_hit_wicket
        season_player_out['no_of_times_out_caught_bowled'] = no_of_times_out_caught_bowled
        season_player_out['no_of_times_out_stumped'] = no_of_times_out_stumped
        season_player_out['no_of_times_out_obstructing_the_field'] = no_of_times_out_obstructing_the_field
        season_player_out['no_of_times_out_retired_hurt'] = no_of_times_out_retired_hurt
        player_out_data.append(season_player_out)


def work_flow(player_id_selected):
    global no_of_times_out_caught
    global no_of_times_out_lbw
    global no_of_times_out_run_out
    global no_of_times_out_bowled
    global no_of_times_out_hit_wicket
    global no_of_times_out_caught_bowled
    global no_of_times_out_stumped
    global no_of_times_out_obstructing_the_field
    global no_of_times_out_retired_hurt
    global season_data
    global ball_by_ball_data
    global player_all_matches
    global player_out_data
    global details_by_season
    global matches_ball_by_ball
    global match_groups_by_player
    global player_id

    player_out_data = []

    season_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv', sep=',')

    ball_by_ball_data = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Ball_by_Ball.csv',
        sep=',')

    player_all_matches = ps.read_csv(
        filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Player_Match.csv',
        sep=',')

    player_id = player_id_selected

    details_by_season = season_data.groupby('Season_Id')
    matches_ball_by_ball = ball_by_ball_data.groupby('Match_Id')
    match_groups_by_player = player_all_matches.groupby('Player_Id')
    getValues()
    return json.dumps(player_out_data)


print work_flow(6)