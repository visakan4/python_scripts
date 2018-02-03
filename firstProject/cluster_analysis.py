# -*- coding: utf-8 -*-

"""

Created on Wed Nov 22 22:49:59 2017



@author: Yuvaraj Subramanian

"""

import json

import numpy as np

from sklearn.cluster import KMeans

import warnings

from sklearn.preprocessing import normalize

from sklearn import metrics

import pandas as pd

from sklearn.preprocessing import Normalizer

cluster_count = 3

minBattingAverage = 35

maxBattingAverage = 45

minStrikeRate = 50

maxStrikeRate = 150

minBowlerEconomy = 5

maxBowlerEconomy = 70

minBowlingAverage = 5

maxBowlingAverage = 450

playerId = []

playerName = []

player_no_of_matches = []

battingStrikeRate = []

battingAverage = []

ballsFaced = []

bowlingAverage = []

bowlingEconomy = []

bowlingStrikeRate = []

ballsBowled = []

totalDismissCount = []

updatedId = []

updated_player_no_of_matches = []

updatedStrikeRate = []

updatedBattingAverage = []

updatedBowlerId = []

updated_bowler_player_no_of_matches = []

updatedBowlerEconomy = []

updatedBowlingAverage = []

updatedBowlingStrikeRate = []

mainData = []

bowlingMainData = []

averageBallFaced = 30

player_match_json = pd.read_json('player_matches_count.json','r')

def getNumberOfMatchesPlayed(player_id):
    return int(player_match_json.query('player_id=='+str(player_id))['numberofMatches'])


with open('playerJsonData.json', 'r') as playerJson:
    jsonData = json.load(playerJson)

    for row in jsonData:
        playerId.append(row['player_id'])

        player_no_of_matches.append(getNumberOfMatchesPlayed(row['player_id']))

        playerName.append(row['player_name'])

        battingStrikeRate.append(row['batting_strike_rate'])

        battingAverage.append(row['batting_average'])

        ballsFaced.append(row['balls_faced'])

        bowlingAverage.append(row['bowling_average'])

        bowlingEconomy.append(row['bowling_economy'])

        bowlingStrikeRate.append(row['bowling_strike_rate'])

        ballsBowled.append(row['balls_bowled'])

        totalDismissCount.append(row['total_dismissal'])

averageBallBowled = float("%.2f" % (sum(ballsBowled) / (len(ballsBowled) * 9)))

maxBattingAverage = max(battingAverage)

minBattingAverage = min(battingAverage)

maxStrikeRate = max(battingStrikeRate)

minStrikeRate = min(battingStrikeRate)

minBowlerEconomy = min(bowlingEconomy)

maxBowlerEconomy = max(bowlingEconomy)

minBowlingAverage = min(bowlingAverage)

maxBowlingAverage = max(bowlingAverage)

for i, indexaverage in enumerate(playerId):

    if battingAverage[i] >= minBattingAverage and battingAverage[i] <= maxBattingAverage:

        if battingStrikeRate[i] >= minStrikeRate and battingStrikeRate[i] <= maxStrikeRate:

            if ballsFaced[i] >= 30:

                if battingStrikeRate[i] != 0 and battingAverage[i] != 0:

                    if totalDismissCount[i] > 7:
                        #                    if battingAverage[i] > 26.5:

                        updatedId.append(playerId[i])

                        updated_player_no_of_matches.append(player_no_of_matches[i])

                        updatedStrikeRate.append(battingStrikeRate[i])

                        updatedBattingAverage.append(battingAverage[i])

    if bowlingEconomy[i] >= minBowlerEconomy and bowlingEconomy[i] <= maxBowlerEconomy:

        if bowlingAverage[i] >= minBowlingAverage and bowlingAverage[i] <= maxBowlingAverage:

            if ballsBowled[i] >= averageBallBowled:

                if bowlingAverage[i] != 0 and bowlingStrikeRate[i] != 0:
                    #                    if bowlingEconomy[i] < 10:

                    #                        if bowlingAverage[i] < 40:

                    updatedBowlerId.append(playerId[i])

                    updated_bowler_player_no_of_matches.append(player_no_of_matches[i])

                    updatedBowlerEconomy.append(bowlingEconomy[i])

                    updatedBowlingAverage.append(bowlingAverage[i])

                    updatedBowlingStrikeRate.append(bowlingStrikeRate[i])

