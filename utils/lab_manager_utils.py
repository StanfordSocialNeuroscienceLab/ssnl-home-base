#!/bin/python3

# --- Imports
import os, json
import pandas as pd
from main import path_to_members, path_to_projects


# --- Functions
def build_members_df():
      """
      Reads in members JSON and stacks each memmber
      into a Pandas DataFrame
      """

      with open(path_to_members) as incoming:
            members = json.load(incoming)

      output = pd.DataFrame()

      for lab_member in list(members.keys()):
            temp_data = members[lab_member]

            temp_df = pd.DataFrame({
                  "Name": temp_data["full-name"],
                  "Employee #": temp_data["employee-number"],
                  "Title": temp_data["title"]
            }, index=[0])

            output = output.append(temp_df, ignore_index=True)

      return output.reset_index(drop=True)


def build_projects_df():
      """
      Reads in projects JSON and stacks each project
      into a Pandas DataFrame
      """

      with open(path_to_projects) as incoming:
            projects = json.load(incoming)

      output = pd.DataFrame()

      for key in list(projects.keys()):

            temp_data = projects[key]

            try:
                  pta = temp_data["funding-string"].split("(")[0].strip()
            except:
                  pta = ""

            try:
                  sponsor = temp_data["funding-string"].split("Sponsor:")[1].strip()
            except:
                  sponsor = ""

            temp_df = pd.DataFrame({
                  "Key": key,
                  "PTA": pta,
                  "Sponsor": sponsor,
                  "IRB Number": temp_data["irb-number"]
            }, index=[0])

            output = output.append(temp_df, ignore_index=True)

      return output.reset_index(drop=True)