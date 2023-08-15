#!/bin/python3
from flask import Flask, render_template, send_file, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
import os, pathlib, pytz
from datetime import datetime
import logging
import json
from time import sleep
from uuid import uuid4
from utils.base.slack import post_webhook
from utils.base.helper import *

logger = logging.getLogger(__name__)

##########


app = Flask(__name__)
app.secret_key = "jamil4ever"
here = app.root_path

app.config["UPLOAD_FOLDER"] = "files/uploads"
app.config["JUSTIFICATIONS"] = "files/justifications"
app.config["BP_TEMPLATES"] = "files/templates"

path_to_members = os.path.join(here, "files/packets/members.json")
path_to_projects = os.path.join(here, "files/packets/projects.json")
path_to_reocurring = os.path.join(here, "files/packets/reocurring.json")

pacific_time = datetime.now(pytz.timezone("US/Pacific")).strftime("%m_%d_%Y")
logging.basicConfig(level=logging.INFO)


##########


for path in ["uploads", "justifications"]:
    temp = os.path.join(here, "files", path)

    if not os.path.exists(temp):
        pathlib.Path(temp).mkdir(parents=True, exist_ok=True)


##########


@app.route("/", methods=["GET", "POST"])
def index():
    # Start with a clean cache
    for dir in ["files/uploads", "files/justifications"]:
        try:
            cleanup_output(dir)

        except Exception as e:
            message = f"Error @ cleanup_output\n\n{e}"
            post_webhook(message=message)

    return render_template("index.html")


#####


@app.route("/Justifications", methods=["GET", "POST"])
def bp():
    return render_template("landing.html")


@app.route("/P-Card", methods=["GET", "POST"])
def bp_pcard():
    if request.method == "POST":
        from utils.justifications.pcard import PCard

        try:
            j_short = request.form["purchased_short"]
            j_long = request.form["purchased_long"]
            j_why = request.form["purchased_why"]
            who = request.form["purchased_by"]
            source = request.form["funding_source"]
            amount = request.form["charge_amount"].replace("$", "")
            date_c = request.form["date_charged"]

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        # -- Instantiate PCard object
        try:
            p_card = PCard(
                here=here,
                charge_to_card=amount,
                j_short=j_short,
                j_long=j_long,
                j_why=j_why,
                who=who,
                when=date_c,
                project=source,
            )

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        # Write to file
        try:
            p_card.write_justification()

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        # Download zipped files
        try:
            path = os.path.join(
                app.config["JUSTIFICATIONS"],
                f"SSNL-Justification-{p_card.timestamp}-{amount}.zip",
            )

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        try:
            return download(path)

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

    return render_template(
        "justifications/justification_template.html",
        endpoint="bp_pcard",
        form_title="P-Card Justifcation Form",
        funding_sources=get_projects(),
        members=get_members(),
    )


@app.route("/Reimbursements", methods=["GET", "POST"])
def bp_reimbursements():
    if request.method == "POST":
        from utils.justifications.reimbursement import Reimbursement

        # -- Assign HTML form input to variables
        j_short = request.form["purchased_short"]
        j_long = request.form["purchased_long"]
        j_why = request.form["purchased_why"]
        who = request.form["purchased_by"]
        source = request.form["funding_source"]
        amount = request.form["charge_amount"].replace("$", "").strip()
        date_c = request.form["date_charged"]

        # -- Instantiate Reimbursement object
        try:
            reimburse = Reimbursement(
                here=here,
                charge_to_card=amount,
                j_short=j_short,
                j_long=j_long,
                j_why=j_why,
                who=who,
                when=date_c,
                project=source,
            )

            # Write to file
            reimburse.write_justification()

        except Exception as e:
            message = f"Error @ Reimbursement\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        # Download zipped files
        path = os.path.join(
            app.config["JUSTIFICATIONS"],
            f"SSNL-Reimbursement-{pacific_time}-{amount}.zip",
        )

        try:
            return download(path)

        except Exception as e:
            message = f"Error @ Reimbursement\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

    return render_template(
        "justifications/justification_template.html",
        endpoint="bp_reimbursements",
        form_title="Reimbursement Form",
        funding_sources=get_projects(),
        members=get_members(),
    )


