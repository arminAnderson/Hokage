import sys
import json
import os
import subprocess
from datetime import date
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
            temp = json.load(jsonFile)
            for where in temp:
                for who in temp[where]:
                    if where == "points":
                        Points(who, temp[where][who])
                    else:
                        for what in temp[where][who]:
                            Add(where, who, what)
        print("JSON loaded.")
    except JSONDecodeError:
        print("Error reading file.")
def Add(where, who, what):
    if where == "":
        where = None
    if who == "":
        who = None
    if what == "":
        what = None
    if where != None and who != None and what != None:
        if not who in data[where]:
            data[where][who] = []
        if not what in data[where][who]:
            data[where][who].append(what)
        return 1
    else:
        print("Missing argument.")
        return 0
def Points(who, what):
    if who == "":
        who = None
    if what == "":
        what = None
    if who == None or what == None:
        print("Missing argument.")
        return 0
    else:
        try:
            num = int(what)
            old = 0
            try:
                old = int(data["points"][who])
            except KeyError:
                data["points"][who] = 0
            data["points"][who] = old + num
            return 1
        except ValueError:
            print("Missing argument.")
            return 0
def Check(who):
    if who != None:
        if who in data["projects"]:
            print(str(len(data["projects"][who])) + " projects to fix:")
            for p in data["projects"][who]:
                print(" - " + p)
        else:
            print("No projects.")
        if who in data["notes"]:
            print("Notes:")
            for p in data["notes"][who]:
                print(" - " + p)
        else:
            print("No notes.")
        if who in data["points"]:
            print(str(data["points"][who]) + " points.")
        else:
            print("No points.")
    else:
        s = {}
        for who in data["projects"]:
            if len(data["projects"][who]) > 0:
                s[who] = len(data["projects"][who])
        for t in sorted(s, key = s.get, reverse = True):
            print(t + " has " + str(s[t]) + " projects to fix:")
            for p in data["projects"][t]:
                print(" - " + p)
            print("-----------------------------")
def Remove(where, who, what):
    if who in data[where]:
        if what != None:
            try:
                if int(what) >= 0 and int(what) < len(data[where][who]):
                    data[where][who].remove(data[where][who][int(what)])
                else:
                    print("Out of bounds.")
            except ValueError:
                if what in data[where][who]:
                    data[where][who].remove(what)
                else:
                    print("'" + what + "' not in " + who + "'s " + where + ".")
        else:
            print("'what' is undefined.")
    else:
        if where == "projects":
            print("No projects found.")
        elif where == "notes":
            print("No notes found.")
def SignIn():
    user = ""
    while user == "":
        user = input("Enter username: ")
    if Git(user, " in ") == 1:
        return 1
    Open()
    return 0
def Git(user, _in):
    print("Pulling repo...")
    out = None
    try:
        out = subprocess.check_output('git pull', shell=True)
        out = out.decode("utf-8")
    except subprocess.CalledProcessError:
        s = WaitForYN("\nStop trying to be fancy. Discard local changes?")
        if s == "y":
            os.system('git reset --hard origin/master')
            print("\n", end="")
        else:   
            print("Exiting safely. Contact Armin.")
        return 1
    if out.find("main.py") != -1:
        print("Old version detected. System exiting without saving. Try again.\n")
        return 1
    print("Verifying integrity...")
    out = subprocess.check_output('git status', shell=True)
    out = out.decode("utf-8")
    if out.find("lock.txt") != -1 and _in == " in ":
        print("Don't edit 'lock.txt', dumbass.\n")
        return 1
    with open('lock.txt') as lock:
        t = lock.readline().strip()
        if not t == "":
            os.system('git reset --hard origin/master')
            print("\n", end="")
            print(t + " is signed in. System exiting without saving.\n")
            return 1
    if _in != " out ":
        with open('lock.txt', 'w') as lock:
            lock.write(user)
    print("Pushing to repo...")
    os.system('git add -A')
    os.system('git commit -m "log' + _in + user + ' | ' + str(date.today()) + '"')
    try:
        out = subprocess.check_output('git push', shell=True)
    except subprocess.CalledProcessError:
        os.system('git reset --hard origin/master')
        print("\n", end="")
        print("Simultaneous logins detected. System exiting without saving.\n")
        sys.exit()
    return 0
