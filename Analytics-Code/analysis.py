#!/usr/bin/env python3

import csv
import os
import sys
from pathlib import Path

odoo_version = None
results_folder = None


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def getResultsFolder(odoo_version):
    rfolder = None
    if odoo_version == '10':
        rfolder = Path("../Odoo10/results/")
    elif odoo_version == '11':
        rfolder = Path("../Odoo11/results/")        
    return rfolder


def getResultFiles(rfolder):
    rfiles = None
    for root, dirs, files in os.walk(rfolder):
        for dirname in dirs:            
            for filename in files:
                if filename.startswith(dirname):
                    print(filename)
            
#todo - list files whose filename starts with the directory name

def realMain(odoo_version):
    results_folder = getResultsFolder(odoo_version)
    results_files = getResultFiles(results_folder)


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