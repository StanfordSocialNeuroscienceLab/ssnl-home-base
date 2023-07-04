### GENERAL PURPOSE ROUTES ###
from flask import render_template, redirect, url_for
from ssnl.general import bp

##########

methods = ["GET", "POST"]


@bp.route("/", methods=methods)
def index():
    return render_template("index.html")


@bp.route("/justifications", methods=methods)
def bp_justifications():
    return render_template("landing.html")


@bp.route("/p_card", methods=methods)
def bp_pcard():
    return redirect(url_for("general.index"))


@bp.route("/reimbursements", methods=methods)
def bp_reimbursements():
    return redirect(url_for("general.index"))


@bp.route("/reocurring", methods=methods)
def bp_reocurring():
    return redirect(url_for("general.index"))


@bp.route("/mturk", methods=methods)
def mturk():
    return redirect(url_for("general.index"))


@bp.route("/combine_pdf", methods=methods)
def combine_pdf():
    return redirect(url_for("general.index"))
