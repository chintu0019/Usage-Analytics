#!/usr/bin/env python3

import csv
import json
import sys
from operator import itemgetter

import patterns
import levenshtein
import log_utils


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)



def _convert_id2nnames(name2id, patterns):
    id2name = {}
    for name, idv in name2id.items():
        id2name[idv] = name

    npatterns = []
    for pattern, times in patterns:
        pl = []
        for element in pattern:
            pl.append(id2name[element])
        npatterns.append( (tuple(pl), times) )

    return npatterns



def _distance_from(ibase):
    def key(v):
        return ( levenshtein.levenshtein(v[0], ibase), -v[1] )
    return key



def _sort_results(found_patterns, sort_by):
    if sort_by != None:
        keyf = _distance_from(sort_by)
        rev = False
    else:
        keyf = itemgetter(1)
        rev = True
    return sorted( [ x for x in found_patterns.items() ], key=keyf, reverse=rev )




def real_main(min_length, csvlog_fn, jsonnumber_fn, numbers, sort_by):
    name2id = log_utils.load_name2id(jsonnumber_fn)
    actions = log_utils.read_actions(csvlog_fn, { 1 : log_utils.name2id_tsfr(name2id), }, 1)

    found_patterns = patterns.find_repetitions(actions, min_length)
    found_patterns = _sort_results(found_patterns, sort_by)

    if not numbers:
        found_patterns = _convert_id2nnames(name2id, found_patterns)

    for itm, times in found_patterns:
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
        min_length = int(argv[1])
        csvlog = argv[2]
        jsonnumber = argv[3]

        numbers = False
        sort_by = None

        for idx in range(4, len(argv)):
            if argv[idx] == '-n': numbers = True
            elif argv[idx] == '-s' and len(argv) > idx + 1:
                sort_by = tuple(int(x.strip()) for x in argv[idx + 1].split(','))

    except:
        eprint('Usage: prg len cvslog json_numbers [-n] [-s 1,2,...,n]')
        eprint('')
        eprint('-n display output in numbers, instead of action names')
        eprint('-s sort the results by distance from input sequence')
        eprint('')
        return 1

    try:
        return real_main(min_length, csvlog, jsonnumber, numbers, sort_by)
    except log_utils.NotLog:
        eprint('Error, the second column is not "actionName", are you sure this is a log?')
        return 2

if __name__ == "__main__":
    sys.exit(main())
