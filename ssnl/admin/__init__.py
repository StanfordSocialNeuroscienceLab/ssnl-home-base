from flask import Blueprint

bp = Blueprint("admin", __name__)

from ssnl.admin import routes
