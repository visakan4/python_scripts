import os
import re
import string
import json
from flask import Flask
from flask_cors import CORS,cross_origin
from flask import request
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

#readFile
def readFiles(filePath,fileName):
    fileLocation = filePath+"/"+fileName
    return open(fileLocation).read()

#get the values of the files in a array
def getFileData(dataSetPath,fileList):
    dataSet = []
    for f in fileList:
        dataSet.append(readFiles(dataSetPath,f))
    return dataSet

#get Labels from the fileList
def getLabels(fileList):
    fileNames = []
    for file in fileList:
        fileNames.append(file.split("_")[0])
    return fileNames

# read Files from a folder
def readDataset(dataSetPath, splitPercent):
    fileList = os.listdir(dataSetPath)
    fileNames = getLabels(fileList)
    dataSet = getFileData(dataSetPath,fileList)
    X_train, X_test, X_train_labels, X_test_lables = train_test_split(dataSet,fileNames,test_size=splitPercent)
    return dataSet,fileNames,X_train, X_test, X_train_labels, X_test_lables

#preProcess
# lowercase the values
# remove the punctuations
# remove numbers

def preprocess(corpus,lower,punc,number):
    for index,data in enumerate(corpus):
        data = re.sub('\s+', '  ', data).strip()
        if (lower):
            data = data.lower()
        if (punc):
            for punctuation in string.punctuation:
                data = data.replace(punctuation, "")
        if (number):
            data = re.sub(r'[0-9]','',data)
        corpus[index] = data
    return (corpus)

# get Document Matrix
# split the document matrix into train and test

def getDocumentTermMatrix(corpus,fileNames,style,splitPercent):
    if (style == 'count'):
        countVector = CountVectorizer(ngram_range=(1, 1))
        count_document_matrix = countVector.fit_transform(corpus)
        count_document_matrix_label_names = countVector.get_feature_names()
        train_document_matrix, test_document_matrix, train_label, test_label = train_test_split(count_document_matrix,fileNames,test_size=splitPercent)
        return train_document_matrix, test_document_matrix, train_label, test_label
    elif (style == 'tf_idf'):
        tf_idf = TfidfVectorizer(ngram_range=(1,1))
        tf_idf_matrix = tf_idf.fit_transform(corpus)
        tf_idf_matrix_label_names = tf_idf.get_feature_names()
        train_document_matrix, test_document_matrix, train_label, test_label = train_test_split(tf_idf_matrix,fileNames,test_size=splitPercent)
        return train_document_matrix, test_document_matrix, train_label, test_label

#Train model based on the classifier name
def trainModel(document_term_matrix, X_train_labels,classifierName,svmkernel,max_depth_value,mlpactivation,mlpsolver):
    if (classifierName == 'svm'):
        classifier = svm.SVC(kernel=str(svmkernel))
    elif (classifierName == 'decisiontree'):
        classifier = DecisionTreeClassifier(max_depth=max_depth_value)
    elif (classifierName == 'randomForestClassifier'):
        classifier = RandomForestClassifier(max_depth=max_depth_value,n_estimators=1,max_features=1)
    elif (classifierName == 'naive-bayes'):
        classifier = GaussianNB()
    elif (classifierName == 'mlp'):
        classifier = MLPClassifier(solver=mlpsolver, activation=mlpactivation,alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    if (classifierName == 'naive-bayes'):
        return classifier.fit(document_term_matrix.toarray(), X_train_labels)
    else:
        return classifier.fit(document_term_matrix, X_train_labels)

# PredictValues for the test document matrix
def predictValues(classifier,test_document_matrix,classifierName):
    if (classifierName == 'naive-bayes'):
        return classifier.predict(test_document_matrix.toarray())
    else:
        return classifier.predict(test_document_matrix)

# getAccuracy score of the classifier
def evaluate(true_label,predicted_labels):
    return (accuracy_score(true_label, predicted_labels))

#workflow function
# Read the files
# Process the dataSet
# Document Train Matrix and split into train and test
# train the model
# predict the values
# get Accuracy score
# create hash
# convert and return the json to front end

def flow(splitPercent,lower,punc,number,style,svmkernel,max_depth_value,mlpactivation,mlpsolver):
    dataSet, fileNames, X_train, X_test, X_train_labels, X_test_lables = readDataset("./classification",0.25)
    preProcessedDataSet = preprocess(dataSet,lower,punc,number)
    train_document_matrix, test_document_matrix, train_label, test_label = getDocumentTermMatrix(preProcessedDataSet,fileNames,style,splitPercent)
    classifierNames = ["svm","naive-bayes","mlp","randomForestClassifier","decisiontree"]
    valueTobeReturned = []
    for classifierName in classifierNames:
        classifierValue = {}
        classifier = trainModel(train_document_matrix,train_label,classifierName,svmkernel,max_depth_value,mlpactivation,mlpsolver)
        predicted_labels = predictValues(classifier,test_document_matrix,classifierName)
        accuracy_value = evaluate(test_label,predicted_labels)
        classifierValue['classifier_name'] = classifierName
        classifierValue['classifier_accuracy'] = accuracy_value * 100
        valueTobeReturned.append(classifierValue)
    return json.dumps(valueTobeReturned)


# getValues from the request and store to a number
def getValues(jsonData):
    number = jsonData['numbers']
    lower = jsonData['lowerCase']
    punctuations = jsonData['punctuations']
    splitPercent = jsonData['splitPercent']
    style = jsonData['style']
    svmkernel = jsonData['kernel']
    max_depth = int(jsonData['max_depth'])
    mlpactivation = jsonData['mlpactivation']
    mlpsolver = jsonData['mlpsolver']
    return number, lower, punctuations, splitPercent, style, svmkernel, max_depth, mlpactivation, mlpsolver


@app.route("/getValues",methods=['GET','POST'])
@cross_origin()
def getAccuracy():
    number, lower, punctuations, splitPercent, style, svmkernel, max_depth, mlpactivation, mlpsolver = getValues(request.get_json())
    return flow(splitPercent,lower,punctuations,number,style,svmkernel,max_depth,mlpactivation,mlpsolver)


if __name__ == '__main__':
    app.run()
