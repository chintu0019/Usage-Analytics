#!/usr/bin/env python3

import csv
from datetime import datetime
import os
from os import path
import threading
import time

class CsvWriter:
    writers = {}

    def __init__(self, dirname, column_names_tuple = None):
        if column_names_tuple == None:
            self._recover(dirname)
        else:
            self._first_init(dirname, column_names_tuple)

    def _recover(self, dirname):
        dirname = os.path.abspath(dirname)
        self.__dict__ = CsvWriter.writers[dirname]

    def _first_init(self, dirname, column_names_tuple):
        dirname = os.path.abspath(dirname)
        CsvWriter.writers[dirname] = {}
        self.__dict__ = CsvWriter.writers[dirname]

        self.filename = path.join(os.path.abspath(dirname), time.strftime("%Y%m%d-%H%M%S", time.gmtime()) + '.csv')

        self.write_lock = threading.Lock()
        self.column_names = {}
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
