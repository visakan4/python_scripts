import pandas as ps
import datetime
import json
import math
from dateutil import relativedelta as rdelta

matches_player_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Player_Match.csv')
players_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Player.csv')
season_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv')

match_by_match_players_data = matches_player_data.groupby('Match_Id')

mainData = []

def wonTheMatchOrNot(match_id,team_id):
    if (math.isnan(season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Match_Winner_Id'])):
        team_details_hash['winner'] = 'washed_out'
    else:
        if (season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Match_Winner_Id'] == team_id):
            team_details_hash['winner'] = 'yes'
        else:
            team_details_hash['winner'] = 'no'

def battingFirstorSecond(match_id,team_id):
    if (season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Toss_Winner_Id'] == team_id):
        team_details_hash['tosswinner'] = 1
        if (season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Toss_Decision'].strip() == 'field'):
            team_details_hash['batting'] = 'second'
        else:
            team_details_hash['batting'] = 'first'
    else:
        team_details_hash['tosswinner'] = 0
        if (season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Toss_Decision'].strip() == 'field'):
            team_details_hash['batting'] = 'first'
        else:
            team_details_hash['batting'] = 'second'


def getMatchYear(match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Match_Date'].strip()


def getAge(player_id):
    return players_data.at[players_data[players_data['Player_Id'] == player_id].index[0], 'DOB'].strip()


def getBattingType(player_id):
    flag = False
    battingType = players_data.at[players_data[players_data['Player_Id'] == player_id].index[0], 'Batting_Hand'].strip()
    if (battingType == 'Right_Hand'):
        flag = True
    return flag


def getCountry(player_id):
    return players_data.at[players_data[players_data['Player_Id'] == player_id].index[0], 'Country'].strip()


def noOfPlayersCountryWise(team_players,match_date):
    no_of_players_between_18_24 = 0
    no_of_players_between_24_30 = 0
    no_of_players_above_30 = 0
    no_of_right_handed_players = 0
    no_of_left_handed_players = 0
    no_of_australian_players = 0
    no_of_england_players = 0
    no_of_westIndian_players = 0
    no_of_srilankan_players = 0
    no_of_pakistan_players = 0
    no_of_newzealand_players = 0
    no_of_bangladesh_players = 0
    no_of_southAfrican_players = 0
    otherCountry = 0

    for player_id, player in team_players.iterrows():
        countryName = getCountry(player['Player_Id'])
        isRightHanded = getBattingType(player['Player_Id'])
        age = rdelta.relativedelta(match_date,datetime.datetime.strptime(getAge(player['Player_Id']), '%d-%b-%y')).years
        if (isRightHanded):
            no_of_right_handed_players+=1
        else:
            no_of_left_handed_players+=1

        if (age > 30):
            no_of_players_above_30+=1
        elif (age <= 30 & age >= 24):
            no_of_players_between_24_30+=1
        elif (age >=18 & age <24):
            no_of_players_between_18_24+=1

        if (countryName == 'Australia'):
            no_of_australian_players+=1
        elif (countryName =='England'):
            no_of_england_players+=1
        elif (countryName == 'Bangladesh'):
            no_of_bangladesh_players+=1
        elif (countryName == 'New Zealand'):
            no_of_newzealand_players+=1
        elif (countryName == 'South Africa'):
            no_of_southAfrican_players+=1
        elif (countryName == 'West Indies'):
            no_of_westIndian_players+=1
        elif (countryName == 'Sri Lanka'):
            no_of_srilankan_players+=1
        elif (countryName == 'Pakistan'):
            no_of_pakistan_players+=1
        else:
            otherCountry+=1

    team_details_hash['NumberOfAustralianPlayers'] = no_of_australian_players
    team_details_hash['NumberOfEnglandPlayers'] = no_of_england_players
    team_details_hash['NumberOfBangladesPlayers'] = no_of_bangladesh_players
    team_details_hash['NumberOfNewzealandPlayers'] = no_of_newzealand_players
    team_details_hash['NumberOfSouthAfricanPlayers'] = no_of_southAfrican_players
    team_details_hash['NumberOfWestIndianPlayers'] = no_of_westIndian_players
    team_details_hash['NumberOfPakistanPlayers'] = no_of_pakistan_players
    team_details_hash['NumberOfSrilankanPlayers'] = no_of_srilankan_players
    team_details_hash['NumberOfOtherPlayers'] = otherCountry
    team_details_hash['NumberOfPlayersbetween18and24'] = no_of_players_between_18_24
    team_details_hash['NumberOfPlayersbetween24and30'] = no_of_players_between_24_30
    team_details_hash['NumberOfPlayersabove30'] = no_of_players_above_30
    team_details_hash['NumberOfLeftHandedPlayers'] = no_of_left_handed_players
    team_details_hash['NumberOfRightHandedPlayers'] = no_of_right_handed_players


for match_id, match_players in match_by_match_players_data:
    team_players_group = match_players.groupby('Team_Id')
    for team_id, team_players in team_players_group:
        global team_details_hash
        team_details_hash = {}
        team_details_hash['Team_ID'] = int(team_id)
        wonTheMatchOrNot(match_id,team_id)
        battingFirstorSecond(match_id,team_id)
        noOfPlayersCountryWise(team_players,datetime.datetime.strptime(getMatchYear(match_id),'%d-%b-%y'))
        mainData.append(team_details_hash)


print json.dumps(mainData)