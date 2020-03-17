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
        eprint('Open commenting in note',  self.current_time_stamp, 'note id:', ocin_id.group(1))
        self.features.append( ('Open commenting in note', self.current_time_stamp, ocin_id.group(1)) )
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


    def add_rename_stage_feature(self, rename_stage):
        eprint('Rename Stage', self.current_time_stamp, 'Stage id:', rename_stage.group(1), 'Stage name:', rename_stage.group(2))
        self.features.append( ('Rename Stage', self.current_time_stamp, rename_stage.group(1), rename_stage.group(2) ) )

    def add_create_stage_feature(self, create_stage):
        eprint('Create Stage', self.current_time_stamp, 'Name:', create_stage.group(1))
        self.features.append( ('Create Stage', self.current_time_stamp, create_stage.group(1)) )


    def add_delete_note_feature(self, delete_note):
        eprint('Delete Note', self.current_time_stamp, 'Note id:', delete_note.group(1))
        self.features.append( ('Delete Note', self.current_time_stamp, delete_note.group(1)) )


    def add_edit_note_feature(self, edit_node):
        eprint('Edit Note', self.current_time_stamp, 'Note id:', edit_node.group(1), 'Nemo text:', edit_node.group(2) )
        self.features.append( ('Edit Note', self.current_time_stamp, edit_node.group(1), edit_node.group(2)) )


    def add_open_smileys_feature(self, open_smiley):
        eprint("Open Smileys in comments", self.current_time_stamp, 'Icon:', open_smiley.group(1))
        self.features.append( ("Open Smileys in comments", self.current_time_stamp, open_smiley.group(1)) )


    def add_tag_create_feature(self, tag_create):
        eprint("Create new tag", self.current_time_stamp, 'Name:', tag_create.group(1))
        pass


    def add_change_tag_color_feature(self, change_tag_color):
        eprint('Change Tag Color', self.current_time_stamp, 'Note tag:', change_tag_color.group(1), 'Color:', change_tag_color.group(2))
        pass


    def add_change_note_feature(self, change_note):
        eprint("Change Note", self.current_time_stamp, 'Node id:', change_note.group(1), 'Color:', change_note.group(2))
        pass


    def add_add_tag_feature(self, add_tag):
        eprint('Add Tag', 'Tag id:', add_tag.group(1), 'Tag ids:', add_tag.group(2))
        pass


    def add_chat_with_other_user_feature(self, chat_with_other_user):
        eprint("Chat with other users", self.current_time_stamp, "Channel id:",chat_with_other_user.group(1), "Body:",chat_with_other_user.group(2))
        pass


def has_note_dot_stage(state):
    line = state.lines[-1]
    delete_state_id = has_note_dot_stage.delete_state_id_re.search(line)
    if delete_state_id:
        state.delete_state_id = delete_state_id.group(1)
        return
    rename_stage = has_note_dot_stage.rename_stage_re.search(line)
    if rename_stage:
        state.add_rename_stage_feature(rename_stage)
        return
    create_stage = has_note_dot_stage.create_stage_re.search(line)
    if create_stage:
        state.add_create_stage_feature(create_stage)
        return

has_note_dot_stage.delete_state_id_re = re.compile(r'note\.stage\((\d+),\)\.unlink\(\)')
has_note_dot_stage.rename_stage_re = re.compile(r"note\.stage\((\d+),\)\.write\(\{'name': '([^']*)'\}\)")
has_note_dot_stage.create_stage_re = re.compile(r"note\.stage\(\)\.name_create\('([^']*)'\)")



def has_note_and_something_else(state):
    pass


def has_note_dot_note_write(state):
    stc = has_note_dot_note_write
    line = state.lines[-1]
    dnd_node_id = stc.dnd_note_re.search(line)
    if dnd_node_id:
        state.add_move_note_feature(dnd_node_id)
        return

    edit_note = stc.edit_note_re.search(line)
    if edit_note:
        state.add_edit_note_feature(edit_note)
        return

    change_note = stc.change_note_re.search(line)
    if change_note:
        state.add_change_note_feature(change_note)
        return

    add_tag = stc.add_tag_re.search(line)
    if add_tag:
        state.add_add_tag_feature(add_tag)
        return

