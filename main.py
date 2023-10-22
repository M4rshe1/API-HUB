#!/usr/bin/env python3

from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import modules.ping_graph as ping_tool


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/ping-graph", methods=["GET", "POST"])
def ping_graph():
    # if the page is cashed, reload it
    return render_template("ping_graph.html", title="Ping Graph")


@app.route("/res/ping-graph", methods=["POST"])
def upload_file():
    return ping_tool.get_ping_data()


@app.route("/graphs/<path:path>", methods=["GET"])
def send_graph(path: str):
    return send_from_directory(ping_tool.GRAPH_FOLDER, path)