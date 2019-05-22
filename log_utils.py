#!/usr/bin/env python3

import csv
import json
from datetime import datetime 

class NotLog(Exception):
    pass



def load_name2id(jsonnumber_fn):
    with open(jsonnumber_fn, 'r') as jsonnumber:
        name2id = json.load(jsonnumber)
    return name2id



def timestap2date_tsfr(timestamp_str):
    return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')



def name2id_tsfr(name2id):
    def f(name):
        return name2id[name]
    return f



def _identity(x): return x



def _get_line(transformators, row, cols_id):
    if type(cols_id) == tuple:
        d = []
        for idx in cols_id:
            d.append( transformators.get(idx, _identity)( row[idx] ) )
        return tuple(d)

    else:
        return transformators.get(cols_id, _identity)( row[cols_id] )



def read_actions(csvlog_fn, transformators, cols_id):
    actions = []
    with open(csvlog_fn, 'r') as csvlog:
        csvlog_reader = csv.reader(csvlog)
        first = True
        for row in csvlog_reader:
            if first:
                first = False
                if row[1] != 'actionName':
                    raise NotLog
            else:
                actions.append( _get_line(transformators, row, cols_id) )

    return actions
