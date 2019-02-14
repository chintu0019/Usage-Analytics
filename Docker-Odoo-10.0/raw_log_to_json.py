#!/usr/bin/env python3
import sys
import argparse

from collections import deque


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class State:
    def __init__(self, nr_lines):
        self.nr_lines = nr_lines
        self.lines = deque()
        self.features = []
        self.current_time_stamp = None

    def add_line(self, line):
        self.lines.append(line)
        if len(self.lines) > self.nr_lines:
            self.lines.popleft()

    def add_feature(self):
        pass


def has_note_dot_stage(state):
    pass


def has_note_and_something_else(state):
    pass


def has_note(state):
    line = state.lines[-1]
    if 'note.stage' in line:
        return has_note_dot_stage
    return has_note_and_something_else


def no_note(state):
    print(state.lines[-1])


def line_contains_note(state):
    line = state.lines[-1]
    if 'note.' in line:
        return has_note
    return no_note


def extract_time_stamp(state):
    line = state.lines[-1]
    state.current_time_stamp = line[18:42]
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

