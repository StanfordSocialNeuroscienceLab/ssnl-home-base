#!/bin/python3
import json
import requests
import sys
from flask import flash


##########


def post_webhook(message: str):
    """
    This is a wrapper to send error data to the `ssnl-app-errors` slack channel
    """

    flash("Sorry, something went wrong! Ian's on it")

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
