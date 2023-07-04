### GENERAL PURPOSE ROUTES ###
from flask import render_template, redirect, url_for, request, current_app
import os
from config import SSNLConfig  # TODO - Figure out the app context here...

from ssnl.general import bp
from ssnl.common.utils import post_webhook, get_members, download

##########

methods = ["GET", "POST"]
here = SSNLConfig.HERE

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
    """ABOUT"""

    if request.method == "POST":
        from ssnl.common.justifications.pcard import PCard

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

            return redirect(url_for("general.index"))

        ###

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

        ###

        try:
            p_card.write_justification()

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        ###

        try:
            path = os.path.join(
                current_app.config["JUSTIFICATIONS"],
                f"SSNL-Justification-{p_card.timestamp}-{amount}.zip",
            )

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

        ###

        try:
            return download(path)

        except Exception as e:
            message = f"Error @ P-Card Justification\n\n{e}"
            post_webhook(message=message)

            return redirect(url_for("index"))

    return render_template("justifications/pcard.html", members=get_members())


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
