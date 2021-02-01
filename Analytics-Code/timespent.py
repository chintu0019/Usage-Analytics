#!/usr/bin/env python3


import pandas
from datetime import datetime
from numpy.core.numeric import NaN
from fnmatch import fnmatch


def toTimestamp(date_time):
    date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f')
    return datetime.timestamp(date_time_obj)


def getTimestamp(index, uDF):
    for i, row in uDF.iterrows():
        if index == i:
            return toTimestamp(uDF.at[i, "timestamp"])


def updateTimespentAction(usage_data_file, ud_userId, ud_actionName):
    uDF = pandas.read_csv(usage_data_file)
    mDF = pandas.read_csv(metrics_file)
    time_spent = 0

    for index, row in uDF.iterrows():
        if index == len(uDF): break
        next_index = index+1
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName and row["userId"] == uDF.at[next_index, "userId"]: #BUG - error here with index+1 or next_index
            time_spent = time_spent + (getTimestamp(index+1, uDF) - getTimestamp(index, uDF))

    for index, row in mDF.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            mDF.at[index, "timeSpent"] = time_spent
    mDF.to_csv(metrics_file, index=False)
    

def start(odoo_version, usage_data_file):
    global metrics_file
    metrics_file = "Insights/Metrics-"+odoo_version+".csv"
    usage_data = pandas.read_csv(usage_data_file)
    for index, row in usage_data.iterrows():
        updateTimespentAction(usage_data_file, row['userId'], row['actionName'])