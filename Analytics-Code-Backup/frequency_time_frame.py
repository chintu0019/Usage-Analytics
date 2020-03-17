#!/usr/bin/env python3

import utils
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

    for action in actions:
        if endtime == None:
            starttime = action['timestamp']
            endtime = starttime + time_window

        if action['timestamp'] >= endtime:
            break

        v = freqs.get( (action['user'], action['action']), 0 )
        freqs[ (action['user'], action['action']) ] = v + 1
        end_idx += 1

    if endtime == None:
        raise EmptyLog

    return ( { 'starttime': starttime, 'freqs': freqs}, endtime, end_idx )



def _user_action(actions, idx):
    return ( actions[idx]['user'], actions[idx]['action'] )



def rotate_on_actions(actions, time_window):
    start_idx = 0
    freq, endtime, end_idx = _get_first_window(actions, time_window)

    yield freq

    while True:
        freq['freqs'][ _user_action(actions, start_idx) ] -= 1
        if freq['freqs'][ _user_action(actions, start_idx) ] == 0:
            del freq['freqs'][ _user_action(actions, start_idx) ]

        start_idx += 1
        if start_idx == len(actions):
            break

        freq['starttime'] = actions[start_idx]['timestamp']
        endtime = actions[start_idx]['timestamp'] + time_window

        while end_idx < len(actions)  and  actions[end_idx]['timestamp'] < endtime:
            v = freq['freqs'].get( _user_action(actions, end_idx), 0 )
            freq['freqs'][ _user_action(actions, end_idx ) ] = v + 1
            end_idx += 1

        yield freq



class Real_main_opt(utils.Frozen):
    def __init__(self):
        self.csvlog_fn = None
        self.jsonnumber_fn= None
        self.time_window_length = None

        self.log_begin = None
        self.log_end = None

        self.frozen = True



def real_main(opt):
    pp = pprint.PrettyPrinter(indent=4).pprint
    name2id = log_utils.load_name2id(opt.jsonnumber_fn)

    raopt = log_utils.Read_action_opt()
    raopt.csvlog_fn = opt.csvlog_fn
    raopt.transformators = {
        0 : log_utils.timestap2date_tsfr,
        1 : log_utils.name2id_tsfr(name2id),
    }
    raopt.col_names = {
        0 : 'timestamp',
        1 : 'action',
        2 : 'user',
    }
    raopt.filter = log_utils.in_date_range(opt.log_begin, opt.log_end, 'timestamp')

    actions = log_utils.read_actions_ex(raopt)

    for f in rotate_on_actions(actions, opt.time_window_length):
        pp(f)



def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    opt = Real_main_opt()
    try:
        opt.csvlog_fn = argv[1]
        opt.jsonnumber_fn = argv[2]
        opt.time_window_length = timedelta(minutes=float(argv[3]))
    except:
        eprint('Output how many times an actions happens in a time window')
        eprint('')
        eprint('Usage:', prgname, 'cvs_log json_numbers time_window')
        eprint('\nThe time_window is in minutes\n')
        return 1

    try:
        return real_main(opt)
    except log_utils.NotLog:
        eprint('Error, the second column is not "actionName", are you sure this is a log?')
        return 2
    except EmptyLog:
        eprint('Cannot make any time window from an empty log!')
        return 3

if __name__ == "__main__":
    sys.exit(main())

