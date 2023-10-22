#!/usr/bin/env python3

from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import json
import os
from datetime import datetime
import modules.ping_graph as ping_tool


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/ping-graph", methods=["GET", "POST"])
def ping_graph():
    # if the page is cashed, reload it
    return render_template("ping_graph.html")


@app.route("/res/ping-graph", methods=["POST"])
def upload_file():
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                return "No file part", 400

            # Get the file from the request
            file = request.files['file']

            # Check if the file is empty
            if file.filename == '':
                return "No selected file", 400

            # Read the JSON data from the file
            json_data = json.loads(file.read().decode('utf-8-sig'))

            filename = f"ping_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

            # Save the file to the GRAPH_FOLDER
            file.save(os.path.join(ping_tool.GRAPH_FOLDER, filename + ".json"))

            # Get the settings from the request
            settings = request.form.to_dict()
            if file:
                # Generate a graph and save it to the GRAPH_FOLDER
                ping_tool.gen_graph(
                    json_data,
                    os.path.join(ping_tool.GRAPH_FOLDER, filename + ".png"),
                    settings
                )

                # Provide a download link for the generated graph
                graph_link = f"/graphs/{filename}.png"

                # redirect to the graph
                return redirect(graph_link)

        except Exception as e:
            return "<strong>Error: </strong>" + str(e)
    else:
        return "GET request received at /api/ping-graph"


@app.route("/graphs/<path:path>", methods=["GET"])
def send_graph(path: str):
    return send_from_directory(ping_tool.GRAPH_FOLDER, path)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6969)
