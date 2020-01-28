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
            temp = json.load(jsonFile)
            for where in temp:
                for who in temp[where]:
                    for what in temp[where][who]:
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
            print(" - " + p)
    else:
        print("Ninja has no projects added.")
    if who in data["notes"]:
        print("Notes: ")
        for p in data["notes"][who]:
            print(" - " + p)
    else:
        print("Ninja has no notes added.")
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
                    print("Project not in " + who + "'s '" + where + "'.")
        else:
            print("'what' is undefined.")
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
            elif com == "queue":
                print("Projects in queue:")
                for n in data["todo"]:
                    for p in data["todo"][n]:
                        print(" - " + n + ": " + p)
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
                na = None
                nb = None
                nc = None
                a = 0
                b = 0
                c = 0
                t = 0
                for who in data["projects"]:
                    for what in data["projects"][who]:
                        num += 1
                        t += 1
                    if t > a:
                        c = b
                        nc = nb
                        b = a
                        nb = na
                        a = t
                        na = who
                    elif t > b:
                        c = b
                        nc = nb
                        b = t
                        nb = who
                    elif t > c:
                        c = t
                        nc = who
                    t = 0
                print("Number of projects to fix: " + str(num))
                print(" - " + na + " has the most with " + str(a))
                print(" - " + nb + " has the second most with " + str(b))
                print(" - " + nc + " has the third most with " + str(c))
                num = 0
                for who in data["todo"]:
                    for what in data["todo"][who]:
                        num += 1
                print("Number of projects to grade: " + str(num))
            elif com == "who":
                for i in sorted(data["projects"].keys()):
                    print(i)
            elif com == "commands":
                group = [3, 4, 4, 2, 2, 2]
                g = 0
                i = 0
                for c in commands:
                    print(" - " + c)
                    g += 1
                    if g == group[i]:
                        g = 0
                        i += 1
                        print("")
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
                        a = data["todo"][who][-1]
                        Remove("todo", who, a)
                else:
                    Remove("todo", who, what)
            elif com == "note":
                Add("notes", who, what)
            elif com == "unnote":
                if who != None and what != None:
                    if what == "all":
                        while len(data["notes"][who]) > 0:
                            a = data["notes"][who][-1]
                            Remove("notes", who, a)
                    else:
                        Remove("notes", who, what)
                else:
                    print("Invalid.")
            else:
                print("'" + com + "' doesn't use args.")
    else:
        print("Command not recognized.")
    

# - - - - - MAIN - - - - - #
data = {}
data["projects"] = {}
data["notes"] = {}
data["todo"] = {}

commands = [
    "save",
    "open",
    "exit",

    "check",
    "queue",
    "stats",
    "who",

    "add",
    "remove",
    "fix",
    "grade",

    "note",
    "unnote",

    "dict",
    "json",

    "commands"
]

print("\nVersion 0.3.3 active.")
Open()
while(True):
    command = input("\nEnter command: ")
    IssueCommand(command)