#!/usr/bin/env python3

# Author - Manoj Kesavulu

import os
import sys
import csv
import pandas
from pathlib import Path


participants_file = Path("../Scenario/Participants.csv")
results_folder_10_path = Path("../Odoo10/results")
results_folder_11_path = Path("../Odoo11/results")


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def getParticipantsList():
    if participants_file.exists():
        column_names = ["userID", "username"]
        p_file_data = pandas.read_csv(participants_file, names = column_names)
        return p_file_data.username.to_list()
            

def getLogFiles(odoo_version):
    participants_list = getParticipantsList()
    #print(participants_list)
    if odoo_version == 10:
        


def realMain(odoo_version):
    getLogFiles(odoo_version)


def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    try:
        odoo_version = argv[1]
        realMain(odoo_version)
    except:
        eprint('\nEnter the Version of the Odoo (10 or 11)')
        eprint('\nProgram to start the analysis, pass the version of the odoo application as an argument \n')
        eprint('Usage: analysis.py odoo_version')
        eprint('Example: python analysis.py 10 \n')


if __name__ == "__main__":
    sys.exit(main())