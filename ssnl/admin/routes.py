### LAB MANAGER / ADMIN ROUTES ###
from flask import render_template, redirect, url_for, request
from flask_httpauth import HTTPBasicAuth
from ssnl.admin import bp
from config import SSNLConfig
from ssnl.common.utils import (
    get_members,
    get_projects,
    get_reocurring_projects,
    update_local_json,
)

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
    endpoint_map = {
        "View Members": "admin.view_members",
        "View Finance Sources": "admin.view_projects",
        "View Recurring Projects": "admin.view_recurring",
        "Update Members": "admin.update_members",
        "Update Finance Sources": "admin.update_projects",
        "Update Recurring Projects": "admin.update_recurring",
        "Add Member": "admin.add_member",
        "Add Finance Source": "admin.add_project",
        "Add Recurring Projects": "admin.add_recurring",
    }

    if request.method == "POST":
        endpoint = request.form["endpoint"]
        return redirect(url_for(endpoint=endpoint))

    return render_template(
        "admin/landing.html", manager_name=None, endpoint_map=endpoint_map
    )


@bp.route("/view_members", methods=methods)
@auth.login_required
def view_members():
    member_data = None
    return render_template("admin/member__view.html", data=member_data)


@bp.route("/view_projects", methods=methods)
@auth.login_required
def view_projects():
    member_data = None
    return render_template("admin/project__view.html", data=member_data)


@bp.route("/update_members", methods=methods)
@auth.login_required
def update_members():
    lab_members = [x for x in get_members()]

    if request.method == "POST":
        member = request.form["lab_member"]
        employee_number = request.form["employee_number"]
        title = request.form["title"]

        update_local_json(
            path_to_json=SSNLConfig.MEMBER_PATH,
            key=member,
            config={"employee_number": employee_number, "title": title},
        )

    return render_template("admin/member__update.html", lab_members=lab_members)


@bp.route("/update_projects", methods=methods)
@auth.login_required
def update_projects():
    member_data = None
    return render_template("admin/project__update.html", data=member_data)


@bp.route("/add_member", methods=methods)
@auth.login_required
def add_member():
    member_data = None
    return render_template("admin/member__add.html", data=member_data)


@bp.route("/add_project", methods=methods)
@auth.login_required
def add_project():
    member_data = None
    return render_template("admin/project__add.html", data=member_data)
