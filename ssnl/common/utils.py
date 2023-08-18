### COMMON SSNL UTILITIES ###
import json
import os
import logging
import requests
from flask import flash
import sys
import random
import traceback
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


def update_local_json(path_to_json: str, key: str, config: dict):
    """
    Updates local JSON file with responses from a Flask form
    """

    filename = path_to_json.split("/")[-1]

    try:
        logging.info(f"Updating the {key} field in {filename}")

        # Open local JSON file as dictionary
        with open(path_to_json) as incoming:
            packet = json.load(incoming)

        # Isolate key (e.g., "Ian Ferguson")
        temp = packet[key]

        # Loop through config keys
        for k in config.keys():
            if config[k]:
                logging.info(f"Updating {k}...")
                temp[k] = config[k]

        # Reassign to local storage
        packet[key] = temp

        # Write to local storage
        with open(path_to_json, "w") as outgoing:
            json.dump(packet, outgoing, indent=5)

        flash(f"Updated {filename}")

    except Exception as e:
        message = f"Failed to update {filename}\n\n{traceback.format_exc()}"
        post_webhook(message=message)


def write_to_local_json(path_to_json: str, key: str, new_data: dict):
    """
    Adds a new key to a local JSON file
    """

    filename = path_to_json.split("/")[-1]

    try:
        logging.info(f"Adding the {key} key to {path_to_json.split('/')[-1]}")

        with open(path_to_json) as incoming:
            packet = json.load(incoming)

        packet[key] = new_data

        with open(path_to_json, "w") as outgoing:
            json.dump(packet, outgoing, indent=5)

        flash(f"Updated {path_to_json.split('/')[-1]}")

    except Exception as e:
        message = f"Failed to write to {filename}\n\n{traceback.format_exc()}"
        post_webhook(message=message)


def post_webhook(message: str):
    """
    This is a wrapper to send error data to the `ssnl-app-errors` slack channel
    """

    flash("Sorry, something went wrong! Please contact your lab manager")

    #####

    webhook_url = SSNLConfig.SLACK_HOOK
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


def get_members(full: bool = False) -> list:
    """
    Queries members JSON and returns keys
    """

    member_path = SSNLConfig.MEMBER_PATH

    with open(member_path) as incoming:
        temp = json.load(incoming)

    if not full:
        return [x for x in temp.keys()]

    return temp


def get_projects() -> dict:
    """
    Queries projects JSON and returns dictionary
    """

    project_path = SSNLConfig.PROJECT_PATH

    with open(project_path) as incoming:
        temp = json.load(incoming)

    return temp


def get_reocurring_projects() -> dict:
    """
    Queries reocurring JSON and returns dictionary
    """

    project_path = SSNLConfig.REOCURRING_PATH

    with open(project_path) as incoming:
        temp = json.load(incoming)

    return temp
