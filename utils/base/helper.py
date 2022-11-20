#!/bin/python3
import os
import shutil
import random


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


def drop_a_line(path):

    options = [
        "Have a nice day!",
        "Keep up the great work!",
        "You're doing great!",
        "You are the sun and the moon!",
        "You are absolute magic!",
        "Thank you for being you!",
        "Make today great!",
        "Make it a great day!",
        "Do something nice for yourself today!",
        "You are a light everywhere you go!",
        "You can accomplish anything you set your mind to!",
        "Everyone needs a friend like you!",
    ]

    with open(os.path.join(path, "README.txt"), "w") as file:
        message = random.choice(options)

        file.write("PLEASE READ\n\n")
        file.write(message)
