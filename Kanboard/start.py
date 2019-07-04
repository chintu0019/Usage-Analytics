#!/usr/bin/env python3

import sys
import csv
import pprint

from flask import request, Flask
import csv_writer as cw

cw.CsvWriter("./results", (
    'timestamp',
    'actionName',
    'userId',
    'ipAddr',
    'id',
    'stageId',
    'partnerId',
    'text',
))


def pp(v):
    pp.f(v)
pp.f = pprint.PrettyPrinter(indent=2, stream=sys.stderr).pprint


def eprint(*args, **kwargs):
    """ Just like the print function, but on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def just_print(json):
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
        f(json)

        return ""
login.dispatch = {}


def call_if(name):
    def call_if_impl(f):
        login.dispatch[name] = f
        return f
    return call_if_impl








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
