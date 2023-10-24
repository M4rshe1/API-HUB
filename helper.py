import json
from colorama import Fore, Style
import os

forbidden_names = ["main", "modules", "templates", "config", "helper", "error", "index", "static", "graphs", "logs",
                   "app", "flask", "matplotlib", "numpy", "pandas", "seaborn", "sklearn", "tensorflow", "keras",
                   "venv", ]

forbidden_names_create = forbidden_names.copy()


def create_api():
    api = {"name": "", "description": "", "file": "", "author": "", "docs": "", "author_link": "", "visible": 1}

    print("This script will help you create a new API for the webserver.")

    print("The settings can be changed later in the config.json file.")
    print(Fore.RED + "WARNING: " + Style.RESET_ALL + "This script will overwrite files if they already exist!")

    print("\n\n")

    api["name"] = input("Name of the API: ")
    if api["name"] in forbidden_names_create:
        print("This name is already taken!")
        return
    api["description"] = input("Description of the API: ")
    api["file"] = api["name"].replace(" ", "_").lower()
    api["author"] = input("Author of the API: ")
    api["docs"] = input("Documentation link of the API: ")
    api["author_link"] = input("Link to the author of the API: ")

    with open(f"modules/{api['file']}.py", "w") as f:
        f.write(f"# Path: modules/{api['file']}\n")
        f.write(f"# Author: {api['author']}\n")
        f.write(f"# Description: {api['description']}\n")
        f.write(f"# Docs: {api['docs']}\n")
        f.write(f"# Author Link: {api['author_link']}\n")
        f.write(f"# ------------------------------------------------------- #\n")
        f.write(f"#                       imports                           #\n")
        f.write(f"# ------------------------------------------------------- #\n")
        f.write(f"import modules.logger as logger\n")
        f.write(f"import modules.config as config\n")

        f.write(f"# ------------------------------------------------------- #\n")
        f.write(f"#                       variables                         #\n")
        f.write(f"# ------------------------------------------------------- #\n")
        f.write(f"LOGGING_HEADER = '[{api['file'].upper()}]'\n")
        f.write(f"LOGGING = config.load_config('config.json')['settings']['log']\n")
        f.write(f"LOGGING_LVL = config.load_config('config.json')['settings']['log_lvl']\n")
        f.write(f"# ------------------------------------------------------- #\n")
        f.write(f"#                   function definitions                  #\n")
        f.write(f"# ------------------------------------------------------- #\n")
        f.write(f"\n")
        f.write(f"\n")
        f.write("# From here on you can start coding your API.\n")
        f.write("# The function start_point() will be called when the API is loaded.\n")
        f.write("# The relative path to the API is /u/" + api["file"] + "\n")
        f.write(f"def start_point():\n")
        f.write(f"    logger.log(f'Loading api {api['file']}...', LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=1)\n")
        f.write(f"    return\n")

    with open(f"templates/{api['file']}.html", "w") as f:
        with open("templates/template.html", "r") as template:
            f.write(template.read())

    with open("config.json", "r") as f:
        config_file = json.load(f)
        config_file["apis"].append(api)
        with open("config.json", "w") as f:
            json.dump(config_file, f, indent=4)

    with open("main.py", "r") as f:
        # update the path_handler dict in main.py
        lines = f.readlines()
        for i in range(len(lines)):
            if "path_handler = {" in lines[i]:
                print("Found path_handler dict!")
                lines[i] += f"        \"{api['file']}\": md.{api['file']}.start_point(),\n"
                break
        with open("main.py", "w") as f:
            f.writelines(lines)

    for i in os.listdir("modules"):
        if i == f"{api['file']}.py":
            print("Found module file!")
            os.remove(f"modules/{api['file']}.py")
            break

    for i in os.listdir("templates"):
        if i == f"{api['file']}.html":
            print("Found template file!")
            os.remove(f"templates/{api['file']}.html")
            break


