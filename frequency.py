#!/usr/bin/env python3

import os
import pprint
import sys
import log_utils
from datetime import timedelta


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)



class EmptyLog(Exception):
    pass


def _get_first_window(actions, time_window):
    endtime = None
    starttime = None
    end_idx = 0
    freqs = {}

    timestamp = 0
    actionidx = 1
    username = 2

    for action in actions:
        if endtime == None:
            starttime = action[timestamp]
            endtime = starttime + time_window

        if action[timestamp] >= endtime:
            break

        v = freqs.get( (action[username], action[actionidx]), 0 )
        freqs[ (action[username], action[actionidx]) ] = v + 1
        end_idx += 1

    if endtime == None:
        raise EmptyLog

    return ( [starttime, freqs], endtime, end_idx )



def _user_action(actions, idx):
    action = 1
    username = 2
    return ( actions[idx][username], actions[idx][action] )



def rotate_on_actions(actions, time_window):
    start_idx = 0
    freq, endtime, end_idx = _get_first_window(actions, time_window)

    starttime = 0
    timestamp = 0
    nr_times = 1

    while True:
        freq[nr_times][ _user_action(actions, start_idx) ] -= 1
        if freq[nr_times][ _user_action(actions, start_idx) ] == 0:
            del freq[nr_times][ _user_action(actions, start_idx) ]

        start_idx += 1
        if start_idx == len(actions):
            break

        freq[starttime] = actions[start_idx][timestamp]
        endtime = actions[start_idx][timestamp] + time_window

        while end_idx < len(actions)  and  actions[end_idx][timestamp] < endtime:
            v = freq[nr_times].get( _user_action(actions, end_idx), 0 )
            freq[nr_times][ _user_action(actions, end_idx ) ] = v + 1
            end_idx += 1

        yield freq



def real_main(csvlog_fn, jsonnumber_fn, time_window, output_fn):
    pp = pprint.PrettyPrinter(indent=4).pprint
    name2id = log_utils.load_name2id(jsonnumber_fn)
    actions = log_utils.read_actions(csvlog_fn,
        {
            0 : log_utils.timestap2date_tsfr,
            1 : log_utils.name2id_tsfr(name2id),
        },
        (0,1,2) )

    for f in rotate_on_actions(actions, time_window):
        pp(f)



def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    try:
        csvlog = argv[1]
        jsonnumber = argv[2]
        time_window = timedelta(minutes=float(argv[3]))
        output = argv[4]
    except:
        eprint('Usage:', prgname, 'cvs_log json_numbers time_window output')
        eprint('\nThe time_window is in minutes\n')
        return 1

    try:
        return real_main(csvlog, jsonnumber, time_window, output)
    except log_utils.NotLog:
        eprint('Error, the second column is not "actionName", are you sure this is a log?')
        return 2
    except EmptyLog:
        eprint('Cannot make any time window from an empty log!')
        return 3

if __name__ == "__main__":
    sys.exit(main())
