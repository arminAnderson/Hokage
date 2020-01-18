import sys
import json
from json.decoder import JSONDecodeError

def WaitForYN(message):
    s = ""
    while s != "y" and s!= "n":
        s = input(message + " (y/n): ")
    return s
    
def Add(name, project):
    if not name in ninjas:
        ninjas[name] = []
    ninjas[name].append(project)

def AddNote(name, note):
    if not name in notes:
        notes[name] = []
    notes[name].append(note)

def Remove(name, project):
    ninjas[name].remove(project)

def RemoveNote(name, noteNum):
    del notes[name][noteNum]

def RemoveAllNotes():
    del notes.clear()

def Fixed(name, project):
    Remove(name, project)
    Add("_todo_", name + ": " + project)

def Save():
    with open('data.txt', 'w') as outfile:
        json.dump(ninjas, outfile, indent=4)

def Open():
    try:
        with open('data.txt') as jsonFile:
            data = json.load(jsonFile)
            for n in data:
                for p in data[n]:
                    Add(n, p)
    except JSONDecodeError:
        print("Error reading file.\n")

def IssueCommand(command):
    commandString = command.split(":")
    if commandString[0] in commands:
        args = None
        ninja = None
        project = None
        try:
            args = commandString[1].split(None, 1)
            ninja = args[0].lstrip()
            project = args[1].lstrip()
        except IndexError:
            pass
        if commandString[0] == "add":
            if args != None and len(args) == 2:
                if ninja in ninjas and project in ninjas[ninja]:
                    print("Project already added.\n")
                else:
                    s = WaitForYN("Add '" + project + "' to " + ninja + "?")
                    if s == "y":
                        Add(ninja, project)
                        print("Added.\n")
                    else:
                        print("Ignored.\n")   
            else:
                print("Invalid input. Example -> add: emma.m fast food\n")
        elif commandString[0] == "check":
            if args != None and len(args) == 1:
                if ninja in ninjas:
                    print("Projects to fix: ")
                    for p in ninjas[ninja]:
                        print("- " + p)
                    print("")
                else:
                    print(ninja + " not registered.\n")
            else:
                print("Invalid input. Example -> check: emma.m\n")
        elif commandString[0] == "fix":
            if (args != None and len(args) == 2):
                if ninja in ninjas:
                    if project == "all":
                        while len(ninjas[ninja]) > 0:
                            a = ninjas[ninja][-1]
                            Fixed(ninja, a)
                            print(ninja + "'s '" + a + "' added to 'todo'.")
                        print("")
                    else:
                        if project in ninjas[ninja]:
                            print("Added to 'todo'.\n")
                            Fixed(ninja, project)
                        else:
                            print(ninja + " doesn't need to fix '" + project + "'.\n")
                else:
                    print(ninja + " not registered.\n")
            else:
                print("Invalid input. Example -> fix: emma.m fast food")
                print("          Can also use -> fix: emma.m all\n")
        elif commandString[0] == "todo":
            if args == None:
                if "_todo_" in ninjas:
                    print("Projects to update: ")
                    for p in ninjas["_todo_"]:
                        print(" - " + p)
                    print("")
                else:
                    print("No projects to update.\n")
            else:
                print("Invalid input, do not include args\n")
        elif commandString[0] == "grade":
            if "_todo_" in ninjas:
                if args != None and (len(args) == 2 or (len(args) == 1 and args[0] == "all")):
                    if len(args) == 1:
                        while len(ninjas["_todo_"]) > 0:
                            a = ninjas["_todo_"][-1]
                            Remove("_todo_", a)
                            print("'" + a + "' graded.")
                        print("")
                    else:
                        if project == "all":
                            i = 0
                            while i < len(ninjas["_todo_"]):
                                s = ninjas["_todo_"][i].split(":")[0]
                                if s == ninja:
                                    print("Graded '" + ninjas["_todo_"][i] + "'")
                                    del ninjas["_todo_"][i]
                                else:
                                    i += 1
                            print("")
                        else:
                            s = ninja + ": " + project
                            if s in ninjas["_todo_"]:
                                Remove("_todo_", s)
                                print("Project graded.\n")
                            else:
                                print("Project not queued\n")
                else:
                    print("Invalid input. Example -> grade: emma.m fast food")
                    print("          Can also use -> grade: emma.m all")
                    print("          Can also use -> grade: all/n")
            else:
                print("No projects queued up.\n")
        elif commandString[0] == "remove":   
            if args != None and len(args) == 2:
                if project == "all":
                    while len(ninjas[ninja]) > 0:
                        a = ninjas[ninja][-1]
                        Remove(ninja, a)
                        print("Removed " + ninja + "'s " + a + ".")
                    print("")
                else:
                    if ninja in ninjas:
                        if project in ninjas[ninja]:
                            print("Removed '" + project + "'.\n")
                            Remove(ninja, project)
                        else:
                            print(ninja + " doesn't need to fix '" + project + "'.\n")
                    else:
                        print(ninja + " not registered.\n")
            else:
                print("Invalid input. Example -> remove: emma.m fast food")
                print("          Can also use -> remove: emma.m all\n")
        elif commandString[0] == "save":   
            if args == None:
                Save()
                print("Dict saved to JSON.\n")
            else:
                print("Invalid input, do not include args\n")
        elif commandString[0] == "exit":
            if args == None:
                s = WaitForYN("Save?")
                print("Clean exit", end = ' ')
                if s == "y":
                    Save()
                    print("with save.\n")
                else:
                    print("without saving.\n")
                ExitProgram()    
            else:
                print("Invalid input, do not include args\n")
        elif commandString[0] == "addNote":
            pass
        elif commandString[0] == "debug_wipe":
            if args == None:
                open('data.txt', 'w').close()
                print("JSON file wiped.\n")
            else:
                print("Invalid input, do not include args\n")
        elif commandString[0] == "debug_clear":
            if args == None:
                ninjas.clear()
                print("Program storage wiped.\n")
            else:
                print("Invalid input, do not include args\n")
    else:
        print("Invalid command -> " + commandString[0] + "\n")
            

def ExitProgram():
    sys.exit()

# ------------------------------------------------ #

print("\nSystem Active")
ninjas = {}
notes = {}
commands = {
    "add",
    "addNote"
    "check",
    "fix",
    "remove",
    "todo",
    "grade",
    "save",
    "exit",
    "debug_wipe",
    "debug_clear"
}

running = True
Open()
print("JSON loaded.\n")

while(running):
    command = input("Enter command: ")
    IssueCommand(command)