import sys
import json
from json.decoder import JSONDecodeError

# - - - - - UTIL - - - - - #
def WaitForYN(message):
    s = ""
    while s != "y" and s!= "n":
        s = input(message + " (y/n): ")
    return s

def Save():
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print("JSON saved to file.\n")

def Open():
    try:
        with open('data.txt') as jsonFile:
            data = json.load(jsonFile)
            for where in data:
                for who in data[where]:
                    for what in data[where][who]:
                        Add(where, who, what)
    except JSONDecodeError:
        print("Error reading file.\n")

def Add(where, who, what):
    if where == "projects" or where == "notes":
        if not who in data[where]:
            data[where][who] = []
        elif not what in data[where][who]
            data[where][who].append(what)
    else:
        print("Undefined dict.\n")

def Exit():
    sys.exit()

# - - - - - COMMAND - - - - - #
def IssueCommand(command):
    commandString = command.split(":")
    if commandString[0] in commands:
        args = None
        who = None
        what = None
        try:
            args = commandString[1].split(None, 1)
            who = args[0].lstrip()
            what = args[1].lstrip()
        except IndexError:
            pass
        if commandString[0] == "save":
            Save()
        elif commandString[0] == "open":
            Open()
        elif commandString[0] == "exit": 
            Exit()    
        elif commandString[0] == "add":
            if args != None:
                if len(args) == 2:
                    Add("projects", who, what)
                elif len(args) == 1 and args[0] == "bulk": 
                    while True:
                        a = input("add -> ")
                        if a == "done":
                            break
                        else:
                            try:
                                args = a.split(None, 1)
                                who = args[0].lstrip()
                                what = args[1].lstrip()
                                if args != None and len(args) == 2:
                                    Add("projects", who, what)   
                            except IndexError:
                                print("Invalid.\n")
            else:    
                print("Invalid input.\n")
        elif commandString[0] == "note":
            if args != None and len(args) == 2:
                Add("notes", who, what)
            else:
                print("Invalid input.\n")
    else:
        print("Command not recognized.\n")

# - - - - - MAIN - - - - - #
data = {}
data["projects"] = {}
data["notes"] = {}

commands = {
    "save",
    "open",
    "exit",
    "add",
    "note"
}

Open()
print("\nJSON loaded.\n")

while(True):
    command = input("Enter command: ")
    IssueCommand(command)