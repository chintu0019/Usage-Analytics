#!/usr/bin/env python3

import sys
import os
import csv
import glob

participant_list_file = "results/Participants.csv"

def _look_it_up(username):
    with open(participant_list_file, 'r') as pf:
        pfr = csv.reader(pf)
        heading = True
        max_id = 0
        for line in pfr:
            if heading:
                heading = False
                if line[0] != 'userID': raise RuntimeError('Participants file first column is not userID!')
                continue

            line[0] = int(line[0])
            if line[0] > max_id: max_id = line[0]

            if line[1] == username:
                return (line[0], True)

    return (max_id + 1, False)


def _add_it(username, new_id):
    with open(participant_list_file, 'a') as pf:
        pfr = csv.writer(pf)
        pfr.writerow([str(new_id), username])


def get_user_id(username):
    userid, found = _look_it_up(username)
    if not found: _add_it(username, userid)
    return userid



def _userId_idx(header):
    if _userId_idx.v != None: return _userId_idx.v
    for idx, v in enumerate(header):
        if v == 'userId':
            _userId_idx.v = idx
            return _userId_idx.v
    raise RuntimeError('csv file misses the userId field!')
_userId_idx.v = None


def _cat_next_file(csv_file, ocsv_writer, userid, done_header):
    with open(csv_file, 'r') as pf:
        pfr = csv.reader(pf)
        heading = True
        for line in pfr:
            if heading:
                heading = False
                header = line
                continue
            if not done_header:
                done_header = True
                ocsv_writer.writerow(header)
            line[ _userId_idx(header) ] = str(userid)
            ocsv_writer.writerow(line)


def cat_csv_files(username, userid):
    ocsv_filename = 'results/' + username + '/' + username + '_usage_data.csv'
    csv_files = glob.glob('results/' + username + '/*.csv')
    csv_files.sort()

    with open(ocsv_filename, 'w') as ocsv:
        ocsvw = csv.writer(ocsv)
        done_header = False
        for csv_file in csv_files:
            if csv_file == ocsv_filename:
                continue
            _cat_next_file(csv_file, ocsvw, userid, done_header)
            done_header = True



def main(argv=None):
    if argv is None:
        argv = sys.argv

    username = argv[1]

    user_id = get_user_id(username)
    cat_csv_files(username, user_id)

    return 0

if __name__ == "__main__":
    sys.exit(main())
