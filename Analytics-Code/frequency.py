#!/usr/bin/env python3

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

    for action in actions:
        if endtime == None:
            starttime = action[0]
            endtime = starttime + time_window

        if action[0] >= endtime:
            break

        v = freqs.get( (action[2], action[1]) , 0 )
        freqs[ (action[2], action[1]) ] = v + 1
        end_idx += 1

    if endtime == None:
        raise EmptyLog

    return ( [starttime, freqs], endtime, end_idx)



def rotate_on_actions(actions, time_window):
    start_idx = 0
    freq, endtime, end_idx = _get_first_window(actions, time_window)

    while True:
        freq[1][ ( actions[start_idx][2], actions[start_idx][1] ) ] -= 1
        if freq[1][ ( actions[start_idx][2], actions[start_idx][1] ) ] == 0:
            del freq[1][ ( actions[start_idx][2], actions[start_idx][1] ) ]

        start_idx += 1
        if start_idx == len(actions):
            break

        freq[0] = actions[start_idx][0]
        endtime = actions[start_idx][0] + time_window

        while end_idx < len(actions)  and  actions[end_idx][0] < endtime:
            v = freq[1].get( (actions[end_idx][2], actions[end_idx][1]), 0 )
            freq[1][ (actions[end_idx][2], actions[end_idx][1]) ] = v + 1
            end_idx += 1

        yield freq



def real_main(csvlog_fn, jsonnumber_fn, time_window, output_fn):
    name2id = log_utils.load_name2id(jsonnumber_fn)
    actions = log_utils.read_actions(csvlog_fn,
        {
            0 : log_utils.timestap2date_tsfr,
            1 : log_utils.name2id_tsfr(name2id),
        },
        (0,1,2) )

    for f in rotate_on_actions(actions, time_window):
        print(f)



def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        csvlog = argv[1]
        jsonnumber = argv[2]
        time_window = timedelta(minutes=float(argv[3]))
        output = argv[4]
    except:
        eprint('Usage: prg cvs_log json_numbers time_window output')
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
