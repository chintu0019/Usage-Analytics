#!/usr/bin/env python3

import sys
import csv
import pprint

from flask import request, Flask
import csv_writer as cw


def pp(v):
    pp.f(v)
pp.f = pprint.PrettyPrinter(indent=2, stream=sys.stderr).pprint


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def just_print(_csvwriter, json):
    eprint("Event", json['event_name'], "is uncovered")
    eprint("===============")
    pp(json)
    eprint("===============")


app = Flask(__name__)

@app.route('/hook', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        eprint("GET", str(request))
        return "Working!"

    elif request.method == 'POST':
        json = request.get_json()
        f = login.dispatch.get(json['event_name'], just_print)
        f(login.csvwriter, json)
        return ""

login.dispatch = {}
login.csvwriter = cw.CsvWriter("./results", (
    'timestamp',
    'actionName',
    'userId',
    'ipAddr',
    'id',
    'stageId',
    'partnerId',
    'text',
    'title',
))


def call_if(name):
    def call_if_impl(f):
        login.dispatch[name] = f
        return f
    return call_if_impl

# comment.update
# comment.delete
# file.create
# task.move.project
# task.move.position
# task.move.swimlane
# task.close
# task.open
# task.assignee_change
# subtask.update
# subtask.create
# subtask.delete
# task_internal_link.create_update
# task_internal_link.delete


@call_if('task.create')
def task_create(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'actionName': 'Create Note',
        'userId': task['creator_id'],
        'title': task['title'],
        'text': task['description'],
        'stageId': task['column_id'],
        'id': json['event_data']['task_id'],
    })



@call_if('task.move.column')
def task_move_column(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'actionName': "Move Note",
        'userId': task['creator_id'],
        'title': task['title'],
        'text': task['description'],
        'stageId': json['event_data']['dst_column_id'],
    })



@call_if('task.update')
def task_update(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'actionName': "Edit Note",
        'stageId': task['column_id'],
        'userId': task['creator_id'],
        'title': task['title'],
        'text': task['description'],
    })



@call_if('comment.create')
def comment_create(csvw, json):
    comment = json['event_data']['comment']
    csvw.write({
        'actionName': "Comment in Note",
        'userId': comment['user_id'],
        'stageId': json['event_data']['task']['column_id'],
        'id': comment['task_id'],
        'text': comment['comment'],
    })



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
