#!/usr/bin/python3
# ------------------------------------------------------- #
#                   import statements                     #
# ------------------------------------------------------- #

import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from flask import redirect, request, render_template, send_from_directory
from matplotlib import gridspec

# ------------------------------------------------------- #
#                   global variables                      #
# ------------------------------------------------------- #

# Set the folder where graphs will be stored
GRAPH_FOLDER = "graphs"
ALLOWED_EXTENSIONS = {'json'}
KeepJSON = False
ImageExpire = 60 * 60 * 24
LOGGING_HEADER = "[PING_GRAPH]"


# LOGGING_LVL = config_load_config("config.json")["settings"]["log_lvl"]


# Check if the graph folder exists, and create it if not


# ------------------------------------------------------- #
#                   function definitions                  #
# ------------------------------------------------------- #

def gen_graph(data: list, file_path: str, settings: dict) -> None:
    # print(data)
    global ax2
    start_time = datetime.strptime(data[0]["starttime"], "%Y.%m.%d %H:%M:%S")
    end_time = datetime.strptime(data[-1]["endtime"], "%Y.%m.%d %H:%M:%S")
    time_diff = end_time - start_time

    table_data = {}
    tmp_times = []

    for i in data:
        tmp_times += i["times"]

    table_data["Start -> End"] = str(datetime.utcfromtimestamp(time_diff.total_seconds()).strftime('%H:%M:%S'))
    table_data["Start Time"] = data[0]["starttime"]
    table_data["End Time"] = data[-1]["endtime"]
    table_data["Min"] = min(tmp_times)
    table_data["Max"] = max(tmp_times)
    table_data["Avg"] = sum(tmp_times) / len(tmp_times)
    table_data["Device"] = data[0]["device"]

    # Create the main figure with gridspec to arrange the graph and table
    fig = plt.figure(figsize=(10, 10))  # Increase the figure size
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])  # Adjust the height ratio
    ax1 = plt.subplot(gs[0])  # Subplot for the graph

    if settings.get("show_table") is None:
        ax2 = plt.subplot(gs[1])  # Subplot for the table
    # ax2.set_visible(False)

    # Adjust the spacing between the subplots to make more room for the table
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    # Create a dictionary to store colors for each request name
    request_colors = {}
    plotted_names = set()
    count = 0
    for entry in data:
        count += 1
        timestamps = entry["timestamps"]
        times = entry["times"]
        request_name = f"Request {count}"  # Use the request name

        # Assign a color for this request if it doesn't already have one
        if request_name not in request_colors:
            request_colors[request_name] = plt.cm.jet(len(request_colors) / len(data))

        # Set the color based on the request name
        color = request_colors[request_name]

        # Plot the data points with the same request name and connect them with lines
        for i in range(len(timestamps) - 1):
            if times[i] != 0:
                marker = 'o'
                if times[i] < 25:
                    f_color = "limegreen"
                elif times[i] < 60:
                    f_color = "yellow"
                else:
                    f_color = "red"
                ax1.plot(timestamps[i:i + 2], times[i:i + 2], linestyle='-', markersize=6,
                         markerfacecolor=f_color, markeredgecolor=f_color, markeredgewidth=1, marker=marker,
                         color=color)
            else:
                marker = 'X'
                f_color = 'red'
                ax1.plot(timestamps[i:i + 2], times[i:i + 2], linestyle='-', markersize=8,
                         markerfacecolor=f_color, markeredgecolor=f_color, markeredgewidth=1, marker=marker,
                         color=color)

        # Add text labels for times next to the markers
        if (settings is not None and settings.get("show_times", "false") == "true" or
                settings.get("show_times") == "on"):
            for timestamp, time in zip(timestamps, times):
                ax1.text(timestamp, time, str(time), ha='left', va='bottom', color=color)

        # Add legend only once for each unique request name
        if request_name not in plotted_names:
            ax1.plot([], [], linestyle='-', label=request_name, color=color)
            plotted_names.add(request_name)

    # Set labels and legend for the graph
    ax1.set_xlabel('Timestamp (seconds)')
    ax1.set_ylabel('Ping Time (ms)')
    ax1.set_title('Ping Results')
    ax1.legend()
    ax1.grid()

    if settings.get("show_table") is None:
        # # Create a table on the second subplot (ax2)
        table_data = list(table_data.items())  # Convert the data to a list
        table = ax2.table(cellText=table_data, loc='bottom', cellLoc='left', colWidths=[0.2, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.2)
        ax2.axis('off')

        for i in range(len(table_data)):
            cell = table.get_celld()[(i, 0)]
            cell.set_facecolor('lightgray')


    plt.savefig(file_path, format="png")
    plt.close(fig)


def start_point():
    if request.method == "POST":
        # logger.log(f"Generating graph...", LOGGING_LVL, LOGGING_HEADER, True, lvl=1)
        print("wefwefwef")
        print(request.files['file'])
        print("wefwefwef")

        try:
            if not os.path.exists(GRAPH_FOLDER):
                os.makedirs(GRAPH_FOLDER)
            # convert request to string and print it
            # print(request.form.to_dict())

            if 'file' not in request.files:
                # logger.log(f"Error generating graph! No file part", LOGGING_LVL, LOGGING_HEADER, True, lvl=3)
                return "No file part", 400

            # read body of request
            print(request.data)

            # Get the file from the request
            file = request.files['file']
            # Check if the file is empty
            if file.filename == '':
                return "No selected file", 400
            # Read the JSON data from the file
            json_data = json.loads(file.read().decode('utf-8-sig'))

            # print(json_data)

            filename = f"ping_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            # logger.log(f"Saving JSON file to {GRAPH_FOLDER}/{filename}.json", LOGGING_LVL, LOGGING_HEADER, True, lvl=1)
            # Save the file to the GRAPH_FOLDER
            file.save(os.path.join(GRAPH_FOLDER, filename + ".json"))
            # Get the settings from the request
            settings = request.form.to_dict()
            if file:
                # Generate a graph and save it to the GRAPH_FOLDER
                gen_graph(
                    json_data,
                    os.path.join(GRAPH_FOLDER, filename + ".png"),
                    settings
                )

                # Provide a download link for the generated graph
                graph_link = f"/{GRAPH_FOLDER}/{filename}.png"
                # logger.log(f"Graph generated! {graph_link}", LOGGING_LVL, LOGGING_HEADER, True, lvl=1)

                # redirect to the graph
                clean_up(filename=filename)
                return send_from_directory(GRAPH_FOLDER, filename + ".png", as_attachment=True)

        except Exception as e:
            # print(e)
            # logger.log(f"Error generating graph! {e}", LOGGING_LVL, LOGGING_HEADER, True, lvl=3)
            return render_template("error.html", errorcode=405, errordesc="Methode not allowed"), 405
    else:
        return redirect("/")


def clean_up(filename: str):
    # logger.log(f"Cleaning up files...", LOGGING_LVL, LOGGING_HEADER, True, lvl=1)
    try:
        if not KeepJSON:
            # logger.log(f"Removing JSON file...", 0, LOGGING_HEADER, True, lvl=1)
            os.remove(os.path.join(GRAPH_FOLDER, filename + ".json"))

        for file in os.listdir(GRAPH_FOLDER):
            if os.path.getmtime(os.path.join(GRAPH_FOLDER, file)) < datetime.now().timestamp() - ImageExpire:
                # logger.log(f"Removing old image file... {GRAPH_FOLDER + '/' + file}", LOGGING_LVL,
                #            LOGGING_HEADER, True, lvl=1)
                os.remove(os.path.join(GRAPH_FOLDER, file))
    except Exception as e:
        # logger.log(f"Error cleaning up files! {e}", LOGGING_LVL, LOGGING_HEADER, True, lvl=3)
        exit(1)
    return


if __name__ == '__main__':
    print("This is a module for API_HUB.")
