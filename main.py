#!/usr/bin/env python3
# ------------------------------------------------------- #
#                       imports                           #
# ------------------------------------------------------- #
import json

from flask import Flask, send_from_directory, render_template, redirect, request

# ------------------------------------------------------- #
#                     module imports                      #
# ------------------------------------------------------- #
import modules.ping_graph as ping_tool

# ------------------------------------------------------- #
#                       variables                         #
# ------------------------------------------------------- #
app = Flask(__name__, template_folder="templates")


# ------------------------------------------------------- #
#                   function definitions                  #
# ------------------------------------------------------- #


def load_index():
    with open("apis.json", "r") as f:
        file = json.load(f)
    return file


@app.route("/", methods=["GET"])
def index():
    file = load_index()
    return render_template("index.html", apis=file)


@app.route("/u/<path:path>", methods=["GET", "POST"])
def ping_graph(path: str):
    file = load_index()
    for i in file:
        if path == i["file"]:
            template = f"{ path }.html"
            try:
                return render_template(template, title=i["name"])
            except Exception as e:
                return render_template("error.html", errorcode=500, errordesc=str(e)), 500
    return render_template("error.html", errorcode=404, errordesc="API not found!"), 404


@app.route("/i/<path:path>", methods=["POST"])
def upload_file(path: str):
    path_handler = {
        "ping_graph": ping_tool.get_ping_data()
    }
    if path in path_handler:
        handler = path_handler[path]
        # print(ping_tool.get_ping_data())
        # return handler()
        link = handler
        print(link)
        return redirect(link)
    return render_template("error.html", errorcode=404, errordesc="API not found!"), 404


@app.route("/graphs/<path:path>", methods=["GET"])
def send_graph(path: str):
    return send_from_directory(ping_tool.GRAPH_FOLDER, path)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', errorcode=404, errordesc="Page not found!"), 404