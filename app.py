import json
from urllib.parse import parse_qs

from flask import Flask, jsonify, request
from pprint import pprint

from tools import *
from extensions import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/rotation_bot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

tm = TaskManager()

lists = dict()

new_list_help = """Here's an example: `/newq nums [1,2,3,4,5]`"""
next_help = """Example usage: `/nextnq nums` \n (This command will pop the first item off the list called `nums`)"""

class InputError(Exception):
    pass

class ArgumentError(Exception):
    pass

def pattern_match_list(string):
    if string[0] != "[" or string[-1] !=  "]":
        raise InputError(f"{string} do not have proper enclosing brackets.")

    return string[1:-1]


def parse_args(args):

    arg1 = None
    arg2 = None
    i = 0

    while i < len(args):
        char = args[i]
        if char == "[":
            arg1 = args[:i]
            arg2 = args[i:]
            break
        else:
            i += 1

    if arg1 is None or arg2 is None:
        raise ArgumentError(next_help)

    # Remove possible space in both sides
    arg1 = arg1.strip()
    arg2 = arg2.strip()

    # Clean list of elements
    result = ""
    group_flag = False
    i, j = 0, 0

    while j < len(arg2) - 1:
        if arg2[j] == '(':
            group_flag = True
            i = j

        if arg2[j] == ')':
            group_flag = False
            elem = arg2[i:j+1]
            elem = elem.strip()
            print(elem)
            result += elem

            i = j


        if arg2[j] == ',' and group_flag is False:
            elem = arg2[i+1:j]
            elem = elem.strip()
            print(elem)
            result += elem + ","
            i = j
        j += 1
    return arg1, result[:-1]


@app.route("/createTask", methods=["POST"])
def createTask():
    payload = parse_qs(request.get_data().decode("utf-8"))
    # pprint(payload)

    text = payload.get("text")

    task_name, task_items = parse_args(text[0])

    message, data = "", ":smile:"
    if text:
        args = text[0]
        try:
            task_name, task_items = parse_args(args)
        except ValueError as err:
            # Not enough args passed (listname, listitem)
            message = f"Hmm, that didn't work. {new_list_help}"
        except InputError as err:
            # The input does not match the pattern
            message = f"{err}"
        except ArgumentError as err:
            message = f"{err}"
        else:
            data = {'team_code': payload.get("team_id"),
                    'name': task_name,
                    'items': task_items}
            rslt = tm.createTask(data)
            message = rslt['message']
    else:
        message = f"Got 0 arguments. {new_list_help}"

    rv = {
        "response_type": "in_channel",
        "replace_original": True,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "text": message,
                    "type": "mrkdwn"
                }
            }
        ]
    }


    print(rv)
    return jsonify(rv)


@app.route("/popitem", methods=["POST"])
def popitem():
    payload = parse_qs(request.get_data().decode("utf-8"))
    pprint(payload)
    raw_args = payload.get("text")

    try:
        list_name = raw_args[0]
    except TypeError:
        # When passed nothing as args
        message = f"`list_name` is a required parameter. {next_help}"
    else:
        try:
            found_list = lists[list_name]
        except KeyError:
            message = f"No such list named `{list_name}` found."

            available_lists = lists.keys()
            if len(available_lists) == 0:
                message += f" Create a list first. {new_list_help}"

            # The following should be admin function
            #else:
            #    available_lists = "".join(list(available_lists))
            #    message += f"These are the current lists for your workspace. {available_lists}"
            # print(type(available_lists), len(available_lists))
        else:
            popped = found_list.pop(0)
            found_list.append(popped)
            message = f"next off `{list_name}` is @{popped}"

    rv = {
        "response_type": "in_channel",
        "text": message
    }


    return jsonify(rv)

@app.route("/test", methods=["GET"])
def test():
    # data = {'team_code': 'T017N93ULR0',
    #         'name': 'peer_review',
    #         'items': 'ali, shaown, jon, mike'}
    #
    # tm = TaskManager()
    #
    # rslt = tm.createTask(data)
    # rslt = tm.popItem('T017N93ULR0', 'peer_review')
    # rslt = tm.deleteTask('T017N93ULR0', 'peer_review')
    # rslt = tm.getTask('T017N93ULR0', 'peer_review')


    data = "   test   [(1,2),3,4,5,6]   "

    parse_args(data)
    #
    # print(rslt)
    return data

if __name__ == "__main__":
    app.run(port=4390)
