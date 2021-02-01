#!/usr/bin/env python3

# Author - Manoj Kesavulu

import os
import sys
import csv
import pandas
import shutil

import frequency
import timespent
import consistency

from pathlib import Path
from fnmatch import fnmatch


participants_file = Path("../Scenario/Participants.csv")
results_folder_10_path = '../Odoo10/results'
results_folder_11_path = '../Odoo11/results'
log_folder_10 = './Combined-log-folder/Log-folder-10'
log_folder_11 = './Combined-log-folder/Log-folder-11'
usage_data_file_10 = './Combined-log-folder/Usage-data-10.csv'
usage_data_file_11 = './Combined-log-folder/Usage-data-11.csv'
metrics_file_10 = "Insights/Metrics-10.csv"
metrics_file_11 = "Insights/Metrics-11.csv"
actions_file = "../Scenario/Actions_list.csv"


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def getParticipantsNames():
    if participants_file.exists():
        column_names = ["userID", "username"]
        p_file_data = pandas.read_csv(participants_file, names = column_names)
        return p_file_data.username.to_list()


def getParticipantsIds():
    if participants_file.exists():
        column_names = ["userID", "username"]
        p_file_data = pandas.read_csv(participants_file, names = column_names, skiprows=1)
        return p_file_data.userID.to_list()


def copyFiles(fileList, destinationFolder):
    for file in fileList:
            if file not in destinationFolder:
                shutil.copy(file, destinationFolder)


def getFileList(path):
    pattern = "*.csv"
    filesToFind = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, pattern):
                dirpath, dirname = os.path.split(path)
                if name.startswith(dirname, 0, len(name)):
                    filesToFind.append(os.path.join(path, name))
    return filesToFind


def updateCombinedLogFile(odoo_version):
    participants_list = getParticipantsNames()
    #print(participants_list)
    fileList = []

    if odoo_version == '10':
        fileList = getFileList(results_folder_10_path)
        copyFiles(fileList, log_folder_10)
        #combine all files in the list
        combined_csv = pandas.concat([pandas.read_csv(f) for f in fileList])
        #export to csv
        combined_csv.to_csv(usage_data_file_10, index=False, encoding='utf-8-sig')
        usage_data_file = Path(usage_data_file_10)

    elif odoo_version == '11':
        fileList = getFileList(results_folder_11_path)
        copyFiles(fileList, log_folder_11)
        combined_csv = pandas.concat([pandas.read_csv(f) for f in fileList])
        combined_csv.to_csv(usage_data_file_11, index=False, encoding='utf-8-sig')
        usage_data_file = Path(usage_data_file_11)
    return usage_data_file


def initialiseMetricsFile(odoo_version):
    actions_data = pandas.read_csv(actions_file)
    actionsList = actions_data.actionName.to_list()
    userIdList = getParticipantsIds()

    with open(metrics_file_10, mode='w') as mFile:
        csv_header = ['userId', 'actionName', 'frequency', 'timeSpent', 'consistency']
        csv_writer = csv.writer(mFile)
        csv_writer.writerow(csv_header)
        for userId in userIdList:
            for action in actionsList:
                csv_writer.writerow([userId, action, 0, 0, 0])


def realMain(odoo_version):
    usage_data_file = updateCombinedLogFile(odoo_version)
    initialiseMetricsFile(odoo_version)
    frequency.start(odoo_version, usage_data_file)
    timespent.start(odoo_version, usage_data_file)
    
    #TODO - call frequency, timespent and consistency metrics
    #TODO - behavioural score


def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    odoo_version = argv[1]
    #print(odoo_version)
    realMain(odoo_version)
    #try:
    #    odoo_version = argv[1]
    #    #print(odoo_version)
    #    realMain(odoo_version)
    #except:
    #    eprint('\nEnter the Version of the Odoo (10 or 11)')
    #    eprint('\nProgram to start the analysis, pass the version of the odoo application as an argument \n')
    #    eprint('Usage: python start_analysis.py odoo_version')
    #    eprint('Example: python start_analysis.py 10 \n')


if __name__ == "__main__":
    sys.exit(main())