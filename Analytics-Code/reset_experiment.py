#!/usr/bin/env python3

# Author - Manoj Kesavulu

import os
import sys


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def realMain(odoo_version):
    if odoo_version == '10':
        os.chdir("../Odoo10/")
        os.system('docker run -it --rm -v odoo10_odoo-db-data-odoo10:/volume -v "`greadlink -e .`":/backup alpine sh -c "find /volume -mindepth 1 -delete ; tar -C /volume/ -xvjf /backup/odoo10_experiment_initialize.tar.bz2"')
    elif odoo_version =='11':
        os.chdir("../Odoo11/")
        os.system('docker run -it --rm -v odoo11_odoo-db-data-odoo11:/volume -v "`greadlink -e .`":/backup alpine sh -c "find /volume -mindepth 1 -delete ; tar -C /volume/ -xvjf /backup/odoo11_experiment_initialize.tar.bz2"')


def main (argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    try:
        odoo_version = argv[1]
        realMain(odoo_version)
    except:
        eprint('\nEnter the Version of the Odoo (10 or 11)')
        eprint('\nProgram to reset the experiment \n')
        eprint('Usage: python reset_experiment.py odoo_version')
        eprint('Example: python reset_experiment.py 10 \n')


if __name__ == "__main__":
    sys.exit(main())