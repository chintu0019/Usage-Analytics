#!/usr/bin/env python3


import pandas
import progressBar as PB
from datetime import datetime


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
    time_spent = 0.0

    #PB.printProgress(0, len(uDF), prefix = 'Timespent Analysis:', suffix = 'Complete', length = 50)
    for index, row in uDF.iterrows():
        if index == len(uDF)-1: break # break the loop if this is the last item in the loop
        if row["actionName"] == ud_actionName:
            time_spent = time_spent + (float(getTimestamp(index+1, uDF)) - float(getTimestamp(index, uDF)))
            #PB.printProgress(index+1, len(uDF), prefix = 'Timespent Analysis:', suffix = 'of', length = 40)

    for index, row in mDF.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            mDF.at[index, "timespent"] = time_spent
    mDF.to_csv(metrics_file, index=False)
    

def analyse(odoo_version, log_files_list):
    print("\nOdoo "+odoo_version+": Timespent Analysis.....\n")
    global metrics_file
    metrics_file = "Insights/Metrics-" + odoo_version + "-frequency-timespent.csv"
    PB.printProgress(0, len(log_files_list), prefix = 'Timespent Analysis:', suffix = 'Complete', length = 50)
    
    for file in log_files_list:
        usage_data = pandas.read_csv(file)
        for index, row in usage_data.iterrows():
            PB.printProgress(index+1, len(usage_data), prefix = file, suffix = 'Complete', length = 50)
            updateTimespentAction(file, row["userId"], row["actionName"])