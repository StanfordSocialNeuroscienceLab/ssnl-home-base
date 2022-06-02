#!/bin/python3

"""
About these Classes


Ian Ferguson | Stanford University
"""


# --- Imports
import json, docx, pathlib, os
import tarfile
from datetime import datetime


# --- Packets
members = {"Jamil": {
            "full-name": "Jamil Zaki",
            "title": "Jamil Zaki, PI for the Social Neuroscience Lab in the Psychology Department",
            "employee-number": "005778469"
            },
            "Rachel Calcott": {
                  "full-name": "Rachel Calcott",
                  "title": "Rachel Calcott, Lab Manager in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "NONE"
            },
            "Ian Ferguson": {
                  "full-name": "Ian Ferguson",
                  "title": "Ian Ferguson, Lab Manager in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "50017234"
            },
            "Marianne Reddan": {
                  "full-name": "Marianne Reddan",
                  "title": "Marianne Reddan, postdoc in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "06406897"
            },
            "Andrea Courtney": {
                  "full-name": "Andrea Courtney",
                  "title": "Andrea Courtney, postdoc in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "06324767"
            },
            "Rui Pei": {
                  "full-name": "Rui Pei",
                  "title": "Rui Pei, postdoc in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "06642333"
            },
            "Luiza Santos": {
                  "full-name": "Luiza Santos",
                  "title": "Luiza Santos, PhD student in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "NONE"
            },
            "Eric Neumann": {
                  "full-name": "Eric Neumann",
                  "title": "Eric Neumann, PhD student in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "NONE"
            },
            "Dean Baltiansky": {
                  "full-name": "Dean Baltiansky",
                  "title": "Dean Baltiansky, Research Assistant in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "050014827"
            },
            "Wicia Fang": {
                  "full-name": "Wicia Fang",
                  "title": "Wicia Fang, Research Assistant in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "06058964"
            },
            "Sydney Garcia": {
                  "full-name": "Sydney Garcia",
                  "title": "Sydney Garcia, Research Assistant in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "06124957"
            },
            "Samantha Grayson": {
                  "full-name": "Samantha Grayson",
                  "title": "Samantha Grayson, Research Assistant in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "50018861"
            },
            "Daniel Ogunbamowo": {
                  "full-name": "Daniel Ogunbamowo",
                  "title": "Daniel Ogunbamowo, Research Assistant in the Social Neuroscience Lab (PI: Jamil Zaki) in the Psychology Department",
                  "employee-number": "50018870"
            }
      }


projects = {
      "Just Mercy": {
            "funding-string": "1239209-100-UAQQZ (PI: Jamil Zaki, Sponsor: Good Films Impact)",
            "award": "UAQQZ",
            "irb-number": "IRB-36348",
            "irb-name": "Empathy and Emotion Understanding in Social Contexts"
      },
      "MASC": {
            "funding-string": "1204832-100-PAKUV (PI: Jamil Zaki, Sponsor: NIH R01)",
            "award": "PAKUV",
            "irb-number": "",
            "irb-name": ""
      },
      "ResX": {
            "funding-string": "1231456-1-DDLHA (PI: Jamil Zaki, Sponsor: Provost ResX Task Force)",
            "award": "DDLHA",
            "irb-number": "IRB-24593",
            "irb-name": "Relationships as Psychological Protective Factors: Neural and Behavioral Markers or Prosocial Behavior Across the Lifespan or Vicarious Reward: A Neural Marker for Beneficial Social Relationships"
      },
      "SCP R01": {
            "funding-string": "1254167-100-PAGYP (PI: Jamil Zaki, Sponsor: National Institute of Health)",
            "award": "PAGYP",
            "irb-number": "IRB-24593",
            "irb-name": "Relationships as Psychological Protective Factors: Neural and Behavioral Markers or Prosocial Behavior Across the Lifespan or Vicarious Reward: A Neural Marker for Beneficial Social Relationships"
      },
      "NSF": {
            "funding-string": "1179634-100-QAASO (PI: Jamil Zaki, Sponsor: National Science Foundation)",
            "award": "QAASO",
            "irb-number": "NA",
            "irb-name": "NA"
      },
      "MOC": {
            "funding-string": "1224924-1-DDLFE (PI: Jamil Zaki, Sponsor: Media and Outrach Committee)",
            "award": "DDLFE",
            "irb-number": "NA",
            "irb-name": "NA"
      },
      "STAP": {
            "funding-string": "{}'s STAP funds",
            "award": "STAP",
            "irb-number": "NA",
            "irb-name": "NA"
      },
      "Dean's": {
            "funding-string": "1145804-1-FZBRB (PI: Jamil Zaki, Sponsor: Dean's Account)",
            "award": "FZBRB",
            "irb-number": "IRB-25837",
            "irb-name": "Unraveling Social Influences on Decision-Making"
      }
}



