#!/bin/python3
from flask import Flask, render_template, url_for, redirect, request
import json, sqlite3, sys, os, pathlib, shutil
from datetime import datetime


##########


def cleanup_output(path):
    """
    Quick function to wipe out any previously uploaded files at init
    """

    for file in os.listdir(path):
        if file != ".DS_Store":

            temp = os.path.join(path, file)

            if os.path.isdir(temp):
                try:
                    shutil.rmtree(temp)
                except Exception as e:
                    print(e)

            elif os.path.isfile(temp):
                try:
                    os.remove(temp)
                except Exception as e:
                    print(e)
