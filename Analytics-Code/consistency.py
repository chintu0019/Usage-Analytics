#!/usr/bin/env python3


import pandas
import progressBar as PB


def getFrequency(ud_userId, ud_actionName, ud_df):
    for index, row in ud_df.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            return ud_df.at[index, "frequency"]


def getTimespent(ud_userId, ud_actionName, ud_df):
    for index, row in ud_df.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            return ud_df.at[index, "timespent"]


def measureConsistency(ud_userId, ud_actionName):
    ft_10_df = pandas.read_csv("Insights/Metrics-10-frequency-timespent.csv")
    ft_11_df = pandas.read_csv("Insights/Metrics-11-frequency-timespent.csv")
    metric_consistency_df = pandas.read_csv("Insights/Metrics-consistency.csv")
    
    for index, row in metric_consistency_df.iterrows():
        if row["userId"] == ud_userId and row["actionName"] == ud_actionName:
            metric_consistency_df.at[index, "consistency (frequency)"] = getFrequency(ud_userId, ud_actionName, ft_10_df) - getFrequency(ud_userId, ud_actionName, ft_11_df)
            metric_consistency_df.at[index, "consistency (timespent)"] = getTimespent(ud_userId, ud_actionName, ft_10_df) - getTimespent(ud_userId, ud_actionName, ft_11_df)
    
    metric_consistency_df.to_csv("Insights/Metrics-consistency.csv", index=False)


def analyse():
    print("\n-----------------------")
    print("\nConsistency Analysis...")
    metric_consistency_df = pandas.read_csv("Insights/Metrics-consistency.csv")
    PB.printProgress(0, len(metric_consistency_df), prefix = 'Timespent Analysis:', suffix = 'Complete', length = 50)
    for index, row in metric_consistency_df.iterrows():
        measureConsistency(row["userId"], row["actionName"])
        PB.printProgress(index+1, len(metric_consistency_df), prefix = 'Consistency Analysis:', suffix = 'Complete', length = 50)