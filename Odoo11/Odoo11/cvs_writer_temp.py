#!/usr/bin/env python3

import csv
from datetime import datetime
import os
import threading
from os.path import isfile, join, listdir
import time

class CvsWriter:
    writers = {}

    def __init__(self, foldername, column_names_tuple = None):
        self.foldername = os.path.abspath(foldername)
        files = [f for f in listdir(self.foldername) if isfile(join(self.foldername, f))]
        files.sort()
        filename = files[-1]
        if not len(files) == 0:
            self._recover(filename)
        else:
            self._first_init(foldername, column_names_tuple)

    def _recover(self, filename):
        self.__dict__ = CvsWriter.writers[filename]

    def _first_init(self, foldername, column_names_tuple):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + ".csv"
        CvsWriter.writers[filename] = CvsWriter.writers.get(filename, {})
        self.__dict__ = CvsWriter.writers[filename]

        self.write_lock = threading.Lock()
        self.column_names = {}
        self.filename = os.path.abspath(filename)
        self.id_to_ip = {}

        label_row = []
        for idx, column_name in enumerate(column_names_tuple):
            self.column_names[column_name] = idx
            label_row.append(column_name)

        with self.write_lock, open(self.filename, 'w') as f:
            csv.writer(f).writerow(label_row)

    def connect_id_to_ip(self, userId, userIp):
        with self.write_lock:
            self.id_to_ip[userId] = userIp

    def write(self, elements_dict):
        with self.write_lock, open(self.filename, 'a') as f:
            if 'userId' in elements_dict and not 'ipAddr' in elements_dict:
                elements_dict['ipAddr'] = self.id_to_ip.get(elements_dict['userId'], '')
            if not 'timestamp' in elements_dict:
                elements_dict['timestamp'] = datetime.now()

            row = ['']*len(self.column_names)

            for column_name, value in elements_dict.items():
                row[ self.column_names[column_name] ] = str(value)

            csv.writer(f).writerow(row)
