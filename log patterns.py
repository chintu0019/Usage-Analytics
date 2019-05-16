#!/usr/bin/env python3

import csv
import json
import sys

import patterns


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def convert_id2nnames(name2id, patterns):
    id2name = {}
    for name, idv in name2id.items():
        id2name[idv] = name

    npatterns = {}
    for pattern, times in patterns.items():
        pl = []
        for element in pattern:
            pl.append(id2name[element])
        npatterns[tuple(pl)] = times
    return npatterns


def real_main(length, csvlog_fn, jsonnumber_fn):
    with open(jsonnumber_fn, 'r') as jsonnumber:
        name2id = json.load(jsonnumber)

    actions = []
    with open(csvlog_fn, 'r') as csvlog:
        csvlog_reader = csv.reader(csvlog)
        first = True
        for row in csvlog_reader:
            if first:
                first = False
                if row[1] != 'actionName':
                    eprint('Error, the second column is not "actionName", are you sure this is a log?')
                    return 1
            else:
                actions.append( name2id[row[1]] )

    found_patterns = convert_id2nnames(name2id, patterns.find_repetitions(actions, length))

    for itm, times in found_patterns.items():
        print(times, ":", itm)

    return 0



def main(argv=None):
    """ Program starting point, it can started by the OS or as normal function

        If it's a normal function argv won't be None if started by the OS
        argv is initialized by the command line arguments
    """
    if argv is None:
        argv = sys.argv

    try:
        length = int(argv[1])
        csvlog = argv[2]
        jsonnumber = argv[3]
    except:
        eprint('Usage: prg len cvs_log json_numbers')
        return 1

    return real_main(length, csvlog, jsonnumber)

if __name__ == "__main__":
    sys.exit(main())
