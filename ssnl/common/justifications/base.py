### BASIC FINANCIAL OBJECT FOR INHERITANCE ###
from config import SSNLConfig
import json
from datetime import datetime
import pytz

##########


class FinanceObject:
    """
    Test test test
    """

    def __init__(self):
        self.here = SSNLConfig.HERE

        self.__path_to_members = SSNLConfig.MEMBER_PATH
        self.__path_to_projects = SSNLConfig.PROJECT_PATH

        with open(self.__path_to_members) as temp:
            self.member_dictionary = json.load(temp)

        with open(self.__path_to_projects) as temp:
            self.project_dictioanry = json.load(temp)

        self.__timestamp = datetime.now(pytz.timezone("US/Pacific"))
