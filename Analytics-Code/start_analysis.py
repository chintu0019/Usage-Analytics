#!/usr/bin/env python3

# Author - Manoj Kesavulu

import os
import sys
import csv
import pandas
import shutil
from fnmatch import fnmatch
from pathlib import Path


participants_file = Path("../Scenario/Participants.csv'")
results_folder_10_path = '../Odoo10/results'
results_folder_11_path = '../Odoo11/results'
log_folder_10 = '.Combined-log-folder/Log-folder-10'
log_folder_11 = '.Combined-log-folder/Log-folder-11'


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def getParticipantsList():
    if participants_file.exists():
        column_names = ["userID", "username"]
        p_file_data = pandas.read_csv(participants_file, names = column_names)
        return p_file_data.username.to_list()


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
    participants_list = getParticipantsList()
    fileList = []

    if odoo_version == '10':
        fileList = getFileList(results_folder_10_path)
        copyFiles(fileList, log_folder_10)

    elif odoo_version == '11':
        fileList = getFileList(results_folder_11_path)
        copyFiles(fileList, log_folder_11)

    #TODO - code to merge the csv files in Combined-log-folder into a single file
    

def realMain(odoo_version):
    updateCombinedLogFile(odoo_version)


def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    try:
        odoo_version = argv[1]
        #print(odoo_version)
        realMain(odoo_version)
    except:
        eprint('\nEnter the Version of the Odoo (10 or 11)')
        eprint('\nProgram to start the analysis, pass the version of the odoo application as an argument \n')
        eprint('Usage: python start_analysis.py odoo_version')
        eprint('Example: python start_analysis.py 10 \n')


if __name__ == "__main__":
    sys.exit(main())