### MAIN APPLICATION CONSTRUCTOR ###
from flask import Flask
from config import SSNLConfig


def create_app(config_class=SSNLConfig):
    """
    Renders main Flask application
    """

    app_ = Flask(__name__)
    app_.config.from_object(config_class)

    ###

    # Main routes
    from ssnl.general import bp as general_routes

    app_.register_blueprint(general_routes)

    # Admin routes
    from ssnl.admin import bp as admin_routes

    app_.register_blueprint(admin_routes, url_prefix="/lab_manager")

    return app_