# --- Object definitions
class PCard:
      def __init__(self, here, charge_to_card, j_short, j_long, j_why, who, when, project):

            today_f = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")

            self.base_path = os.path.join(here, "files/justifications")

            self.input_path = os.path.join(here, "files/templates")
            self.output_path = os.path.join(self.base_path, today_f)

            if not os.path.exists(self.output_path):
                  pathlib.Path(self.output_path).mkdir(exist_ok=True, parents=True)

            self.output_filename = f"pcard_{charge_to_card}_zaki.docx"

            self.j_short = j_short
            self.j_long = j_long
            self.j_why = j_why
            self.who = members[who]
            self.when = when
            self.project = projects[project]


      def load_template(self):
            return docx.Document(os.path.join(self.input_path, "P-Card.docx"))


      def write_justification(self):

            template = self.load_template()

            now = datetime.now().strftime("%m/%d/%Y")

            template.paragraphs[3].text = template.paragraphs[3].text.format(self.j_short,
                                                                             self.project["award"],
                                                                             self.who["title"],
                                                                             self.j_long,
                                                                             self.when,
                                                                             self.j_why,
                                                                             self.project["funding-string"])


            header = template.sections[0].header
            head = header.paragraphs[0]
            head.text = f"\n\nCreated {now}"

            template.save(os.path.join(self.output_path, self.output_filename))

            self.gunzip()



      def gunzip(self):

            with tarfile.open(os.path.join(self.base_path, "SSNL-Justification.tar.gz"), "w:gz") as tar:
                  tar.add(self.output_path, arcname=f"SSNL-Justification-{datetime.now().strftime('%m-%d-%Y')}")




class Reimbursement:
      def __init__(self, here, charge_to_card, j_short, j_long, j_why, who, when, project):
            today_f = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")

            self.base_path = os.path.join(here, "files/justifications")

            self.input_path = os.path.join(here, "files/templates")
            self.output_path = os.path.join(self.base_path, today_f)

            if not os.path.exists(self.output_path):
                  pathlib.Path(self.output_path).mkdir(
                        exist_ok=True, parents=True)

            self.output_filename = f"reimbursement_{charge_to_card}_zaki.docx"

            self.j_short = j_short
            self.j_long = j_long
            self.j_why = j_why
            self.who = members[who]
            self.when = when
            self.project = projects[project]



      def load_template(self):
            return docx.Document(os.path.join(self.input_path, "Reimbursement.docx"))



      def write_justification(self):

            template = self.load_template()

            now = datetime.now().strftime("%m/%d/%Y")

            template.paragraphs[3].text = template.paragraphs[3].text.format(self.j_short,
                                                                             self.project["award"],
                                                                             self.who["title"],
                                                                             self.who["employee-number"],
                                                                             self.j_long,
                                                                             self.when,
                                                                             self.j_why,
                                                                             self.project["funding-string"])


            header = template.sections[0].header
            head = header.paragraphs[0]
            head.text = f"\n\nCreated {now}"

            template.save(os.path.join(self.output_path, self.output_filename))

            self.gunzip()



      def gunzip(self):
            with tarfile.open(os.path.join(self.base_path, "SSNL-Reimbursement.tar.gz"), "w:gz") as tar:
                  tar.add(self.output_path, arcname=f"SSNL-Reimbursement-{datetime.now().strftime('%m-%d-%Y')}")



class Reocurring:
      def __init__(self, here, charge, date_of_charge):
            self.charge = charge
            self.date = date_of_charge

            today_f = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")

            self.base_path = os.path.join(here, "files/justifications")
            self.template_path = os.path.join(here, "files/templates/reoccuring")
            self.output_path = os.path.join(self.base_path, today_f)

            if not os.path.exists(self.output_path):
                  pathlib.Path(self.output_path).mkdir(exist_ok=True, parents=True)


      def get_file(self):
            if self.charge == "AWS_SCP":
                  filename = "pcard_AWS-SCP_zaki.docx"
                  filepath = os.path.join(self.template_path, "SCP_AWS.docx")

            elif self.charge == "AWS_JM":
                  filename = "pcard_AWS-JM_zaki.docx"
                  filepath = os.path.join(self.template_path, "JM_AWS.docx")

            elif self.charge == "Mailchimp":
                  filename = "pcard_87.00_zaki.docx"
                  filepath = os.path.join(self.template_path, "SCP_Mailchimp.docx")

            elif self.charge == "Forge":
                  filename = "pcard_12.00_zaki.docx"
                  filepath = os.path.join(self.template_path, "JM_Forge.docx")

            elif self.charge == "Buzzsprout":
                  filename = "pcard_27.00_zaki.docx"
                  filepath = os.path.join(self.template_path, "Buzzsprout.docx")

            
            return filename, filepath



      def write_justification(self):
            
            filename, filepath = self.get_file()

            doc = docx.Document(filepath)
            doc.paragraphs[3].text = doc.paragraphs[3].text.format(self.date)

            header = doc.sections[0].header
            head = header.paragraphs[0]
            head.text = "\n\nCreated {}".format(datetime.today().strftime("%m/%d/%Y"))

            doc.save(os.path.join(self.output_path, filename))

            self.gunzip()


      def gunzip(self):
            with tarfile.open(os.path.join(self.base_path, f"SSNL-{self.charge}.tar.gz"), "w:gz") as tar:
                  tar.add(self.output_path, arcname=f"SSNL-{self.charge}")



class FoodOrder:
      def __init__(self):
            pass



class LabLunch:
      def __init__(self):
            pass
