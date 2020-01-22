import sys
import json
from json.decoder import JSONDecodeError

# - - - - - UTIL - - - - - #
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
            data = json.load(jsonFile)
            for where in data:
                for who in data[where]:
                    for what in data[where][who]:
                        Add(where, who, what)
        print("JSON loaded.")
    except JSONDecodeError:
        print("Error reading file.")
def Add(where, who, what):
    if where != None and who != None and what != None:
        if not who in data[where]:
            data[where][who] = []
        if not what in data[where][who]:
            data[where][who].append(what)
        else:
            pass
    else:
        print("Missing argument.")
def Check(who):
    if who in data["projects"]:
        print("Projects to fix: ")
        for p in data["projects"][who]:
            print("- " + p)
    else:
        print("Ninja has no projects added.")
    if who in data["notes"]:
        print("Notes: ")
        for p in data["notes"][who]:
            print("- " + p)
    else:
        print("Ninja has no notes added.")
def Remove(where, who, what):
    if who in data[where]:
        if what in data[where][who]:
            data[where][who].remove(what)
        else:
            print("Project not in " + who + "'s '" + where + "'.")
    else:
        print("Ninja not found.")
def Exit():
    s = WaitForYN("Save?")
    print("Program terminated",end=", ")
    if s == "y":
        Save()
    else:
        print("without saving.")
    print("")
    sys.exit()

# - - - - - COMMAND - - - - - #
def IssueCommand(command):
    commandString = command.split(":")
    com = commandString[0]
    if com in commands:
        args = None
        who = None
        what = None
        try:
            args = commandString[1].split(None, 1)
            who = args[0].lstrip()
            what = args[1].lstrip()
        except IndexError:
            pass
        if args == None:
            if com == "save":
                Save()
            elif com == "open":
                Open()
            elif com == "exit": 
                Exit()    
            elif com == "add":
                s = None
                while True:
                    s = input("add -> ")
                    if s == "done":
                        break
                    IssueCommand("add:" + s)
                print("Finished.")
            elif com == "grade":
                pass
            else:
                print("'" + com + "' requires args.")
        else:
            if com == "add":
                Add("projects", who, what)
            elif com == "check":
                Check(who)
            elif com == "remove":
                if what == "all" and who in data["projects"]:
                    while len(data["projects"][who]) > 0:
                        a = data["projects"][who][-1]
                        Remove("projects", who, a)
                else:
                    Remove("projects", who, what)
            elif com == "fixed":
                if who in data["projects"]:
                    if what == "all":
                        for p in data["projects"][who]:
                            Add("todo", who, p)
                        IssueCommand("remove:" + who + " all")
                    elif what in data["projects"][who]:
                        Add("todo", who, what)
                        Remove("projects", who, what)
                    else:
                        print("Project not added to " + who + ".")
                else:
                    print("Ninja not found.")
            elif com == "grade":
                if what == "all" and who in data["todo"]:
                    while len(data["todo"][who]) > 0:
                        a = data["todo"][who][-1]
                        Remove("todo", who, a)
                else:
                    Remove("todo", who, what)
            elif com == "note":
                Add("notes", who, what)
            elif com == "unnote":
                if what != None:
                    if what == "all":
                        while len(data["notes"][who]) > 0:
                            a = data["notes"][who][-1]
                            Remove("notes", who, a)
                    else:
                        if int(what) >= 0 and int(what) < len(data["notes"][who]):
                            Remove("notes", who, data["notes"][who][int(what)])
                        else:
                            print("Note out of bounds.")
            else:
                print("'" + com + " doesn't use args.")
    else:
        print("Command not recognized.")
    

# - - - - - MAIN - - - - - #
data = {}
data["projects"] = {}
data["notes"] = {}
data["todo"] = {}

commands = {
    "save",
    "open",
    "exit",
    "add",
    "check",
    "remove",
    "fixed",
    "grade",
    "note",
    "unnote"
}

print("\nVersion 0.1.0 active.")
Open()
while(True):
    command = input("\nEnter command: ")
    IssueCommand(command)