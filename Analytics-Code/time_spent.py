#!/usr/bin/env python3

import sys
import os

import utils
import pprint
import log_utils
import datetime
from copy import deepcopy


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)



def _user_action(actn):
    return (actn['user'], actn['action'])



def is_in_group(user_action, storage):
    for win in storage:
        if user_action[0] in win[0] and user_action[1] == win[1]:
            return True
    return False



def find_group(user_id, groups):
    for g in groups:
        if user_id in g:
            return g
    return ( user_id, )



def compute_timings(actions, groups):
    results = {} # results associates a user,action pair to its time delta
    windows = {} # window associates a user,action pair to its starting time point

    #readable indexes
    user_group = 0
    action = 1

    for actn in actions:
        if not is_in_group(_user_action(actn), windows):
            # open the window
            windows[ ( find_group(actn['user'], groups), actn['action'] ) ] = actn['timestamp']
            if not is_in_group(_user_action(actn), results):
                results[ ( find_group(actn['user'], groups), actn['action'] ) ] = datetime.timedelta(0)

        # it is probably not a good idea modify the variable windows while iterating over it
        nwindows = deepcopy(windows)
        for win in windows:
            if actn['user'] not in win[user_group]:
                continue

            results[win] += actn['timestamp'] - nwindows[win]

            if win[action] == actn['action']:
                nwindows[win] = actn['timestamp']
            else:
                del nwindows[win]

        windows = nwindows

    return results



class Real_main_opt(utils.Frozen):
    def __init__(self):
        self.csvlog_fn = None
        self.jsonnumber_fn= None

        self.log_begin = None
        self.log_end = None

        self.groups = []

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
    results = compute_timings(actions, opt.groups)

    pp( results )



def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    opt = Real_main_opt()
    try:
        opt.csvlog_fn = argv[1]
        opt.jsonnumber_fn = argv[2]
        opt.groups = []
        if len(argv) > 3:
            for g in [x.strip() for x in argv[3].split('-')]:
                opt.groups.append( tuple(x.strip() for x in g.split(',')) )
    except:
        eprint('Adds up how much time the user spent on certain actions')
        eprint('')
        eprint('Usage:', prgname, 'csvlog jsonnumber users_groups')
        eprint('"user_groups" is a dash-separated list of groups')
        eprint('each group is a comma separed list of user ids\n')
        eprint('Example: 1,4,3-7,2 to group 1, 3, and 4 in one group, and 7 and 2 in another.')
        eprint('         Users id outside any group are counted separately')
        return 1

    try:
        return real_main(opt)
    except log_utils.NotLog:
        eprint('Error, the second column is not "actionName", are you sure this is a log?')
        return 2


if __name__ == "__main__":
    sys.exit(main())

