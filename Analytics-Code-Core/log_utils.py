#!/usr/bin/env python3

import csv
import json
import utils
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



def in_date_range(start, end, colname):
    def lower(row):
        return row[colname] >= start
    def upper(row):
        return row[colname] < end

    if start == None and end == None:
        return lambda x : True

    if start == None:
        return upper

    if end == None:
        return lower

    return lambda x : lower(x) and upper(x)



class Read_action_opt(utils.Frozen):
    def __init__(self):
        self.csvlog_fn = None
        self.transformators = {}
        self.col_names = {}
        self.filter = lambda x : True

        self.frozen = True



def _get_line_ex(opt, row):
    action = {}
    for idx, readable_name in opt.col_names.items():
        action[readable_name] = opt.transformators.get(idx, lambda x:x)( row[idx] )
    return action if opt.filter(action) else None



def read_actions_ex(opt):
    actions = []
    with open(opt.csvlog_fn, 'r') as csvlog:
        csvlog_reader = csv.reader(csvlog)
        first = True
        for row in csvlog_reader:
            if first:
                first = False
                if row[1] != 'actionName':
                    raise NotLog
            else:
                action = _get_line_ex(opt, row)
                if action: actions.append(action)

    return actions