def Exit():
    t = None
    with open('lock.txt') as lock:
        t = lock.readline().strip()
    open('lock.txt', 'w').close()
    s = WaitForYN("Save?")
    print("Program terminated",end=", ")
    if s == "y":
        Save()
    else:
        print("without saving.")
    Git(t, " out ")
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
            who = args[0].rstrip()
            if who == "":
                who = None
            what = args[1].lstrip()
            what = args[1].rstrip()
            if what == "":
                what = None
        except IndexError:
            if who == None and what == None:
                args = None
        if args == None:
            if com == "exit": 
                Exit()    
            elif com == "add":
                s = None
                while True:
                    s = input("add | ")
                    if s == "done":
                        break
                    IssueCommand("add:" + s)
                print("Finished.")
            elif com == "points":
                s = None
                while True:
                    s = input("points | ")
                    if s == "done":
                        break
                    IssueCommand("points:" + s)
                print("Finished.")
            elif com == "score":
                for p in sorted(data["points"].values()):
                    print(p + p.key)
            elif com == "check":
                Check(None)
            elif com == "queue":
                if len(data["todo"]) > 0:
                    print("Projects in queue:")
                    for n in data["todo"]:
                        for p in data["todo"][n]:
                            print(" - " + n + ": " + p)
                else:
                    print("No projects to grade.")
            elif com == "grade":
                s = WaitForYN("Are you sure you want to clear the whole grade queue?")
                if s == "y":
                    for n in data["todo"]:
                        while len(data["todo"][n]) > 0:
                            Remove("todo", n, 0)
                    print("Cleared.")
                else:
                    print("Cancelled.")
            elif com == "dict":
                print(json.dumps(data, sort_keys=False, indent=4))
            elif com == "json":
                try:
                    with open('data.txt') as jsonFile:
                        temp = json.load(jsonFile)
                        print(json.dumps(temp, sort_keys=False, indent=4))
                except JSONDecodeError:
                    print("Error printing.")
            elif com == "stats":
                num = 0
                for who in data["projects"]:
                    for what in data["projects"][who]:
                        num += 1
                print("Number of projects to fix: " + str(num))          
                num = 0      
                for who in data["todo"]:
                    for what in data["todo"][who]:
                        num += 1
                print("Number of projects to grade: " + str(num))
            elif com == "who":
                for i in sorted(data["projects"].keys()):
                    if len(data["projects"][i]) > 0:
                        print(i)
            elif com == "info":
                for c in info:
                    print(" - " + c)
            else:
                print("'" + com + "' requires args.")
        else:
            if com == "add":
                if what != None and what.find('#') != -1:
                    parts = what.split("#")
                    parts[0] = parts[0].lstrip()
                    parts[0] = parts[0].rstrip()
                    parts[1] = parts[1].lstrip()
                    parts[1] = parts[1].rstrip()
                    Add("projects", who, parts[0])
                    if parts[0] != "" and parts[1] != "":
                        Add("notes", who, parts[0] + " | " + parts[1])
                else:
                    if what == None:
                        s = None
                        while True:
                            s = input("add for " + who + " | ")
                            s.strip()
                            if s == "done" or s == "":
                                break
                            IssueCommand("add: " + who + " " + s)
                        print("Finished.")
                    else:
                        Add("projects", who, what)
            elif com == "check":
                Check(who)
            elif com == "points":
                if Points(who, what) == 1:
                    print("Now has " + str(data["points"][who]) + " points.")
            elif com == "wipe":
                IssueCommand("remove:" + who + " all")
                IssueCommand("unnote:" + who + " all")
            elif com == "remove":
                if what == "all" and who in data["projects"]:
                    while len(data["projects"][who]) > 0:
                        Remove("projects", who, 0)
                else:
                    Remove("projects", who, what)
            elif com == "fix":
                if who in data["projects"]:
                    if what != None:
                        if what == "all":
                            for p in data["projects"][who]:
                                Add("todo", who, p)
                            IssueCommand("remove:" + who + " all")
                        else:
                            try:
                                if int(what) >= 0 and int(what) < len(data["projects"][who]):
                                    Add("todo", who, data["projects"][who][int(what)])
                                    Remove("projects", who, what)
                                else:
                                    print("Out of bounds.")
                            except ValueError:
                                if what in data["projects"][who]:
                                    Add("todo", who, what)
                                    Remove("projects", who, what)
                                else:
                                    print("Project not added to " + who + ".")
                    else:
                        print("Invalid")
                else:
                    print("Ninja not found.")
            elif com == "grade":
                if what == "all" and who in data["todo"]:
                    while len(data["todo"][who]) > 0:
                        Remove("todo", who, 0)
                else:
                    Remove("todo", who, what)
            elif com == "note":
                Add("notes", who, what)
            elif com == "unnote":
                if what == "all" and who in data["notes"]:
                    while len(data["notes"][who]) > 0:
                        Remove("notes", who, 0)
                else:
                    Remove("notes", who, what)
            else:
                print("'" + com + "' doesn't use args.")
    else:
        print("Command not recognized.")
    

# - - - - - MAIN - - - - - #
data = {}
data["projects"] = {}
data["notes"] = {}
data["todo"] = {}
data["points"] = {}

commands = [
    #"save",
    #"open",
    "exit",

    "check",
    "queue",
    "stats",
    "who",

    "add",
    "remove",
    "wipe",
    "fix",
    "grade",
    "points",
    "score",

    "note",
    "unnote",

    #"dict",
    #"json",

    "info"
]

info = [
    #"save",
    #"open",
    "\nexit\n",

    "check",
    "check: name",
    "queue",
    "stats",
    "who\n",

    "add",
    "add: name",
    "add: name project",
    "add: name project # note",
    "remove: name project",
    "remove: name project index",
    "remove: name all",
    "wipe: name",
    "fix: name project",
    "fix: name project index",
    "fix: name all",
    "grade",
    "grade: name project",
    "grade: name project index",
    "grade: name all",
    "points",
    "points: name value",
    "score",

    "note: name note",
    "unnote: name note",
    "unnote: name note index",
    "unnote: name all\n",

    #"dict",
    #"json\n",

    "info"
]

print("\nVersion 0.1.0 active.\n")
f = SignIn()
if f == 0:
    while(True):
        command = input("\nEnter command: ")
        IssueCommand(command)