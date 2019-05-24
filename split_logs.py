#!/usr/bin/env python3

import csv
import sys
import os

def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def get_file(split, csvlog_fn, header, userid):
    fname = 'u' + userid + '_' + csvlog_fn
    f = split.get(fname, None)
    if f != None:
        return f

    if os.path.isfile(fname):
        raise Exception(fname + ' already exists!')

    f = open(fname, 'w')
    split[fname] = f

    csv.writer(f).writerow(header)
    return f


def real_main(csvlog_fn):
    split = {}
    try:
        with open(csvlog_fn, 'r') as csvlog:
            csvlog_reader = csv.reader(csvlog)
            first = True
            for row in csvlog_reader:
                if first:
                    first = False
                    if row[2] != 'userId':
                        eprint('Error, the third column is not "userId", are you sure this is a log?')
                        return 1
                    header = row
                else:
                    f = get_file(split, csvlog_fn, header, row[2])
                    csv.writer(f).writerow(row)
    finally:
        for _, f in split.items():
            f.close()


def main(argv=None):
    """ Program starting point, it can started by the OS or as normal function

        If it's a normal function argv won't be None if started by the OS
        argv is initialized by the command line arguments
    """
    if argv is None:
        argv = sys.argv

    try:
        csvlog = argv[1]
    except:
        eprint('Usage: prg log_name')
        return 1

    return real_main(csvlog)


if __name__ == "__main__":
    sys.exit(main())

