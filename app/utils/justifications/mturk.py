#!/bin/python3
import pandas as pd
import os, docx, shutil
from datetime import datetime
from uuid import uuid4
import pathlib

from ..base.helper import drop_a_line


##########


class WorkerFile:
    """
    This class intakes a workerfile and generates the following output files:

    * Workerfile manifest (how much each person got paid)
    * A breakdown of each charge / bonus count
    """

    def __init__(self, filename, filepath, basepath, template_path, output_dir):
        self.incoming_filepath = filepath
        self.base_path = basepath
        self.template = os.path.join(template_path, "MTurk.docx")

        ###

        self.output_path = output_dir
        pathlib.Path(self.output_path).mkdir(exist_ok=True, parents=True)

        ###

        self.incoming_file = filename
        self.payments, self.workerfile = self.clean_filename()
        self.working_file = self.clean_dataframe()

        ###

        self.hex = uuid4().hex

    def clean_filename(self):
        """
        Generates output filenames
        """

        temp = self.incoming_file.split(".")[0]

        return f"{temp}_payment-combinations.txt", f"{temp}_workerfile.txt"

    def load_file(self):
        """
        Wrapper to process tabular data upload

        NOTE: This is hardcoded to two file types, as that is all the intake route allows
        """

        path = os.path.join(self.incoming_filepath, self.incoming_file)

        if ".csv" in self.incoming_file:
            return pd.read_csv(path)

        elif ".xlsx" in self.incoming_file:
            return pd.read_excel(path, engine="openpyxl")

    def clean_dataframe(self):
        """
        This function standardizes column names, replaces null values
        """

        dataframe = self.load_file()

        # NOTE: Adding this to prevent needless exceptions
        dataframe.fillna(0, inplace=True)

        today = datetime.now().strftime("%m/%d/%Y")

        # Allow end user to feed variable-case data
        dataframe.columns = [x.lower() for x in dataframe.columns]

        if "fee" in dataframe.columns:
            dataframe = dataframe.loc[:, ["workerid", "payment", "fee"]]
        else:
            dataframe = dataframe.loc[:, ["workerid", "payment"]]
            dataframe["fee"] = [0.0] * len(dataframe)

        dataframe["Date"] = [today] * len(dataframe)

        dataframe.rename(
            columns={"workerid": "MTurk ID", "payment": "Pay", "fee": "AmazonFee"},
            inplace=True,
        )

        return dataframe.loc[:, ["Date", "Pay", "AmazonFee", "MTurk ID"]]

    def get_percentage(self, DF):
        """
        Determines bonus percentage

        NOTE: This number will NOT be accurate when there are different pay / bonus structures
        """

        return int(DF["AmazonFee"][0] / DF["Pay"][0]) * 100

    def write_payment_combinations(self):
        """
        Creates a text file with a manifest of pay / bonus combinations to plug in
        to the justification if needed
        """

        dataframe = self.working_file
        output_name = self.payments

        with open(os.path.join(self.output_path, output_name), "w") as file:
            file.write(f"== {output_name} ==\n\n")

            """
            Loops through unique pay values and unique bonus values ... determines
            the number of each combination by subsetting the dataframe and inputting
            the resulting length 
            """

            for pay in dataframe["Pay"].unique():
                for fee in dataframe["AmazonFee"].unique():
                    temp = dataframe[
                        (dataframe["Pay"] == pay) & (dataframe["AmazonFee"] == fee)
                    ].reset_index(drop=True)

                    file.write(f"* Pay ${pay}\tAmazon fee ${fee}:\t\t{len(temp)}\n")

    def write_workerfile(self):
        """
        Generate textfile of participant compensation
        """

        dataframe = self.working_file
        percent = self.get_percentage(dataframe)
        filename = self.workerfile

        ###

        pay_sum = round(sum(dataframe["Pay"]), 2)
        fee_sum = round(sum(dataframe["AmazonFee"]), 2)
        total = pay_sum + fee_sum
        PCT = f"{percent}%"

        ###

        with open(os.path.join(self.output_path, filename), "w") as file:
            file.write("Total to Participants:\t\t{}".format(pay_sum))
            file.write("\t\tAmazon Fee: {}".format(PCT))
            file.write("\nTotal to Amazon:\t\t{}".format(fee_sum))
            file.write("\n\n--------------\n\n")
            file.write("Grand Total:\t\t\t{}\n\n\n\n".format(total))
            file.write("Date\t\tPay\t\tAmazonFee\tMTurk ID\n")

            for index, date in enumerate(dataframe["Date"]):
                file.write(
                    "{}\t{}\t\t{}\t\t{}\n".format(
                        str(date),
                        str(dataframe["Pay"][index]),
                        str(round(dataframe["AmazonFee"][index], 2)),
                        str(dataframe["MTurk ID"][index]),
                    )
                )

            file.write(f"\n\nTotal Participants:\t\t{len(dataframe)}")

        ###

        self.write_justification(
            total_subs=len(dataframe),
            price_per_sub=dataframe["Pay"][0],
            percent=percent,
            fee_per_sub=dataframe["AmazonFee"][0],
            total=total,
        )

        drop_a_line(self.incoming_filepath)

    def gunzip(self):
        """
        Creates zip archive of all output generated by this class
        """

        out_path = os.path.join(self.base_path, f"SSNL-MTurk-{self.hex}")
        shutil.make_archive(out_path, "zip", self.output_path)
        self.download_me = os.path.join(self.base_path, f"SSNL-MTurk-{self.hex}.zip")

    def write_justification(
        self, total_subs, price_per_sub, percent, fee_per_sub, total
    ):
        """
        Generate .docx file with justification data
        """

        doc = docx.Document(self.template)
        today = datetime.today().strftime("%m/%d/%Y")

        doc.paragraphs[3].text = doc.paragraphs[3].text.format(
            "Unraveling Social Influences on Decision-Making",
            "25837",
            total_subs,
            price_per_sub,
            percent,
            fee_per_sub,
            total,
            today,
        )

        doc.paragraphs[3].text = (
            doc.paragraphs[3].text.replace('"', "").replace("'", "")
        )

        header = doc.sections[0].header
        head = header.paragraphs[0]
        head.text = f"\n\nCreated {today}"

        doc.save(os.path.join(self.output_path, f"mturk_{total}_zaki.docx"))

    def run(self):
        """
        Wraps all of the above
        """

        self.write_payment_combinations()
        self.write_workerfile()
        self.gunzip()
