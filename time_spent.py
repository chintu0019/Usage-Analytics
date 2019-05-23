#!/usr/bin/env python3

import sys
import os

import pprint
import log_utils
import datetime
from copy import deepcopy


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)



def _user_action(actn):
    return (actn[2], actn[1])



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
    pp = pprint.PrettyPrinter(indent=4).pprint
    results = {} # results associates a user,action pair to its time delta
    windows = {} # window associates a user,action pair to its starting time point

    #readable indexes
    userw = 0
    usera = 2
    action = 1
    timestamp = 0

    for actn in actions:
        if not is_in_group(_user_action(actn), windows):
            # open the window
            windows[ ( find_group(actn[usera], groups), actn[action] ) ] = actn[timestamp]
            if not is_in_group(_user_action(actn), results):
                results[ ( find_group(actn[usera], groups), actn[action] ) ] = datetime.timedelta(0)


        # it is probably not a good idea modify the variable windows while iterating over it
        nwindows = deepcopy(windows)
        for win in windows:
            if actn[usera] not in win[userw]:
                continue

            # in the user group
            group = find_group(actn[usera], groups)
            if win[action] == actn[action]:
                # just add the time
                results[win] += actn[timestamp] - nwindows[win]
                nwindows[win] = actn[timestamp]

            elif win[action] != actn[action]:
                # add up and close the window
                results[win] += actn[timestamp] - nwindows[win]
                del nwindows[win]
        windows = nwindows

    return results



def real_main(csvlog_fn, jsonnumber_fn, user_groups):
    pp = pprint.PrettyPrinter(indent=4).pprint

    name2id = log_utils.load_name2id(jsonnumber_fn)
    actions = log_utils.read_actions(csvlog_fn,
        {
            0 : log_utils.timestap2date_tsfr,
            1 : log_utils.name2id_tsfr(name2id),
        },
        (0,1,2)
    )
    results = compute_timings(actions, user_groups)
    pp( results )



def main(argv=None):
    prgname = os.path.basename(__file__) if '__file__' in globals() else 'prg'
    if argv is None:
        argv = sys.argv

    try:
        csvlog = argv[1]
        jsonnumber = argv[2]
        groups = []
        if len(argv) > 3:
            for g in [x.strip() for x in argv[3].split('-')]:
                groups.append( tuple(x.strip() for x in g.split(',')) )
    except:
        eprint('Usage:', prgname, 'csvlog jsonnumber users_groups')
        eprint('"user_groups" is a dash-separated list of groups')
        eprint('each group is a comma separed list of user ids\n')
        eprint('Example: 1,4,3-7,2 to group 1, 3, and 4 in one group, and 7 and 2 in another.')
        eprint('         Users id outside any group are counted separately')
        return 1

    try:
        return real_main(csvlog, jsonnumber, groups)
    except log_utils.NotLog:
        eprint('Error, the second column is not "actionName", are you sure this is a log?')
        return 2


if __name__ == "__main__":
    sys.exit(main())

