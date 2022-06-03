#!/bin/python3

# --- Imports
from flask import Flask, render_template, send_file, request
from werkzeug.utils import secure_filename
import os, pathlib
from datetime import datetime
from helper import *

# == APP CONFIGURATION ==
app = Flask(__name__)
here = app.root_path

app.config["UPLOAD_FOLDER"] = "files/uploads"
app.config["JUSTIFICATIONS"] = "files/justifications"
app.config["BP_TEMPLATES"] = "files/templates"


# -- Confirm output directories exist at __init__
for path in ["uploads", "justifications"]:

      temp = os.path.join(here, "files", path)

      if not os.path.exists(temp):
            pathlib.Path(temp).mkdir(parents=True, exist_ok=True)


# == ROUTING ==
@app.route("/", methods=["GET", "POST"])
def index():
      # Start with a clean cache
      for dir in ["files/uploads", "files/justifications"]:
            try:
                  cleanup_output(dir)
            except Exception as e:
                  print(e)

      return render_template("index.html")



@app.route("/Admin", methods=["GET", "POST"])
def admin():
      return render_template("admin.html")



# -- Justifications
@app.route("/Justifications", methods=["GET", "POST"])
def bp():
      return render_template("landing.html")



@app.route("/P-Card", methods=["GET", "POST"])
def bp_pcard():

      if request.method == "POST":

            from justifications.justification import PCard

            # -- Assign HTML form input to variables
            j_short = request.form["purchased_short"]
            j_long = request.form["purchased_long"]
            j_why = request.form["purchased_why"]
            who = request.form["purchased_by"]
            source = request.form["funding_source"]
            amount = request.form["charge_amount"].replace("$", "")
            date_c = request.form["date_charged"]

            # -- Instantiate PCard object
            p_card = PCard(here=here, charge_to_card=amount, j_short=j_short,
                          j_long=j_long, j_why=j_why, who=who, when=date_c,
                          project=source)

            # Write to file
            p_card.write_justification()

            # Download zipped files
            path = os.path.join(app.config["JUSTIFICATIONS"], "SSNL-Justification.tar.gz")
            return download(path)

      return render_template("pcard.html")


@app.route("/Reimbursements", methods=["GET", "POST"])
def bp_reimbursements():

      if request.method == "POST":

            from justifications.justification import Reimbursement

            # -- Assign HTML form input to variables
            j_short = request.form["purchased_short"]
            j_long = request.form["purchased_long"]
            j_why = request.form["purchased_why"]
            who = request.form["purchased_by"]
            source = request.form["funding_source"]
            amount = request.form["charge_amount"].replace("$", "")
            date_c = request.form["date_charged"]

            # -- Instantiate Reimbursement object
            reimburse = Reimbursement(here=here, charge_to_card=amount, j_short=j_short,
                                      j_long=j_long, j_why=j_why, who=who, when=date_c,
                                      project=source)

            # Write to file
            reimburse.write_justification()

            # Download zipped files
            path = os.path.join(app.config["JUSTIFICATIONS"], "SSNL-Reimbursement.tar.gz")
            return download(path)

      return render_template("reimbursement.html")


@app.route("/Reocurring-Charges", methods=["GET", "POST"])
def bp_reocurring():

      if request.method == "POST":

            from justifications.justification import Reocurring

            # -- HTML form => variables
            charge = request.form["charge"]
            date_of_charge = request.form["date_of_charge"]

            # -- Instantiate Reocurring object
            ripper = Reocurring(here=here, charge=charge, date_of_charge=date_of_charge)

            # Write to file
            ripper.write_justification()

            # Download zipped files
            path = os.path.join(app.config["JUSTIFICATIONS"], f"SSNL-{charge}.tar.gz")
            return download(path)

      return render_template("reocurring.html")


# -- MTurk
@app.route("/MTurk", methods=["GET", "POST"])
def mturk():

      if request.method == "POST":

            from utils.mturk import WorkerFile

            # -- HTML form => variables
            file = request.files["file"]
            safe_name = secure_filename(file.filename)

            # -- Create output directories
            output_dir = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_dir)

            if not os.path.exists(output_path):
                  pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

            # Save file
            file.save(os.path.join(output_path, safe_name))

            # -- Instantiate WorkerFile object
            worker = WorkerFile(filename=safe_name, filepath=output_path,
                                basepath=os.path.join(here, app.config["UPLOAD_FOLDER"]),
                                template_path=os.path.join(here, app.config["BP_TEMPLATES"]))
            worker.run()

            # Download zipped files
            target = os.path.join(app.config["UPLOAD_FOLDER"], "SSNL-MTurk-Workerfile.tar.gz")
            return download(target)

      return render_template("mturk.html")


# -- EMA
@app.route("/EMA", methods=["GET", "POST"])
def ema():

      if request.method == "POST":

            from utils.scp_ema_parser import EMA_Parser

            # -- Read in and save JSON file
            file = request.files["file"]
            safe_name = secure_filename(file.filename)

            output_dir = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
            output_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], output_dir)

            if not os.path.exists(output_path):
                  pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)

            file.save(os.path.join(output_path, safe_name))

            # -- Instantiate EMA_Parser object
            parser = EMA_Parser(filename=safe_name, output_path=output_path)
            parser.big_dogs_only()

            # -- Download resulting files
            target = os.path.join(output_path, "SCP_EMA_Responses.tar.gz")
            return download(target)

      return render_template("ema.html")


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
            for k in request.files:
                  temp = request.files[k]

                  if ".pdf" in temp.filename:
                        safe = secure_filename(temp.filename)
                        temp.save(os.path.join(output_path, safe))
                        ordered_files.append(os.path.join(output_path, safe))


            # -- Instantiate PdfFileMerger object
            ripper = PdfFileMerger()

            # Add files to PDF object
            for m in ordered_files:
                  ripper.append(m)

            # Download aggregated PDF
            ripper.write(os.path.join(output_path, "MERGED-FILES.pdf"))
            return download(os.path.join(output_path, "MERGED-FILES.pdf"))

      return render_template("combine_pdf.html")


@app.route("/download", methods=["GET", "POST"])
def download(filepath):
      return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
      app.run(debug=True)