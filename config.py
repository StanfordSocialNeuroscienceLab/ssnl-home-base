### CONFIG CLASS FOR FLASK APP ###
import os
from datetime import datetime
import pytz


class SSNLConfig:
    HERE = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = "jamil4ever"
    UPLOAD_FOLDER = "files/uploads"
    JUSTIFICATIONS = "files/justifications"
    BP_TEMPLATES = "files/templates"

    JSON_PATH = "files/packets"
    MEMBER_PATH = os.path.join(JSON_PATH, "members.json")
    PROJECT_PATH = os.path.join(JSON_PATH, "projects.json")
    ADMIN_PATH = os.path.join(JSON_PATH, "admin.json")

    PACIFIC_TIME = datetime.now(pytz.timezone("US/Pacific"))
