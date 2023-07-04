from flask import Blueprint

bp = Blueprint("general", __name__)

from ssnl.general import routes
