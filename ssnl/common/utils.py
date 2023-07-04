### COMMON SSNL UTILITIES ###
import json
import os
import logging
import requests
from flask import flash
import sys
import random
from config import SSNLConfig

logging.basicConfig(level=logging.INFO)

##########


# Global utils...
def safe_load_json(path: str) -> dict:
    """
    Ensures that a filepath exists before
    attempting to load
    """

    if not os.path.exists(path=path):
        logging.warn("PATH DOES NOT EXIST")
        logging.warn(f"Creating new [path={path}]")

        with open(path, "w+") as temp:
            json.dump(obj={}, fp=temp)

    ###

    with open(path) as temp:
        return json.load(temp)


def post_webhook(message: str):
    """
    This is a wrapper to send error data to the `ssnl-app-errors` slack channel
    """

    flash("Sorry, something went wrong! Please contact your lab manager")

    #####

    webhook_url = "https://hooks.slack.com/services/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"
    title = "New SSNL App Error"

    slack_data = {
        "username": "SSNL IO Error Bot",
        "icon_emoji": ":jzneutral:",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [{"title": title, "value": message, "short": "false"}],
            }
        ],
    }

    byte_length = str(sys.getsizeof(slack_data))
    headers = {"Content-Type": "application/json", "Content-Length": byte_length}
    response = requests.post(webhook_url, data=json.dumps(slack_data), headers=headers)

    return response


def download():
    return None


def drop_a_line(path):
    options = [
        "Have a nice day!",
        "Keep up the great work!",
        "You're doing great!",
        "You are the sun and the moon!",
        "You are absolute magic!",
        "Thank you for being you!",
        "Make today great!",
        "Make it a great day!",
        "Do something nice for yourself today!",
        "You are a light everywhere you go!",
        "You can accomplish anything you set your mind to!",
        "Everyone needs a friend like you!",
    ]

    with open(os.path.join(path, "README.txt"), "w") as file:
        message = random.choice(options)

        file.write("PLEASE READ\n\n")
        file.write(message)


#####


def get_members() -> list:
    """
    Queries members JSON and returns keys
    """

    member_path = SSNLConfig.MEMBER_PATH

    with open(member_path) as incoming:
        temp = json.load(incoming)

    return [x for x in temp.keys()]


def get_projects() -> list:
    """
    Queries projects JSON and returns keys
    """

    project_path = SSNLConfig.PROJECT_PATH

    with open(project_path) as incoming:
        temp = json.load(incoming)

    return [x for x in temp.keys()]
