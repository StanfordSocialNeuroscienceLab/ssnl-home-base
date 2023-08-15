#!/bin/python3
import json
import requests
import sys
from flask import flash


##########


def post_webhook(message: str, hook: str):
    """
    This is a wrapper to send error data to the `ssnl-app-errors` slack channel
    """

    flash("Sorry, something went wrong! Ian's on it")

    #####

    webhook_url = hook
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
