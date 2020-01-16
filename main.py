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

def Remove(name, project):
    ninjas[name].remove(project)

def Fixed(name, project):
    Remove(name, project)
    Add("_fixed_", name + ": " + project)

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
        try:
            args = commandString[1].split(None, 1)
        except IndexError:
            pass
        if commandString[0] == "add":
            if args != None and len(args) == 2:
                ninja = args[0].lstrip()
                project = args[1].lstrip()
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
            if len(args) == 1:
                if args[0] in ninjas:
                    print("Projects to fix: ")
                    for p in ninjas[args[0]]:
                        print("- " + p)
                    print("")
                else:
                    print(args[0] + " not registered.\n")
            else:
                print("Invalid input. Example -> check: emma.m\n")
        elif commandString[0] == "fixed":
            if args != None and len(args) == 2:
                if fg[0] in ninjas:
                    if fg[1] in ninjas[fg[0]]:
                        print("Added to 'fixed'.\n")
                        Fixed(fg[0], fg[1])
                    else:
                        print(fg[0] + " doesn't need to fix '" + fg[1] + "'.\n")
                else:
                    print(fg[0] + " not registered.\n")
            else:
                print("Invalid input. Example -> fixed: emma.m fast food\n")
        elif commandString[0] == "exit":
            print("Clean exit", end = ' ')
            s = WaitForYN("Save?")
            if s == "y":
                Save()
                print("with save.\n")
            else:
                print("without saving.\n")
            ExitProgram()    
    else:
        print("Invalid command -> " + commandString[0])


    if True:
        return
    if not command in commands:
        print("Invalid command")
    else:
        if command == "add":
            f = input("Enter name and project, all lowercase, dash separated (emma.m-hide and seek): ")
            fg = f.split("-")
            try:
                if fg[1] in ninjas[fg[0]]:
                    print("Project already exists.\n")
                else:
                    s = ""
                    while s != "y" and s!= "n":
                        s = input("Add '" + fg[1] + "' to " + fg[0] + "? (y/n): ")
                    if s == "y":
                        Add(fg[0], fg[1])
                        print("Added.\n")
                    else:
                        print("Ignored.\n")
            except IndexError:
                print("Invalid input.\n")
            except KeyError:
                s = ""
                while s != "y" and s!= "n":
                    s = input("Add '" + fg[1] + "' to " + fg[0] + "? (y/n): ")
                if s == "y":
                    Add(fg[0], fg[1])
                    print("Added.\n")
                else:
                    print("Ignored.\n")
        elif command == "check":
            s = input("Enter name: ")
            if s in ninjas:
                print("Projects to fix: ")
                for p in ninjas[s]:
                    print(" - " + p)
                print("")
            else:
                print(s + " not registered.\n")
        elif command == "fixed":
            try:
                f = input("Enter name and project, all lowercase, dash separated (emma.m-hide and seek): ")
                fg = f.split("-")
                if fg[0] in ninjas:
                    if fg[1] in ninjas[fg[0]]:
                        print("Added to 'fixed'.\n")
                        Fixed(fg[0], fg[1])
                    else:
                        print(fg[0] + " doesn't need to fix '" + fg[1] + "'.\n")
                else:
                    print(fg[0] + " not registered.\n")
            except IndexError:
                print("Invalid input.\n")
        elif command == "remove":
            try:
                f = input("Enter name and project, all lowercase, dash separated (emma.m-hide and seek): ")
                fg = f.split("-")
                if fg[0] in ninjas:
                    if fg[1] in ninjas[fg[0]]:
                        print("Removed.\n")
                        Remove(fg[0], fg[1])
                    else:
                        print(fg[0] + " doesn't have '" + fg[1] + "'.\n")
                else:
                    print(fg[0] + " not registered.\n")
            except IndexError:
                print("Invalid input.\n")
        elif command == "grade":
            if "_fixed_" in ninjas:
                print("Fixed projects: ")
                for p in ninjas["_fixed_"]:
                    print(" - " + p)
                print("")
            else:
                print("No fixed projects.\n")
        elif command == "save":
            Save()
            print("Dict saved to JSON.\n")
        elif command == "exit":
            s = ""
            while s != "y" and s!= "n":
                s = input("Save? (y/n): ")
            print("Clean exit", end = ' ')
            if s == "y":
                Save()
                print("with save.\n")
            else:
                print("without saving.\n")
            ExitProgram()
        elif command == "debug_wipe":
            open('data.txt', 'w').close()
            print("JSON file wiped.\n")
        elif command == "debug_clear":
            ninjas.clear()
            print("Program storage wiped.\n")
            

def ExitProgram():
    sys.exit()

# ------------------------------------------------ #

print("\nSystem Active")
ninjas = {}
commands = {
    "add",
    "check",
    "fixed",
    "remove",
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