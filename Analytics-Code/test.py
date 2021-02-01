#!/usr/bin/env python3

from datetime import datetime
import pandas
from pathlib import Path

from pandas.io.parsers import read_csv


participants_file = '../Scenario/Participants.csv'
results_folder_10_path = '../Odoo10/results'
results_folder_11_path = '../Odoo11/results'
log_folder_10 = './Combined-log-folder/Log-folder-10'
log_folder_11 = './Combined-log-folder/Log-folder-11'
usage_data_file_10 = './Combined-log-folder/Usage-data-10.csv'
usage_data_file_11 = './Combined-log-folder/Usage-data-11.csv'
metrics_file_10 = "Insights/Metrics-10.csv"
actions_file = "../Scenario/Actions_list.csv"

def getTimestamp(date_time):
    date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f')
    return datetime.timestamp(date_time_obj)

uFile = pandas.read_csv(usage_data_file_10)
index = 1
a = "actionName"
print(uFile.at[index, "actionName"], uFile.at[index, "userId"], getTimestamp(uFile.at[index, "timestamp"]))
print(uFile.at[index+1, "actionName"], uFile.at[index+1, "userId"], getTimestamp(uFile.at[index+1, "timestamp"]))
print(getTimestamp(uFile.at[index+1, "timestamp"])-getTimestamp(uFile.at[index, "timestamp"]))