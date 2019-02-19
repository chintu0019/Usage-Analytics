#!/usr/bin/env python3
import sys
import argparse
import re

from collections import deque


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class State:
    def __init__(self, nr_lines):
        self.nr_lines = nr_lines
        self.lines = deque()
        self.features = []
        self.current_time_stamp = None
        self.delete_state_id = None
        self.delete_state_user = None
        self.move_note_prev_line_re = re.compile(r'note\.stage\(\d+,\)\.name_get\(\)')


    def add_line(self, line):
        self.lines.append(line)
        if len(self.lines) > self.nr_lines:
            self.lines.popleft()

    def feature_precondition(self):
        if not self.current_time_stamp:
            raise RuntimeError('Stage feature with no timestamp')

    def add_delete_stage_feature(self):
        self.feature_precondition()
        if not (self.delete_state_id and self.delete_state_user):
            raise RuntimeError('Trying to add an incomplete delete stage feature')

        self.features.append( ('Delete Stage', self.current_time_stamp, self.delete_state_user, self.delete_state_id) )
        eprint('Adding Delete Stage:', self.current_time_stamp, 'User id:', self.delete_state_user, 'State id:', self.delete_state_id)

        self.current_time_stamp = None
        self.delete_state_id = None
        self.delete_state_user = None


    def add_opening_commenting_note_feature(self, ocin_id):
        self.feature_precondition()
        eprint('Open commenting in note',  self.current_time_stamp, ocin_id.group(1))
        self.features.append( ('Open commenting in note', self.current_time_stamp, 'id:', ocin_id.group(1)) )
        self.current_time_stamp = None


    def add_move_note_feature(self, dnd_note_id):
        self.feature_precondition()
        try:
            prev_line = self.lines[-2]
        except IndexError:
            prev_line = ''

        if self.move_note_prev_line_re.search(prev_line):
            feature_name = 'Move note'
        else:
            feature_name = 'Drag and Drop note'

        eprint(feature_name, self.current_time_stamp, 'Note id:', dnd_note_id.group(1), 'Stage id:', dnd_note_id.group(2))
        self.features.append( (feature_name, self.current_time_stamp, dnd_note_id.group(1), dnd_note_id.group(2) ) )
        self.current_time_stamp = None



def has_note_dot_stage(state):
    line = state.lines[-1]
    delete_state_id = has_note_dot_stage.delete_state_id_re.search(line)
    if delete_state_id:
        state.delete_state_id = delete_state_id.group(1)

has_note_dot_stage.delete_state_id_re = re.compile(r'note\.stage\((\d+),\)\.unlink\(\)')



def has_note_and_something_else(state):
    pass



def has_note_dot_note(state):
    line = state.lines[-1]
    ocin_id = has_note_dot_note.open_commenting_in_note_re.search(line)
    if ocin_id:
        state.add_opening_commenting_note_feature(ocin_id)
        return
    dnd_node_id = has_note_dot_note.dnd_note_re.search(line)
    if dnd_node_id:
        state.add_move_note_feature(dnd_node_id)

has_note_dot_note.open_commenting_in_note_re = re.compile(r'note\.note\((\d+),\).message_get_suggested_recipients\(\)')
has_note_dot_note.dnd_note_re = re.compile(r"note\.note\((\d+),\).write\(\{u'stage_id': *(\d+)\}\)")



def has_note(state):
    line = state.lines[-1]
    if 'note.stage' in line:
        return has_note_dot_stage
    if 'note.note' in line:
        return has_note_dot_note
    return has_note_and_something_else



def no_note(state):
    line = state.lines[-1]
    if 'odoo.models.unlink' in line:
        delete_state_user = no_note.delete_state_user_re.search(line)
        if delete_state_user:
            state.delete_state_user = delete_state_user.group(1)
        if state.delete_state_user and state.delete_state_id:
            state.add_delete_stage_feature()

no_note.delete_state_user_re = re.compile(r'odoo\.models\.unlink: User #(\d+) deleted')



def line_contains_note(state):
    line = state.lines[-1]
    if 'note.' in line:
        return has_note
    return no_note



def extract_time_stamp(state):
    line = state.lines[-1]
    state.current_time_stamp = line[18:41]
    state.lines[-1] = line[42:]
    return line_contains_note



def initial(state):
    line = state.lines[-1]
    if (line.startswith('\x1b[33mweb_1  |\x1b[0m ')):
        return extract_time_stamp
    return None



def examine(state):
    f = initial
    while f:
        f = f(state)



def rmain(args):
    state = State(5)
    with open(args.input) as finput:
        for line in finput:
            state.add_line(line)
            examine(state)



def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input raw log", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output json log", type=str, default='output_log.json')

    args = parser.parse_args(argv[1:])
    rmain(args)

    return 0

if __name__ == "__main__":
    sys.exit(main())

