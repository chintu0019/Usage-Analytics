#!/usr/bin/python

import os
import sys


fd = "abcdef"
fl = "abcdef_123.csv"


def eprint(*args):
    print(*args)


def main(argv=None):
    #eprint(sys.argv)
    if fl.startswith(fd):
        print(fl)


if __name__ == "__main__":
    sys.exit(main())