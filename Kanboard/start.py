#!/usr/bin/env python3

# Set up and start a http server on port 5000 that receives
# POST webhooks from kanboard on /hook

# e.g. 127.0.0.1:5000/hook


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
    'id', # actually taskId
    'stageId',
    'partnerId',
    'text',
    'title',
    'positionId',
    'swimlaneId'
))


def call_if(name):
    def call_if_impl(f):
        login.dispatch[name] = f
        return f
    return call_if_impl


def get_task_data(json):
    task = json['event_data']['task']
    return {
        'title': task['title'],
        'text': task['description'],
        'userId': task['creator_id'],
        'stageId': task['column_id'],
        'id': json['event_data']['task_id'],
        'swimlaneId': task['swimlane_id'],
    }



@call_if('task.create')
def task_create(csvw, json):
    csvw.write({
        'actionName': 'Create Note',
        **get_task_data(json),
    })



@call_if('task.move.column')
def task_move_column(csvw, json):
    csvw.write({
        'actionName': "Move Note Column",
        'positionId': json['event_data']['position'],
        **get_task_data(json),
    })



@call_if('task.update')
def task_update(csvw, json):
    csvw.write({
        'actionName': "Edit Note",
        **get_task_data(json),
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



@call_if('comment.update')
def comment_update(csvw, json):
    comment = json['event_data']['comment']
    csvw.write({
        'actionName': "Comment Edit",
        'userId': comment['user_id'],
        'stageId': json['event_data']['task']['column_id'],
        'id': comment['task_id'],
        'text': comment['comment'],
    })



@call_if('comment.delete')
def comment_delete(csvw, json):
    comment = json['event_data']['comment']
    csvw.write({
        'actionName': "Comment Delete",
        'userId': comment['user_id'],
        'stageId': json['event_data']['task']['column_id'],
        'id': comment['task_id'],
        'text': comment['comment'],
    })



@call_if('task.file.create')
def file_create(csvw, json):
    file_data = json['event_data']['file']
    csvw.write({
        'actionName': "Attach File",
        'userId': file_data['user_id'],
        'stageId': json['event_data']['task']['column_id'],
        'id': file_data['task_id'],
        'text': file_data['name'],
    })


@call_if('task.move.position')
def task_move_column(csvw, json):
    csvw.write({
        'actionName': "Move Note Position",
        'positionId': json['event_data']['position'],
        **get_task_data(json),
    })


@call_if('task.move.swimlane')
def task_move_swimlane(csvw, json):
    csvw.write({
        'actionName': "Move Note Swimlane",
        'positionId': json['event_data']['position'],
        **get_task_data(json),
    })


@call_if('task.close')
def task_close(csvw, json):
    csvw.write({
        'actionName': "Close Note",
        **get_task_data(json),
    })


@call_if('task.open')
def task_close(csvw, json):
    csvw.write({
        'actionName': "Open Note",
        **get_task_data(json),
    })


@call_if('task.assignee_change')
def task_assignee_change(csvw, json):
    csvw.write({
        'actionName': "Note Change Assignee",
        **get_task_data(json),
    })


@call_if('subtask.create')
def subtask_create(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'title': task['title'],
        'text': task['description'],
        'userId': task['creator_id'],
        'stageId': task['column_id'],
        'swimlaneId': task['swimlane_id'],
        'title': json['event_data']['subtask']['title'],
        'positionId': json['event_data']['subtask']['position'],
        'actionName': 'Subtask Create'
    })


@call_if('subtask.update')
def subtask_update(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'title': task['title'],
        'text': task['description'],
        'userId': task['creator_id'],
        'stageId': task['column_id'],
        'title': json['event_data']['subtask']['title'],
        'positionId': json['event_data']['subtask']['position'],
        'actionName': 'Subtask Update',
    })


@call_if('subtask.delete')
def subtask_delete(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'title': task['title'],
        'text': task['description'],
        'userId': task['creator_id'],
        'stageId': task['column_id'],
        'title': json['event_data']['subtask']['title'],
        'positionId': json['event_data']['subtask']['position'],
        'actionName': 'Subtask Delete',
    })


@call_if('task_internal_link.create_update')
def task_internal_link_create_update(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'actionName': 'Create Internal Link',
        'partnerId': json['event_data']['task_link']['opposite_task_id'],
        'title': task['title'],
        'text': task['description'],
        'userId': task['creator_id'],
        'stageId': task['column_id'],
        'id': json['event_data']['task_link']['id'],
    })


@call_if('task_internal_link.delete')
def task_internal_link_delete(csvw, json):
    task = json['event_data']['task']
    csvw.write({
        'actionName': 'Delete Internal Link',
        'partnerId': json['event_data']['task_link']['opposite_task_id'],
        'title': task['title'],
        'text': task['description'],
        'userId': task['creator_id'],
        'stageId': task['column_id'],
        'id': json['event_data']['task_link']['id'],
    })



@call_if('task.move.project')
def task_move_project(csvw, json):
    csvw.write({
        'actionName': 'Move Note Project',
        **get_task_data(json),
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
