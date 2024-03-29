### GENERAL PURPOSE ROUTES ###
from flask import render_template, redirect, url_for, request, flash, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import pathlib
import os
import traceback
from config import SSNLConfig

from ssnl.general import bp
from ssnl.common.utils import (
    post_webhook,
    download,
    get_members,
    get_projects,
    get_reocurring_projects,
)

##########

methods = ["GET", "POST"]
here = SSNLConfig.HERE
dev = SSNLConfig.DEVMODE

#####


@bp.route("/", methods=methods)
def index():
    return render_template("index.html")


@bp.route("/justifications", methods=methods)
def bp_justifications():
    """
    Renders the landing page for other financial forms
    """

    return render_template("landing.html")


@bp.route("/p_card", methods=methods)
def bp_pcard():
    if request.method == "POST":
        from ssnl.common.justifications.pcard import PCard

        try:
            j_short = request.form["purchased_short"]
            j_long = request.form["purchased_long"]
            j_why = request.form["purchased_why"]
            who = request.form["purchased_by"]
            source = request.form["funding_source"]
            where = request.form["purchased_where"]
            amount = request.form["charge_amount"].replace("$", "")
            date_c = request.form["date_charged"]

            p_card = PCard(
                here=here,
                charge_to_card=amount,
                j_short=j_short,
                j_long=j_long,
                j_why=j_why,
                who=who,
                when=date_c,
                where=where,
                project=source,
            )

            p_card.write_justification()

            path = os.path.join(
                SSNLConfig.JUSTIFICATIONS,
                f"SSNL-Justification-{p_card.timestamp}-{amount}.zip",
            )

            return download(path)

        except Exception as e:
            # if dev:
            #     raise e

            message = f"Error @ P-Card Justification\n\n{str(traceback.format_exc())}"
            post_webhook(message=message)

            return redirect(url_for("general.index"))

    return render_template(
        "justifications/justification_template.html",
        endpoint="general.bp_pcard",
        form_title="P-Card Justifcation Form",
        funding_sources=get_projects(),
        members=get_members(),
    )


@bp.route("/reimbursements", methods=methods)
def bp_reimbursements():
    if request.method == "POST":
        from ssnl.common.justifications.reimbursement import Reimbursement

        j_short = request.form["purchased_short"]
        j_long = request.form["purchased_long"]
        j_why = request.form["purchased_why"]
        who = request.form["purchased_by"]
        source = request.form["funding_source"]
        amount = request.form["charge_amount"].replace("$", "").strip()
        date_c = request.form["date_charged"]
        where = request.form["purchased_where"]

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
                where=where,
            )

            # Write to file
            reimburse.write_justification()

            # Download zipped files
            path = os.path.join(
                SSNLConfig.JUSTIFICATIONS,
                f"SSNL-Reimbursement-{reimburse.timestamp}-{amount}.zip",
            )

            return download(path)

        except Exception as e:
            if dev:
                raise e

            message = f"Error @ Reimbursement\n\n{str(traceback.format_exc())}"
            post_webhook(message=message)

            return redirect(url_for("general.index"))

    return render_template(
        "justifications/justification_template.html",
        endpoint="general.bp_reimbursements",
        form_title="Reimbursement Form",
        funding_sources=get_projects(),
        members=get_members(),
    )


@bp.route("/reocurring", methods=methods)
def bp_reocurring():
    if request.method == "POST":
        from ssnl.common.justifications.reocurring import Reocurring

        charge = request.form["charge"]
        date_of_charge = request.form["date_of_charge"]

        try:
            ripper = Reocurring(here=here, charge=charge, date_of_charge=date_of_charge)

            # Write to file
            ripper.write_justification()

            # Output filename
            output_filename = ripper.output_name

            path = os.path.join(SSNLConfig.JUSTIFICATIONS, f"{output_filename}.zip")

            return download(path)

        except Exception as e:
            if dev:
                raise e

            message = f"Error @ Reocurring Charges\n\n{str(traceback.format_exc())}"
            post_webhook(message=message)

            return redirect(url_for("general.index"))

    rec_charges = get_reocurring_projects()

    return render_template("justifications/reocurring.html", rec_charges=rec_charges)


@bp.route("/mturk", methods=methods)
def mturk():
    if request.method == "POST":
        from ssnl.common.justifications.mturk import WorkerFile

        file = request.files["file"]
        safe_name = secure_filename(file.filename)

        output_dir = datetime.now().strftime("mturk_%b_%d_%Y_%H_%M_%S")
        output_path = os.path.join(SSNLConfig.UPLOAD_FOLDER, output_dir)

        if not os.path.exists(output_path):
            pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

        file.save(os.path.join(output_path, safe_name))

        try:
            worker = WorkerFile(
                filename=safe_name,
                filepath=output_path,
                basepath=os.path.join(here, SSNLConfig.UPLOAD_FOLDER),
                template_path=os.path.join(here, SSNLConfig.BP_TEMPLATES),
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

            return download(worker.download_me)

        except Exception as e:
            if dev:
                raise e

            message = f"Error @ MTurk\n\n{str(traceback.format_exc())}"
            post_webhook(message=message)

            return redirect(url_for("general.index"))

    return render_template("utils/mturk.html")


@bp.route("/combine_pdf", methods=methods)
def combine_pdf():
    if request.method == "POST":
        from PyPDF2 import PdfFileMerger

        now = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
        output_path = os.path.join(SSNLConfig.ROOT, SSNLConfig.UPLOAD_FOLDER, now)

        if not os.path.exists(output_path):
            pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

        ordered_files = []

        if len(request.files) == 0:
            flash("No files to merge")
            return redirect(url_for("combine_pdf"))

        for k in request.files:
            temp = request.files[k]

            if ".pdf" in temp.filename:
                safe = secure_filename(temp.filename)
                temp.save(os.path.join(output_path, safe))
                ordered_files.append(os.path.join(output_path, safe))

        try:
            ripper = PdfFileMerger()

            # Add files to PDF object
            for m in ordered_files:
                ripper.append(m)

            # Download aggregated PDF
            ripper.write(os.path.join(output_path, "MERGED-FILES.pdf"))

            return download(os.path.join(output_path, "MERGED-FILES.pdf"))

        except Exception as e:
            if dev:
                raise e

            message = f"Error @ Combine PDF\n\n{str(traceback.format_exc())}"
            post_webhook(message=message)

            return redirect(url_for("general.index"))

    return render_template("utils/combine_pdf.html")


@bp.route("/download", methods=["GET", "POST"])
def download(filepath):
    return send_file(filepath, as_attachment=True)
