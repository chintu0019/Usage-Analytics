#!/usr/bin/env python3


import pandas


def updateFrequencyActionName(odoo_version, ud_userId, ud_actionName):
    mFile = pandas.read_csv(metrics_file)
    for index, row in mFile.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            mFile.at[index, "frequency"] += 1
    mFile.to_csv(metrics_file, index=False)


def start(odoo_version, usage_data_file):
    global metrics_file 
    metrics_file = "Insights/Metrics-"+odoo_version+".csv"
    usage_data = pandas.read_csv(usage_data_file)
    for index, row in usage_data.iterrows():
        updateFrequencyActionName(odoo_version, row["userId"], row["actionName"])