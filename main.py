import sys
import json
from json.decoder import JSONDecodeError

def Add(name, project):
    if not name in ninjas:
        ninjas[name] = []
    ninjas[name].append(project)

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
        pass

def IssueCommand(command):
    if not command in commands:
        print("Invalid command")
    else:
        if command == "add":
            f = input("Enter name and project: ")
            fg = f.split(",")
            Add(fg[0], fg[1])
        elif command == "exit":
            s = ""
            while s != "y" and s!= "n":
                s = input("Save? (y/n): ")
            print("Clean exit.\n")
            ExitProgram(s)
        elif command == "debug_wipe":
            open('data.txt', 'w').close()
            print("JSON file wiped.\n")
        elif command == "debug_clear":
            ninjas.clear()
            print("Program storage wiped.\n")
            

def ExitProgram(s):
    if s == "y":
        Save()
    sys.exit()

# ------------------------------------------------ #

print("\nSystem Active")
ninjas = {}
commands = {
    "add",
    "save",
    "debug_wipe",
    "debug_clear",
    "exit"
}

running = True
Open()
print("JSON loaded.\n")

while(running):
    command = input("Enter command: ")
    IssueCommand(command)
    