# print(updatedId)

# combinedData = np.vstack((updated_player_no_of_matches,updatedBattingAverage, updatedStrikeRate)).T
combinedData = np.vstack((updatedBattingAverage, updatedStrikeRate)).T

bowlingCombinedData = np.vstack((updated_bowler_player_no_of_matches,updatedBowlerEconomy, updatedBowlingAverage, updatedBowlingStrikeRate)).T

# print combinedData[0][2]



battingNormalizedData = normalize(combinedData, axis=1, norm='l2')

bowlingNormalizedData = normalize(bowlingCombinedData, axis=1, norm='l2')

# print (bowlingNormalizedData)

# for i,index in enumerate(battingNormalizedData):
#     battingNormalizedData[i][1]*=1.5
#     battingNormalizedData[i][2]*=1.5


try:
    kmeanscluster = KMeans(n_clusters=cluster_count, random_state=0).fit(battingNormalizedData)


except ValueError:

    print("ValueError encountered in batting cluster")

km_labels = kmeanscluster.labels_

try:

    bowlingKmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(bowlingCombinedData)



except ValueError:

    print("ValueError encountered")

print("Batting Silhouette Coefficient: %0.3f"

      % metrics.silhouette_score(battingNormalizedData, kmeanscluster.labels_, sample_size=1000))

bowling_km_labels = bowlingKmeans.labels_

# print("Bowling Silhouette Coefficient: %0.3f"

#      % metrics.silhouette_score(bowlingNormalizedData, bowlingKmeans.labels_, sample_size=1000))



warnings.filterwarnings('ignore',

                        '.*Graph is not fully connected, spectral embedding.*',

                        UserWarning,

                        )

batting_km_labels_list = km_labels.tolist()

bowling_km_labels_list = bowling_km_labels.tolist()

# print(batting_km_labels_list)



count = 0

# print (playerId)

# print (updatedId)

for k, player in enumerate(playerId):

    for i, updatedplayer in enumerate(updatedId):

        playerHash = {}

        if playerId[k] == updatedId[i]:
            #            print (playerId[k], updatedId[i])

            playerHash['player_id'] = playerId[k]

            playerHash['numberOfMatches'] = player_no_of_matches[k]

            playerHash['player_name'] = playerName[k]

            playerHash['batting_strike_rate'] = battingStrikeRate[k]

            playerHash['batting_average'] = battingAverage[k]

            playerHash['balls_faced'] = ballsFaced[k]

            playerHash['km_batting_cluster_label'] = batting_km_labels_list[i]

            mainData.append(playerHash)

    for j, bowlingUpdatedplayer in enumerate(updatedBowlerId):

        bowlingPlayerHash = {}

        if playerId[k] == updatedBowlerId[j]:
            count = count + 1

            bowlingPlayerHash['player_id'] = playerId[k]

            bowlingPlayerHash['numberOfMatches'] = player_no_of_matches[k]

            bowlingPlayerHash['player_name'] = playerName[k]

            bowlingPlayerHash['bowling_average'] = bowlingAverage[k]

            bowlingPlayerHash['bowling_economy'] = bowlingEconomy[k]

            bowlingPlayerHash['bowling_strike_rate'] = bowlingStrikeRate[k]

            bowlingPlayerHash['balls_bowled'] = ballsBowled[k]
            bowlingPlayerHash['km_bowling_cluster_label'] = bowling_km_labels_list[j]

            bowlingMainData.append(bowlingPlayerHash)

print ("Bowling Total", count)

with open('jsonData_1.json', 'w') as mainDataJSON:
    json.dump(mainData, mainDataJSON)

with open('bowlingJsonData.json', 'w') as bowlingDataJSON:
    json.dump(bowlingMainData, bowlingDataJSON)