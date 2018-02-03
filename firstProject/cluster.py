# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 00:25:28 2017

@author: Yuvaraj Subramanian
"""
import csv
import json

player_id = []
player_name = []
matchPlayedPId = []
Match_Id = []
StrikerID = []
Batsman_Scored = []
Extra_Type = []
playerDissimalId = []
bowlerId = []
extraRuns = []
dissimalType = []
totalDismissal = []

strikeRate = []
battingAverage = []

bowlerEconomy = []
bowlingAverage = []
bowlingStrikeRate = []

ballsBowled = []
ballsFaced = []

totalFour = []
totalSix = []
averageFour = []
averageSix = []

totalScore = []

a = []

with open('F:\SEM 1\Visual Analytics\Project\Player.csv', 'r') as playerfile:
    playerFileReader = csv.DictReader(playerfile)
    for row in playerFileReader:
        if (row['Is_Umpire'] == "0"):
            player_id.append(row['Player_Id'])
            player_name.append(row['Player_Name'])

with open('F:\SEM 1\Visual Analytics\Project\Player_Match.csv', 'r') as playerMatchFile:
    playerMatchFileReader = csv.DictReader(playerMatchFile)
    for row in playerMatchFileReader:
        matchPlayedPId.append(row['Player_Id'])

with open('F:\SEM 1\Visual Analytics\Project\Ball_by_Ball.csv') as ballbybaplayerfile:
    ballByBallReader = csv.DictReader(ballbybaplayerfile)
    for row in ballByBallReader:
        Match_Id.append(row['Match_Id'])
        StrikerID.append(row['Striker_Id'])
        Batsman_Scored.append(row['Batsman_Scored'])
        Extra_Type.append(row['Extra_Type'])
        playerDissimalId.append(row['Player_dissimal_Id'])
        bowlerId.append(row['Bowler_Id'])
        extraRuns.append(row['Extra_Runs'])
        dissimalType.append(row['Dissimal_Type'])

    for index, i in enumerate(player_id):
        playertotalScore = 0
        ballCount = 0
        matchCount = 0
        matchDismissedCount = 0
        bowlerRun = 0
        bowlerBallCount = 0
        wicketCount = 0
        fourCount = 0
        sixCount = 0

        for indexk, k in enumerate(matchPlayedPId):
            if player_id[index] == matchPlayedPId[indexk]:
                matchCount = matchCount + 1

        for indexj, j in enumerate(Batsman_Scored):
            if Batsman_Scored[indexj] == " ":
                Batsman_Scored[indexj] = 0
            elif Batsman_Scored[indexj] != "Do_nothing":
                if player_id[index] == playerDissimalId[indexj]:
                    matchDismissedCount = matchDismissedCount + 1
                if player_id[index] == StrikerID[indexj]:
                    if (Extra_Type[indexj] == "wides"):
                        playertotalScore += int(Batsman_Scored[indexj])
                    else:
                        playertotalScore += int(Batsman_Scored[indexj])
                        ballCount = ballCount + 1

                    if Batsman_Scored[indexj] == "4":
                        fourCount = fourCount + 1
                    elif Batsman_Scored[indexj] == "6":
                        sixCount = sixCount + 1
                if player_id[index] == bowlerId[indexj]:
                    if Extra_Type[indexj] == "wides" or Extra_Type[indexj] == "noballs":
                        bowlerRun += int(Batsman_Scored[indexj]) + int(extraRuns[indexj])
                    else:
                        bowlerRun += int(Batsman_Scored[indexj])
                        bowlerBallCount = bowlerBallCount + 1

                    if dissimalType[indexj] == "caught" or dissimalType[indexj] == "bowled" or dissimalType[
                        indexj] == "lbw" or dissimalType[indexj] == "stumped" or dissimalType[
                        indexj] == "caught and bowled" or dissimalType[indexj] == "hit wicket":
                        wicketCount = wicketCount + 1

        matchNotOutCount = matchCount - matchDismissedCount

        if ballCount == 0:
            stRate = "%.2f" % (0.00)
        else:
            stRate = "%.2f" % ((playertotalScore / ballCount) * 100)

        if playertotalScore == 0:
            battingAvg = "%.2f" % (0.00)
        elif matchCount - matchNotOutCount == 0:
            battingAvg = "%.2f" % (0.00)
        else:
            battingAvg = "%.2f" % (playertotalScore / (matchCount - matchNotOutCount))

        totalDismissal.append(int(matchDismissedCount))
        totalScore.append(int(playertotalScore))
        strikeRate.append(float(stRate))
        battingAverage.append(float(battingAvg))
        ballsFaced.append(int(ballCount))

        totalFour.append(int(fourCount))
        totalSix.append(int(sixCount))

        if fourCount > 0 and ballCount > 0:
            avgFour = "%.2f" % ((fourCount / ballCount) * 100)
        else:
            avgFour = "%.2f" % (0.00)
        averageFour.append(avgFour)

        if sixCount > 0 and ballCount > 0:
            avgSix = "%.2f" % ((sixCount / ballCount) * 100)
        else:
            avgSix = "%.2f" % (0.00)
        averageSix.append(avgSix)

        if bowlerRun == 0:
            economy = "%.2f" % (0.00)
        else:
            economy = "%.2f" % (bowlerRun / (bowlerBallCount / 6))

        if wicketCount == 0:
            bowaverage = "%.2f" % (0.00)
            bowlingStrRate = "%.2f" % (0.00)
        else:
            bowaverage = "%.2f" % (bowlerRun / wicketCount)
            bowlingStrRate = "%.2f" % (bowlerBallCount / wicketCount)

        bowlingStrikeRate.append(float(bowlingStrRate))
        bowlingAverage.append(float(bowaverage))
        ballsBowled.append(int(bowlerBallCount))
        bowlerEconomy.append(float(economy))

playerData = []

for i, player in enumerate(player_id):
    playerHash = {}
    playerHash['player_id'] = player_id[i]
    playerHash['player_name'] = player_name[i]
    playerHash['batting_strike_rate'] = strikeRate[i]
    playerHash['batting_average'] = battingAverage[i]
    playerHash['total_scored'] = totalScore[i]
    playerHash['total_fours'] = totalFour[i]
    playerHash['average_fours_in_percentage'] = averageFour[i]
    playerHash['total_six'] = totalSix[i]
    playerHash['average_six_in_percentage'] = averageSix[i]
    playerHash['balls_faced'] = ballsFaced[i]
    playerHash['total_dismissal'] = totalDismissal[i]
    playerHash['bowling_average'] = bowlingAverage[i]
    playerHash['bowling_economy'] = bowlerEconomy[i]
    playerHash['bowling_strike_rate'] = bowlingStrikeRate[i]
    playerHash['balls_bowled'] = ballsBowled[i]

    playerData.append(playerHash)

with open('F:\SEM 1\Visual Analytics\Project\playerJsonData.json', 'w') as mainDataJSON:
    json.dump(playerData, mainDataJSON)