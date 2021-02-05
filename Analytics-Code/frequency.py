#!/usr/bin/env python3


import pandas
import progressBar as PB


def updateFrequency(metrics_file):
    mFile = pandas.read_csv(metrics_file)
    total_timespent = 0

    for index, row in mFile.iterrows():
        total_timespent += row["timespent"]
    
    for index, row in mFile.iterrows():
        mFile.at[index, "frequency"] = (float(mFile.at[index, "occurrences"])/total_timespent)*100
    mFile.to_csv(metrics_file, index=False)


def updateFrequencyActionName(ud_userId, ud_actionName):
    mFile = pandas.read_csv(metrics_file)

    for index, row in mFile.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            mFile.at[index, "occurrences"] += 1

    mFile.to_csv(metrics_file, index=False)


def analyse(odoo_version, log_files_list):
    print("\nOdoo "+odoo_version+": Frequency Analysis.....\n")
    PB.printProgress(0, len(log_files_list), prefix = 'Frequency Analysis:', suffix = 'Complete', length = 50)
    global metrics_file 
    metrics_file = "Insights/Metrics-" + odoo_version + "-frequency-timespent.csv"

    for file in log_files_list:
        usage_data = pandas.read_csv(file)
        for index, row in usage_data.iterrows():
            updateFrequencyActionName(row["userId"], row["actionName"])
            PB.printProgress(index + 1, len(usage_data), prefix = file, suffix = 'Complete', length = 50)
    updateFrequency(metrics_file)