@app.route("/Reocurring-Charges", methods=["GET", "POST"])
def bp_reocurring():
    if request.method == "POST":
        from utils.justifications.reocurring import Reocurring

        # -- HTML form => variables
        charge = request.form["charge"]
        date_of_charge = request.form["date_of_charge"]

        logging.info("Reocurring charge submitted: date={}".format(date_of_charge))

        try:
            ripper = Reocurring(here=here, charge=charge, date_of_charge=date_of_charge)

            # Write to file
            ripper.write_justification()

            # Output filename
            output_filename = ripper.output_name

        except Exception as e:
            message = f"Error @ Reocurring Charges\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        # Download zipped files
        path = os.path.join(app.config["JUSTIFICATIONS"], f"{output_filename}.zip")

        sleep(5)

        try:
            return download(path)

        except Exception as e:
            message = f"Error @ Reocurring Charges\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

    return render_template(
        "justifications/reocurring.html",
        members=get_members(),
        rec_charges=get_reocurring(),
    )


#####


@app.route("/MTurk", methods=["GET", "POST"])
def mturk():
    if request.method == "POST":
        from utils.justifications.mturk import WorkerFile

        # -- HTML form => variables
        file = request.files["file"]
        safe_name = secure_filename(file.filename)

        # -- Create output directories
        output_dir = datetime.now().strftime("mturk_%b_%d_%Y_%H_%M_%S")
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_dir)

        if not os.path.exists(output_path):
            pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

        # Save file
        file.save(os.path.join(output_path, safe_name))

        # -- Instantiate WorkerFile object
        try:
            worker = WorkerFile(
                filename=safe_name,
                filepath=output_path,
                basepath=os.path.join(here, app.config["UPLOAD_FOLDER"]),
                template_path=os.path.join(here, app.config["BP_TEMPLATES"]),
                output_dir=output_path,
            )

            ###

            incoming_columns = [x.lower() for x in worker.load_file().columns]

            # Sanity check
            for var in ["workerid", "payment"]:
                if var not in incoming_columns:
                    flash(f"Whoops! We're missing the {var} column")
                    return redirect(url_for("mturk"))

            ###

            worker.run()

        except Exception as e:
            message = f"Error @ MTurk\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        ###

        try:
            return download(worker.download_me)

        except Exception as e:
            message = f"Error @ MTurk\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

    return render_template("utils/mturk.html")


#####


@app.route("/EMA", methods=["GET", "POST"])
def ema():
    if request.method == "POST":
        from utils.base.scp_ema_parser import EMA_Parser

        # -- Read in and save JSON file
        file = request.files["file"]
        safe_name = secure_filename(file.filename)

        output_dir = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
        output_path = os.path.join(
            app.root_path, app.config["UPLOAD_FOLDER"], output_dir
        )

        if not os.path.exists(output_path):
            pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

        file.save(os.path.join(output_path, safe_name))

        # -- Instantiate EMA_Parser object
        try:
            parser = EMA_Parser(filename=safe_name, output_path=output_path)
            parser.big_dogs_only()

        except Exception as e:
            message = f"Error @ EMA Parser\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        # -- Download resulting files
        target = os.path.join(output_path, "SCP_EMA_Responses.tar.gz")
        return download(target)

    return render_template("utils/ema.html")


@app.route("/combine_pdf", methods=["GET", "POST"])
def combine_pdf():
    if request.method == "POST":
        from PyPDF2 import PdfFileMerger

        # -- Create output directories
        now = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
        output_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], now)

        if not os.path.exists(output_path):
            pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

        # -- List to append into
        ordered_files = []

        # -- Save and aggregate PDF inputs
        logging.info(request.files)

        if len(request.files) == 0:
            flash("No files to merge")
            return redirect(url_for("combine_pdf"))

        for k in request.files:
            temp = request.files[k]

            if ".pdf" in temp.filename:
                safe = secure_filename(temp.filename)
                temp.save(os.path.join(output_path, safe))
                ordered_files.append(os.path.join(output_path, safe))

        # -- Instantiate PdfFileMerger object
        try:
            ripper = PdfFileMerger()

            # Add files to PDF object
            for m in ordered_files:
                ripper.append(m)

            # Download aggregated PDF
            ripper.write(os.path.join(output_path, "MERGED-FILES.pdf"))

            return download(os.path.join(output_path, "MERGED-FILES.pdf"))

        except Exception as e:
            message = f"Error @ Combine PDF\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

    return render_template("utils/combine_pdf.html")


##########

auth = HTTPBasicAuth()
foolproof_security = {"user": "jamil4ever"}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return password == "jamil4ever"


