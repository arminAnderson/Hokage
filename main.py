import sys
import json
import os
import subprocess
import datetime
from datetime import date
from json.decoder import JSONDecodeError

# - - - - - UTIL - - - - - #
class InfoBundle():
    def __init__(self, id, stars, date, comment):
        self.id = id
        self.stars = stars
        self.date = date
        self.comment = comment
    def ToJson(self):
        return self.__dict__

def WaitForYN(message):
    s = None
    while s != "y" and s!= "n":
        s = input(message + " (y/n): ")
    return s

def Save():
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print("JSON saved to file.")

def Open():
    try:
        with open('data.txt') as jsonFile:
            temp = json.load(jsonFile)
            for name in temp:
                for p in temp[name]:
                    Add(name, p["id"], p["stars"], p["date"], p["comment"])
        print("JSON loaded.")
    except JSONDecodeError:
        print("Error reading file.")

def TodaysDate():
    return str(date.today())

def GetStudent(name):
    if not name in data:
        data[name] = []
        print("Student '" + name + "' added.")
    else:
        print("Projects for '" + name + "':")
        for p in data[name]:
            print("\tName: {}\tStars: {}\tDate: {}\tComment: {}".format(activities[int(p["id"])], p["stars"], p["date"], p["comment"]))
        print()

def Add(name, id, stars, date, comment):
    bundle = InfoBundle(id, stars, date, comment)
    if not name in data:
        GetStudent(name)
    data[name].append(bundle.ToJson())

data = {}
activities = ["root"] + [p.replace("\n", "") for p in open("activities.txt", 'r').readlines()]
Open()
print("-----------")
while True:
    command = input("\nFunc: ")
    parse = command.split(" ")
    func = parse[0]
    if func == "help":
        print("Format: func name id stars date comment")
        print("Example: add armin 5 3 10/14/2020 this is a comment")
        print("You can also automatically get the date")
        print("Example: add armin 5 3 auto this is a comment")
    elif func == "add":
        comment = ""
        for i in range(5, len(parse)):
            comment += parse[i] + " "
        Add(parse[1], parse[2], parse[3], parse[4], comment)
        print()
        Save()
    elif func == "get":
        GetStudent(parse[1])
