import scipy
import pandas as ps

match_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/data.csv')

feature_columns = ['batting position','batting first']
X = match_data[feature_columns]
y = match_data.strike_rate_over_10

# print X
# print match_data.strike_rate_over_1

# follow the usual sklearn pattern: import, instantiate, fit
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X, y)

# print intercept and coefficients
# print lm.intercept_
# print lm.coef_

print lm.predict([[4,1]])
print lm.predict([[4,2]])

# from sklearn.multioutput import MultiOutputRegressor
# lm = MultiOutputRegressor()
# lm.fit(X, y)
#
# # print intercept and coefficients
# # print lm.intercept_
# # print lm.coef_
#
# print lm.predict([[4,1]])
# print lm.predict([[4,2]])