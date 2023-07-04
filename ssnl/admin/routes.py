### LAB MANAGER / ADMIN ROUTES ###
from flask import render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from ssnl.admin import bp

##########

auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return password == "test"


#####

methods = ["GET", "POST"]


@bp.route("/", methods=methods)
def index():
    error = None
    return render_template("admin/login.html", error=error)


@bp.route("/landed", methods=methods)
@auth.login_required
def landing():
    return render_template("admin/landing.html", manager_name=None)


@bp.route("/view_members", methods=methods)
@auth.login_required
def view_members():
    member_data = None
    return render_template("admin/members.html", data=member_data)


@bp.route("/view_projects", methods=methods)
@auth.login_required
def view_projects():
    member_data = None
    return render_template("admin/members.html", data=member_data)


@bp.route("/update_members", methods=methods)
@auth.login_required
def update_members():
    member_data = None
    return render_template("admin/members.html", data=member_data)


@bp.route("/update_projects", methods=methods)
@auth.login_required
def update_projects():
    member_data = None
    return render_template("admin/members.html", data=member_data)


@bp.route("/add_member", methods=methods)
@auth.login_required
def add_member():
    member_data = None
    return render_template("admin/members.html", data=member_data)


@bp.route("/add_project", methods=methods)
@auth.login_required
def add_project():
    member_data = None
    return render_template("admin/members.html", data=member_data)