@app.route("/lab_manager", methods=["GET", "POST"])
def lab_manager_login():
    error = None

    if request.method == "POST":
        manager = request.form["name"]
        password = request.form["password"]

        logging.info("\n\nUsername: {}\nPassword: {}\n\n".format(manager, password))

        if verify(manager, password):
            return render_template("lab_manager/landing.html", manager_name=manager)
        else:
            error = "Invalid password!"
            return render_template("lab_manager/login.html", error=error)

    return render_template("lab_manager/login.html", error=error)


@app.route("/lab_manager_landed", methods=["GET", "POST"])
@auth.login_required
def lab_manager_landing():
    return render_template("lab_manager/landing.html", manager_name=None)


@app.route("/lab_manager/view_lab_members", methods=["GET", "POST"])
@auth.login_required
def view_members():
    from utils.base.lab_manager_utils import build_members_df

    dataframe, test = build_members_df()

    return render_template(
        "lab_manager/view_members.html", data=test, data2=dataframe.to_html()
    )


@app.route("/lab_manager/view_projects", methods=["GET", "POST"])
@auth.login_required
def view_projects():
    from utils.base.lab_manager_utils import build_projects_df

    dataframe, projects = build_projects_df()

    return render_template("lab_manager/view_projects.html", data=projects)


@app.route("/lab_manager/update_members", methods=["GET", "POST"])
@auth.login_required
def update_members():
    if request.method == "POST":
        from utils.base.lab_manager_utils import MembersCursor

        # -- Form input
        member = request.form["member_to_update"]
        employee_number = request.form["employee_number"]
        title = request.form["title"]

        cursor = MembersCursor(
            path_to_packets=path_to_members,
            key=member,
            employee_number=employee_number,
            title=title,
        )

        cursor.run()

        comment = f"{member} was updated successfuly!"

        return redirect(url_for("lab_manager_landing", special_text=comment))

    return render_template("lab_manager/update_members.html")


@app.route("/lab_manager/update_projects", methods=["GET", "POST"])
@auth.login_required
def update_projects():
    if request.method == "POST":
        from utils.base.lab_manager_utils import ProjectsCursor

        project = request.form["project_to_update"]
        pta = request.form["pta"]
        sponsor = request.form["sponsor"]
        irb_number = request.form["irb_number"]

        cursor = ProjectsCursor(
            path_to_packets=path_to_projects,
            key=project,
            pta=pta,
            sponsor=sponsor,
            irb_number=irb_number,
        )

        cursor.run()

        comment = f"{project} was updated successfully!"

        return redirect(url_for("lab_manager_landing", special_text=comment))

    return render_template("lab_manager/update_projects.html")


@app.route("/lab_manager/add_lab_member", methods=["GET", "POST"])
@auth.login_required
def add_lab_member():
    if request.method == "POST":
        from utils.base.lab_manager_utils import MembersCursor

        # -- Form input
        member = request.form["member_to_add"]
        employee_number = request.form["employee_number"]
        title = request.form["title"]

        cursor = MembersCursor(
            path_to_packets=path_to_members,
            key=member,
            employee_number=employee_number,
            title=title,
        )

        cursor.run()

        comment = f"{member} was added successfuly!"

        return redirect(url_for("lab_manager_landing", special_text=comment))

    return render_template("lab_manager/add_member.html")


@app.route("/lab_manager/add_project", methods=["GET", "POST"])
@auth.login_required
def add_project():
    if request.method == "POST":
        from utils.base.lab_manager_utils import ProjectsCursor

        project = request.form["project_to_add"]
        pta = request.form["pta"]
        sponsor = request.form["sponsor"]
        irb_number = request.form["irb_number"]

        cursor = ProjectsCursor(
            path_to_packets=path_to_projects,
            key=project,
            pta=pta,
            sponsor=sponsor,
            irb_number=irb_number,
        )

        cursor.run()

        comment = f"{project} was added successfully!"

        return redirect(url_for("lab_manager_landing", special_text=comment))

    return render_template("lab_manager/add_project.html")


##########


@app.route("/download", methods=["GET", "POST"])
def download(filepath):
    return send_file(filepath, as_attachment=True)


def get_members() -> list:
    with open(path_to_members) as temp:
        return sorted(list(json.load(temp).keys()))


def get_projects() -> dict:
    with open(path_to_projects) as temp:
        return json.load(temp)


def get_reocurring() -> list:
    with open(path_to_reocurring) as temp:
        return json.load(temp)


##########


if __name__ == "__main__":
    logging.info("\n=== App Running ===\n")
    app.run(debug=True)
