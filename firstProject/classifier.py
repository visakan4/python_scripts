import json
import numpy as np
from random import shuffle
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
from sklearn import svm

def getInputValues():
    ipath = "inputValues.json"
    with open(ipath,"r") as ip:
        input_data = json.loads(ip.read())
        keySetLength = len(input_data.items())
        X_predict = np.zeros((1,keySetLength))
        input_data_as_vec = np.array([])
        input_features = [
            "NumberOfBangladesPlayers",
            "NumberOfPlayersabove30",
            "NumberOfAustralianPlayers",
            "NumberOfEnglandPlayers",
            "NumberOfOtherPlayers",
            "tosswinner",
            "NumberOfSouthAfricanPlayers",
            "NumberOfRightHandedPlayers",
            "NumberOfNewzealandPlayers",
            "NumberOfSrilankanPlayers",
            "NumberOfPlayersbetween24and30",
            "NumberOfLeftHandedPlayers",
            "NumberOfPlayersbetween18and24",
            "NumberOfWestIndianPlayers",
            "NumberOfPakistanPlayers",
            "batting"
        ]
        for i in range(len(input_features)):
            tsf_val = input_data.get(input_features[i])
            if input_features[i] == "batting":
                if input_data.get(input_features[i]) == "first":
                    tsf_val = 0
                else:
                    tsf_val = 1
            input_data_as_vec = np.append(input_data_as_vec, tsf_val)
        X_predict[0] = input_data_as_vec
    return X_predict


def get_dataset():
    train_perc = 0.90
    fpath = "team_analysis.json"
    with open(fpath, "r") as fh:
        all_data = json.loads(fh.read())
        # shuffle(all_data) # Shuffles data every time, to generate diff test, train set
        feat_count = len(all_data[0].items()) - 2  # -1 for excluding "winner"
        X = np.zeros((len(all_data), feat_count))
        Y = np.zeros((len(all_data), 1))
        for idx in range(0, len(all_data)):
            data = all_data[idx]
            features = [
                "NumberOfBangladesPlayers",
                "NumberOfPlayersabove30",
                "NumberOfAustralianPlayers",
                "NumberOfEnglandPlayers",
                "NumberOfOtherPlayers",
                "tosswinner",
                "NumberOfSouthAfricanPlayers",
                "NumberOfRightHandedPlayers",
                "NumberOfNewzealandPlayers",
                "NumberOfSrilankanPlayers",
                "NumberOfPlayersbetween24and30",
                "NumberOfLeftHandedPlayers",
                "NumberOfPlayersbetween18and24",
                "NumberOfWestIndianPlayers",
                "NumberOfPakistanPlayers",
                "batting"
            ]
            # X
            data_as_vec = np.array([])
            for j in range(len(features)):
                tsf_val = data.get(features[j])
                if features[j] == "batting":
                    if data.get(features[j]) == "first":
                        tsf_val = 0
                    else:
                        tsf_val = 1
                data_as_vec = np.append(data_as_vec, tsf_val)
            X[idx] = data_as_vec

            # Y
            if data.get("winner") == "no":
                tsf_val = 0
            elif data.get("winner") == "yes":
                tsf_val = 1
            else:
                tsf_val = 2
            Y[idx] = tsf_val

    tot = X.shape[0]
    train_samples = int(tot * train_perc)
    return X[0:train_samples, :], Y[0:train_samples, :], X[train_samples:tot, :], Y[train_samples:tot, :]


def predict(clf, x):
    return clf.predict(x)


def train(X_train,Y_train,classifier):
    if (classifier == 0):
        clf = MultinomialNB()
    elif (classifier == 1):
        clf = tree.DecisionTreeClassifier()
    elif (classifier == 2):
        clf = svm.SVC(probability=True)
    else:
        print classifier
    return clf.fit(X_train, Y_train)

def evaluate(predicted, Y_test):
    mean_acc = np.mean(predicted == Y_test)
    print "Mean Accuracy:", mean_acc
    print(metrics.classification_report(Y_test, predicted))


def test(clf, X_test):
    return clf.predict(X_test)


def classifier():
    inputValues = getInputValues()
    print inputValues
    X_train, Y_train, X_test, Y_test = get_dataset()
    clf = train(X_train, Y_train,0)
    predicted = test(clf, X_test)
    evaluate(predicted, Y_test)
    print inputValues
    prediction = predict(clf, inputValues)
    print prediction
    print clf.predict_proba(inputValues)

classifier()