#!/bin/python3

# --- Imports
import pandas as pd
import os, docx, tarfile
from datetime import date, datetime


# --- Object definitions
class WorkerFile:
      def __init__(self, filename, filepath, basepath, template_path):
            # -- Paths
            self.incoming_filepath = filepath
            self.base_path = basepath
            self.template = os.path.join(template_path, "MTurk.docx")

            # -- Attributes
            self.incoming_file = filename
            self.payments, self.workerfile = self.clean_filename()
            self.working_file = self.clean_dataframe()


      def clean_filename(self):
            temp = self.incoming_file.split(".")[0]

            return f"{temp}_payment-combinations.txt", f"{temp}_workerfile.txt"


      def load_file(self):

            path = os.path.join(self.incoming_filepath, self.incoming_file)
            
            if ".csv" in self.incoming_file:
                  return pd.read_csv(path)

            elif ".xlsx" in self.incoming_file:
                  return pd.read_excel(path, engine="openpyxl")


      def clean_dataframe(self):
            
            dataframe = self.load_file()

            today = datetime.now().strftime("%m/%d/%Y")


            if "fee" in dataframe.columns:
                  dataframe = dataframe.loc[:, ["WorkerId", "payment", "fee"]]
            else:
                  dataframe = dataframe.loc[:, ["WorkerId", "payment"]]
                  dataframe["fee"] = [0.] * len(dataframe)

            dataframe["Date"] = [today] * len(dataframe)

            dataframe.rename(columns={"WorkerId": "MTurk ID", 
                                      "payment": "Pay",
                                      "fee": "AmazonFee"}, inplace=True)

            return dataframe.loc[:, ["Date", "Pay", "AmazonFee", "MTurk ID"]]


      def get_percentage(self, DF):
            return int(DF["AmazonFee"][0] / DF["Pay"][0]) * 100


      def write_payment_combinations(self):
            
            dataframe = self.working_file
            output_name = self.payments

            with open(os.path.join(self.incoming_filepath, output_name), "w") as file:
                  file.write(f"== {output_name} ==\n\n")

                  for pay in dataframe["Pay"].unique():
                        for fee in dataframe["AmazonFee"].unique():
                              temp = dataframe[(dataframe["Pay"] == pay) &
                                               (dataframe["AmazonFee"] == fee)].reset_index(drop=True)

                              file.write(f"* Pay ${pay}\tAmazon fee ${fee}:\t\t{len(temp)}\n")



      def write_workerfile(self):
            
            dataframe = self.working_file
            percent = self.get_percentage(dataframe)
            filename = self.workerfile

            pay_sum = round(sum(dataframe["Pay"]), 2)
            fee_sum = round(sum(dataframe["AmazonFee"]), 2)
            total = pay_sum + fee_sum
            PCT = f"{percent}%"

            with open(os.path.join(self.incoming_filepath, filename), "w") as file:
                  file.write("Total to Participants:\t\t{}".format(pay_sum))
                  file.write("\t\tAmazon Fee: {}".format(PCT))
                  file.write("\nTotal to Amazon:\t\t{}".format(fee_sum))
                  file.write("\n\n--------------\n\n")
                  file.write("Grand Total:\t\t\t{}\n\n\n\n".format(total))
                  file.write("Date\t\tPay\t\tAmazonFee\tMTurk ID\n")

                  for index, date in enumerate(dataframe["Date"]):
                        file.write("{}\t{}\t\t{}\t\t{}\n".format(str(date),
                                                                 str(dataframe["Pay"][index]),
                                                                 str(round(dataframe["AmazonFee"][index], 2)),
                                                                 str(dataframe["MTurk ID"][index])))

                  file.write(f"\n\nTotal Participants:\t\t{len(dataframe)}")


            self.write_justification(total_subs=len(dataframe), price_per_sub=dataframe["Pay"][0],
                                    percent=percent, fee_per_sub=dataframe["AmazonFee"][0],
                                    total=total)


      def gunzip(self):
            with tarfile.open(os.path.join(self.base_path, "SSNL-MTurk-Workerfile.tar.gz"), "w:gz") as tar:
                  tar.add(self.incoming_filepath, arcname="SSNL-MTurk-Workerfile")


      def write_justification(self, total_subs, price_per_sub, percent, fee_per_sub, total):
            doc = docx.Document(self.template)
            today = datetime.today().strftime("%m/%d/%Y")

            doc.paragraphs[3].text = doc.paragraphs[3].text.format("Unraveling Social Influences on Decision-Making",
                                                                  "25837",
                                                                  total_subs,
                                                                  price_per_sub,
                                                                  percent,
                                                                  fee_per_sub,
                                                                  total,
                                                                  today)

            header = doc.sections[0].header
            head = header.paragraphs[0]
            head.text = f"\n\nCreated {today}"

            doc.save(os.path.join(self.incoming_filepath, f"mturk_{total}_zaki.docx"))


      def run(self):
            self.write_payment_combinations()
            self.write_workerfile()
            self.gunzip()
