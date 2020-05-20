#!/usr/bin/env python3

import os
import shutil
from glob import glob
from fnmatch import fnmatch


def listLogs(src):
    pattern = "*.csv"
    for path, subdirs, files in os.walk(src):
        for name in files:
            if fnmatch(name, pattern):
                print(os.path.join(path, name))
            #print("path = " + path + "\nsubdirs = " + subdirs + "\nfiles = ")
            #print("path = " + "\nsubdirs = " + "\nfiles = ")


def listLogs2(src):
    pattern = "*.csv"
    for path, subdirs, files in os.walk(src):
        for name in files:
            if fnmatch(name, pattern):
                dirpath, dirname = os.path.split(path)
                if name.startswith(dirname, 0, len(name)):
                    print(os.path.join(path, name))


def copyFiles():
    src10  = '../Odoo10/results/'
    src11  = os.listdir("../Odoo11/results/")
    dest10 = os.listdir("../Odoo10/Log-folder/")
    dest11 = os.listdir("../Odoo11/Log-folder/")

    gsrc10  = glob("../Odoo10/results/")
    gsrc11  = glob("../Odoo11/results/")
    gdest10 = glob("../Odoo10/Log-folder/")
    gdest11 = glob("../Odoo11/Log-folder/")

    listLogs2(src10)


copyFiles()    