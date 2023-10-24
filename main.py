#!/usr/bin/env python3
# ------------------------------------------------------- #
#                       imports                           #
# ------------------------------------------------------- #
from flask import Flask, render_template, redirect

# ------------------------------------------------------- #
#                     module imports                      #
# ------------------------------------------------------- #
from modules import *


# ------------------------------------------------------- #
#                       variables                         #
# ------------------------------------------------------- #
app = Flask(__name__, template_folder="templates")
LOGGING_HEADER = "[MAIN]"
LOGGING = config_load_config("config.json")["settings"]["log"]  # 1 or 0
LOGGING_LVL = config_load_config("config.json")["settings"]["log_lvl"]  # DEBUG = 0, INFO = 1, WARNING = 2, ERROR = 3, CRITICAL = 4
logging_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
# logger.log(f"Setting Logging to {bool(LOGGING)} with level "
#            f"{logging_levels[config_load_config('config.json')['settings']['log_lvl']]}", 1,
#            LOGGING_HEADER, LOGGING, lvl=1)


# ------------------------------------------------------- #
#                   function definitions                  #
# ------------------------------------------------------- #


@app.route("/", methods=["GET"])
def index():
    file = config_load_config("config.json")
    # logger.log("Loading index page...", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=1)
    return render_template("index.html", apis=file["apis"], files=file["files"])


@app.route("/u/<path:path>", methods=["GET"])
def ping_graph(path: str):
    # logger.log(f"Loading api UI using GET methode with path: /u/{path}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=1)
    for i in config_load_config("config.json")["apis"]:
        if path == i["file"]:
            template = f"{path}.html"
            try:
                return render_template(template, title=i["name"])
            except Exception as e:
                # logger.log(f"Error loading template! {e}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=3)
                return render_template("error.html", errorcode=500, errordesc=str(e)), 500
    return render_template("error.html", errorcode=404, errordesc="API not found!"), 404


@app.route("/i/<path:path>", methods=["POST"])
def upload_file(path: str):
    # logger.log(f"Loading api UI using POST methode with path: /i/{path}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=1)
    path_handler = {
        "ping_graph": ping_graph_start
    }
    if path in path_handler:
        handler = path_handler[path]
        result = handler()
        return result
    # logger.log(f"No UI for api found. path: {path}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=1)
    return render_template("error.html", errorcode=404, errordesc="API not found!"), 404


# @app.route("/graphs/<path:path>", methods=["GET"])
# def send_graph(path: str):
#     # logger.log(f"Loading graph via GET with path: /graph/{path}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=0)
#     return send_from_directory(PING_GRAPH_GRAPH_FOLDER, path)


@app.route("/<path:path>", methods=["GET"])
def send_ps1(path: str):
    # logger.log(f"Loading ps1 via GET with path: /{path}", LOGGING_LVL, LOGGING_HEADER, LOGGING, lvl=0)
    for i in config_load_config("config.json")["files"]:
        if path == i["name"]:
            return redirect(i["link"])
    return render_template("error.html", errorcode=404, errordesc="RUN file not found!"), 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', errorcode=404, errordesc="Page not found!"), 404


if __name__ == '__main__':
    print("This is a module, not a script!")