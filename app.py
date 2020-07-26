import json
from urllib.parse import parse_qs

from flask import Flask, jsonify, request
from pprint import pprint


app = Flask(__name__)

lists = dict()

new_list_help = """Here's an example: `/newlist nums [1,2,3,4,5]`"""
next_help = """Example usage: `/next nums` \n (This command will pop the first item off the list called `nums`)"""

class InputError(Exception):
    pass

class ArgumentError(Exception):
    pass

def pattern_match_list(string):
    if string[0] != "[" or string[-1] !=  "]":
        raise InputError(f"{string} do not have proper enclosing brackets.")

    return string[1:-1]


def parse_args(args):
    # TODO: listname cannot have space in it
    # FIXME: trailing comma fucks up the list

    arg1, arg2 = args.split(" ", 1)
    
    if arg1.startswith("["):
        # Possible case: command arg2 (forgot arg1) 
        raise ArgumentError("Forgot list name")

    arg2 = pattern_match_list(arg2)
    # TODO: delimiter (comma). Check if the comma is not in there
    arg2 = [i for i in arg2.split(",")]

    return arg1, arg2

@app.route("/welcome", methods=["POST"])
def welcome():
    payload = parse_qs(request.get_data().decode("utf-8"))
    text = payload.get("text")

    message, data = "", ":smile:" 
    if text:
        args = text[0]
        try:
            list_name, list_items = parse_args(args)
        except ValueError as err:
            # Not enough args passed (listname, listitem)
            message = f"Hmm, that didn't work. {new_list_help}"
        except InputError as err:
            # The input does not match the pattern
            message = f"{err}" 
        except ArgumentError as err:
            message = f"{err}"
        else:
            action = "Created" if lists.get(list_name, None) is None else "Updated"

            # Add it to the datastorage
            lists[list_name] = list_items
            message = f"{action} a list `{list_name}` with the following items:"
            data = str(list_items)
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
                    "type": "mrkdwn",
                },
       # Add a conditional before returning the second field
              "fields": [
                {
                  "type": "mrkdwn",
                  "text": data 
                }
            ]
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
            message = f"next off `{list_name}` is {popped}"

    rv = {
        "response_type": "in_channel",
        "text": message
    }


    return jsonify(rv)


if __name__ == "__main__":
    app.run(port=8080)