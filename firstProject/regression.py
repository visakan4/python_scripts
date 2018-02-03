import pandas as ps
import json
import numpy as np

match_data = ps.read_csv(filepath_or_buffer='D:/Semester1/VisualAnalytics/Project/indian-premier-league-csv-dataset/Match.csv')

match_by_groups = match_data.groupby(['Venue_Name'])

for name, match_by_group in match_by_groups:
    print name