def create_run_file():
    files = {"name": "", "show": "", "description": "", "link": "", "author": "", "docs": "", "author_link": "",
             "visible": 1, "command": ""}
    print("This script will help you create a new file for the webserver.")
    print("The settings can be changed later in the config.json file.")

    print("\n\n")

    files["show"] = input("Name of the RUN File: ")
    if files["show"] in forbidden_names_create:
        print("This name is already taken!")
        return
    files["name"] = files["show"].replace(" ", "_").lower()
    files["description"] = input("Description of the file: ")
    files["link"] = input("Link to the file: ")
    files["author"] = input("Author of the file: ")
    files["author_link"] = input("Link to the author of the file: ")
    files["docs"] = input("Documentation link of the file: ")
    files["command"] = f"irm api.heggli.dev/{files['name']} | iex"

    with open(f"config.json", "r") as f:
        config_file = json.load(f)
        config_file["files"].append(files)
        with open("config.json", "w") as f:
            json.dump(config_file, f, indent=4)

    with (open("run.ps1", "r") as f):
        lines = f.readlines()
        for i in range(len(lines)):
            if f"Switch ($select)" in lines[i]:
                name = files["name"]
                lines[i + 1] = f"{'{'}" + '\n  (\"' + files["show"] + '\") ' + (f"{'{'}" +
                f"\nWrite-Host 'Starting {files['show']}...'\nirm api.heggli.dev/{name} | iex\n" + f"{'}'}\n")

        for i in range(len(lines)):
            if lines[i].startswith("#"):
                lines[i] = "Write-Host '    " + files["show"] + " as [" + files["name"] + " ]'\n" + lines[i]
                break

        with open("run.ps1", "w") as f:
            f.writelines(lines)


def del_api():
    name = input("Name of the API like (ping_graph): ")
    if name == "":
        return
    if name in forbidden_names:
        print("You can't delete this file!")
        return
    with open("config.json", "r") as f:
        config_file = json.load(f)
        for i in config_file["apis"]:
            if i["file"] == name:
                config_file["apis"].remove(i)
                with open("config.json", "w") as f:
                    json.dump(config_file, f, indent=4)
                break

    with open("main.py", "r") as f:
        # update the path_handler dict in main.py
        lines = f.readlines()
        for i in range(len(lines)):
            if f"\"{name}\": md.{name}.start_point()," in lines[i]:
                print("Found path_handler dict!")
                lines[i] = ""
                break
        with open("main.py", "w") as f:
            f.writelines(lines)


def del_run_file():
    name = input("Name of the file like (ping_tool): ")
    if name == "":
        return
    if name in forbidden_names:
        print("You can't delete this file!")
        return
    with open("config.json", "r") as f:
        config_file = json.load(f)
        for i in config_file["files"]:
            if i["name"] == name:
                config_file["files"].remove(i)
                with open("config.json", "w") as f:
                    json.dump(config_file, f, indent=4)
                break

    with open("run.ps1", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if f" as [{name}]" in lines[i]:
                print("Found run file!")
                lines[i] = ""
                break

        for i in range(len(lines)):
            if f"(\"{name}\")" in lines[i]:
                print("Found run file!")
                lines[i] = ""
                lines[i + 1] = ""
                lines[i + 2] = ""
                lines[i + 3] = ""
                break
        with open("run.ps1", "w") as f:
            f.writelines(lines)


def visible_run_file():
    name = input("Name of the file like (ping_tool): ")
    if name == "":
        return
    with open("config.json", "r") as f:
        config_file = json.load(f)
        for i in config_file["files"]:
            if i["name"] == name:
                if i["visible"] == 1:
                    i["visible"] = 0
                else:
                    i["visible"] = 1
                with open("config.json", "w") as f:
                    json.dump(config_file, f, indent=4)
                break


def visible_api():
    name = input("Name of the API like (ping_graph): ")
    if name == "":
        return
    with open("config.json", "r") as f:
        config_file = json.load(f)
        for i in config_file["apis"]:
            if i["file"] == name:
                if i["visible"] == 1:
                    i["visible"] = 0
                else:
                    i["visible"] = 1
                with open("config.json", "w") as f:
                    json.dump(config_file, f, indent=4)
                break


if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)
    for i in config["apis"]:
        forbidden_names_create.append(i["name"])
        forbidden_names_create.append(i["file"])
    for i in config["files"]:
        forbidden_names_create.append(i["show"])
        forbidden_names_create.append(i["name"])

    print("What do you want to do?")
    print("   Create a new API------------------[1]")
    print("   Delete an API---------------------[2]")
    print("   Create a new Run file-------------[3]")
    print("   Delete a Run file-----------------[4]")
    print("   Toggle visibility of an API-------[5]")
    print("   Toggle visibility of a run file---[6]")

    choice = input("Choice: ")
    if choice == "1":
        create_api()
    elif choice == "2":
        del_api()
    elif choice == "3":
        create_run_file()
    elif choice == "4":
        del_run_file()
    elif choice == "5":
        visible_api()
    elif choice == "6":
        visible_run_file()
