#!/bin/python3
import os, json
import pandas as pd
from main import path_to_members, path_to_projects


##########


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

        temp_df = pd.DataFrame(
            {
                "full_name": temp_data["full_name"],
                "employee_number": temp_data["employee_number"],
                "title": temp_data["title"],
            },
            index=[0],
        )

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
            "irb_number": temp_data["irb-number"],
        }

        temp_df = pd.DataFrame(clean_dictionary, index=[0])

        output = output.append(temp_df, ignore_index=True)
        projects_.append(clean_dictionary)

    return output.reset_index(drop=True), projects_


#####


class JSONCursor:
    def __init__(self, path_to_packets, packet="members"):
        """
        Simple wrapper to perform input and output functions
        on the underlying members and projects dictionaries
        """

        self.base_path = path_to_packets
        self.packet_type = packet

        self.filepath = os.path.join(self.base_path)

    def open_file(self):

        with open(self.filepath) as incoming:
            return json.load(incoming)

    def save_file(self, temp_dictionary):

        with open(self.filepath, "w") as outgoing:
            json.dump(temp_dictionary, outgoing, indent=4)


#####


class MembersCursor(JSONCursor):
    def __init__(
        self, path_to_packets, key, employee_number, title, create_new_key=False
    ):

        JSONCursor.__init__(self, path_to_packets, packet="members")

        self.key = key
        self.employee_number = employee_number
        self.title = title

        self.create_new_key = create_new_key

    def run(self):

        temp_data = self.open_file()

        if self.create_new_key:
            temp_data[self.key] = {}

        if self.employee_number != "":
            temp_data[self.key]["employee_number"] = self.employee_number

        if self.title != "":
            temp_data[self.key]["title"] = self.title

        self.save_file(temp_dictionary=temp_data)


#####


class ProjectsCursor(JSONCursor):
    def __init__(
        self, path_to_packets, key, pta, sponsor, irb_number, create_new_key=False
    ):

        JSONCursor.__init__(self, path_to_packets=path_to_packets, packet="projects")

        self.key = key
        self.pta = pta
        self.sponsor = sponsor
        self.irb_number = irb_number

        self.create_new_key = create_new_key

    def run(self):

        temp_data = self.open_file()

        if self.create_new_key:
            temp_data[self.key] = {}

        if self.pta != "":
            temp_data[self.key]["pta"] = self.pta

        if self.sponsor != "":
            temp_data[self.key]["sponsor"] = self.sponsor

        if self.irb_number != "":
            temp_data[self.key]["irb_number"] = self.irb_number

        self.save_file(temp_dictionary=temp_data)
