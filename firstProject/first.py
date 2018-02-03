import os
import numpy as np
import pandas as pd
import json

script_dir = os.path.dirname("D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/")
# script_dir = os.path.dirname("C:/Users/visak/Desktop/")
fileName = "Match.csv"
filePath = os.path.join(script_dir,fileName)
file = open(filePath,"r")

data =[]

for index, line in enumerate(file):
    if index == 0:
        header = line.replace("'","").replace("\n","").split(",")
        # print len(header),"header"
    else:
        values = line.replace('"',"").replace("\n","").split(",")
        if (len(values)>len(header)):
            temp = values
            values = []
            i =0
            for value in temp:
                if (i == 5):
                    values.append(temp[i]+" - "+temp[i+1])
                    i+=2
                elif (i==7):
                    i+=1
                else:
                    values.append(value)
                    i+=1
        hashValue = {}
        for i,value in enumerate(values):
            hashValue[header[i]] = value
        data.append(hashValue)

s = pd.DataFrame(data)

groups = s.groupby('Venue_Name')

a = s['Venue_Name'].value_counts()

analysisData = []
jsonHeader = ['groundID','groundName','numberofMatchesPlayed','winPercentagePlayingFirst','winPercentagePlayingSecond','winPercentageWinningToss','winPercentageLosingToss']
groupIndex = 0
for name,group in groups:
    value = 0
    battingFirst = 0
    groundData = []
    groundHash = {}
    numberOfMatches = group.size / len(header)
    for index, row in group.iterrows():
        if (row['Match_Winner_Id'] == row['Toss_Winner_Id']):
            value+=1
        if ((row['Toss_Decision']=='bat') & (row['Toss_Winner_Id'] == row['Match_Winner_Id']) | (row['Toss_Decision']=='field') & (row['Toss_Winner_Id'] != row['Match_Winner_Id'])):
            battingFirst+=1
    groundData.append(groupIndex)
    groundData.append(name)
    groundData.append(numberOfMatches)
    groundData.append((float(battingFirst)/float(numberOfMatches))*100)
    groundData.append(((float(numberOfMatches) - float(battingFirst))/float(numberOfMatches))*100)
    groundData.append((float(value) / float(numberOfMatches)) * 100)
    groundData.append(((float(numberOfMatches) - float(value)) / float(numberOfMatches)) * 100)
    for i,groundDataValue in enumerate(groundData):
        groundHash[jsonHeader[i]] = groundDataValue
    analysisData.append(groundHash)
    groupIndex += 1


print analysisData

analysisJSON = json.dumps(analysisData)

print analysisJSON

