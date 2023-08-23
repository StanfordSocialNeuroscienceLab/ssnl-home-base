### CONFIG CLASS FOR FLASK APP ###
import os
from datetime import datetime
import pytz

config_path = os.path.join(".", ".env")


class SSNLConfig:
    DEVMODE = True

    ROOT = os.path.abspath(os.path.dirname(__file__))
    HERE = os.path.join(ROOT, "ssnl")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SLACK_HOOK = os.environ.get("SLACK_HOOK")
    UPLOAD_FOLDER = "files/uploads"
    JUSTIFICATIONS = "files/justifications"
    BP_TEMPLATES = "files/templates"

    JSON_PATH = os.path.join(HERE, "files/packets")
    MEMBER_PATH = os.path.join(JSON_PATH, "members.json")
    PROJECT_PATH = os.path.join(JSON_PATH, "projects.json")
    REOCURRING_PATH = os.path.join(JSON_PATH, "reocurring.json")
    ADMIN_PATH = os.path.join(JSON_PATH, "admin.json")

    PACIFIC_TIME = datetime.now(pytz.timezone("US/Pacific"))
