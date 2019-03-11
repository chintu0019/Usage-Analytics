#!/usr/bin/env python3

import os
import threading
import csv

class CvsWriter:
    writers = {}

    def __init__(self, filename, column_names_tuple = None):
        if column_names_tuple == None:
            self._recover(filename)
        else:
            self._first_init(filename, column_names_tuple)

    def _recover(self, filename):
        self.__dict__ = CvsWriter.writers[filename]

    def _first_init(self, filename, column_names_tuple):
        CvsWriter.writers[filename] = CvsWriter.writers.get(filename, {})
        self.__dict__ = CvsWriter.writers[filename]

        self.write_lock = threading.Lock()
        self.column_names = {}
        self.filename = os.path.abspath(filename)

        label_row = []
        for idx, column_name in enumerate(column_names_tuple):
            self.column_names[column_name] = idx
            label_row.append(column_name)

        with self.write_lock, open(self.filename, 'w') as f:
            csv.writer(f).writerow(label_row)

    def write(self, elements_dict):
        with self.write_lock, open(self.filename, 'a') as f:
            row = ['']*len(self.column_names)

            for column_name, value in elements_dict.items():
                row[ self.column_names[column_name] ] = str(value)

            csv.writer(f).writerow(row)