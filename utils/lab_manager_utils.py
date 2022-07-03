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
      members_ = []

      for lab_member in list(members.keys()):
            temp_data = members[lab_member]

            temp_df = pd.DataFrame({
                  "full_name": temp_data["full_name"],
                  "employee_number": temp_data["employee_number"],
                  "title": temp_data["title"]
            }, index=[0])

            output = output.append(temp_df, ignore_index=True)
            members_.append(temp_data)

      return output.reset_index(drop=True), members_


def build_projects_df():
      """
      Reads in projects JSON and stacks each project
      into a Pandas DataFrame
      """

      with open(path_to_projects) as incoming:
            projects = json.load(incoming)

      output = pd.DataFrame()
      projects_ = []

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

            clean_dictionary = {
                  "key": key,
                  "pta": pta,
                  "sponsor": sponsor.replace(")", ""),
                  "irb_number": temp_data["irb-number"]
            }

            temp_df = pd.DataFrame(clean_dictionary, index=[0])

            output = output.append(temp_df, ignore_index=True)
            projects_.append(clean_dictionary)

      return output.reset_index(drop=True), projects_