has_note_dot_note_write.dnd_note_re = re.compile(r"note\.note\((\d+),\).write\(\{u'stage_id': *(\d+)\}\)")
has_note_dot_note_write.edit_note_re = re.compile(r"note\.note\((\d+)\,\)\.write\({'memo': '([^']*)'}\)")
has_note_dot_note_write.change_note_re = re.compile(r"note\.note\((\d+),\)\.write\({'color': (\d+)}\)")
has_note_dot_note_write.add_tag_re = re.compile(r"note\.note\((\d*)\,\)\.write\({'tag_ids': (\[[^}]*)}\)")


def has_note_dot_note(state):
    stc = has_note_dot_note
    line = state.lines[-1]
    if 'write' in line:
        return has_note_dot_note_write

    ocin_id = stc.open_commenting_in_note_re.search(line)
    if ocin_id:
        state.add_opening_commenting_note_feature(ocin_id)
        return

    delete_note = stc.delete_note_re.search(line)
    if delete_note:
        state.add_delete_note_feature(delete_note)
        return

has_note_dot_note.open_commenting_in_note_re = re.compile(r'note\.note\((\d+),\).message_get_suggested_recipients\(\)')
has_note_dot_note.delete_note_re = re.compile(r'note\.note\((\d+),\)\.unlink\(\)')




def has_note_dot_tag(state):
    line = state.lines[-1]
    tag_create = has_note_dot_tag.tag_create_re.search(line)
    if tag_create:
        state.add_tag_create_feature(tag_create)
        return
    change_tag_color = has_note_dot_tag.change_tag_color_re.search(line)
    if change_tag_color:
        state.add_change_tag_color_feature(change_tag_color)
        return

has_note_dot_tag.tag_create_re = re.compile(r"note\.tag\(\)\.create\({'name': '([^']*)'}\)")
has_note_dot_tag.change_tag_color_re = re.compile(r"note\.tag\((\d+)\,\)\.write\({'color': (\d+)}\)")
# "Change Tag Color": 



def has_note(state):
    line = state.lines[-1]
    if 'note.stage' in line:
        return has_note_dot_stage
    if 'note.note' in line:
        return has_note_dot_note
    if 'note.tag' in line:
        return has_note_dot_tag
    return has_note_and_something_else



def no_note(state):
    line = state.lines[-1]
    if 'odoo.models.unlink' in line:
        delete_state_user = no_note.delete_state_user_re.search(line)
        if delete_state_user:
            state.delete_state_user = delete_state_user.group(1)
        if state.delete_state_user and state.delete_state_id:
            state.add_delete_stage_feature()
        return
    open_smiley = no_note.open_smiley_re.search(line)
    if open_smiley:
        state.add_open_smileys_feature(open_smiley)

no_note.delete_state_user_re = re.compile(r'odoo\.models\.unlink: User #(\d+) deleted')
no_note.open_smiley_re = re.compile(r"/mail/static/src/img/smiley/([ \w]*)\.png HTTP/1\.1")


def has_mail_dot_channel(state):
    stc = has_mail_dot_channel
    line = state.lines[-1]
    chat_with_other_user = stc.chat_with_other_user_re.search(line)
    if chat_with_other_user:
        state.add_chat_with_other_user_feature(chat_with_other_user)
        return

has_mail_dot_channel.chat_with_other_user_re = re.compile(r"mail\.channel\((\d+),\).message_post\(attachment_ids=\[\], body='([^']*)', content_subtype='html', message_type='comment', partner_ids=\[\], subtype='mail.mt_comment'\)")


def has_mail(state):
    line = state.lines[-1]
    if '.channel' in line:
        return has_mail_dot_channel


def line_contains_note(state):
    line = state.lines[-1]
    if 'note.' in line:
        return has_note
    if 'mail.' in line:
        return has_mail
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

