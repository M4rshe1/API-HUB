import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import gridspec


# Set the folder where graphs will be stored
GRAPH_FOLDER = "graphs"
ALLOWED_EXTENSIONS = {'json'}
# Check if the graph folder exists, and create it if not
if not os.path.exists(GRAPH_FOLDER):
    os.makedirs(GRAPH_FOLDER)


def gen_graph(data: list, file_path: str, settings: dict) -> None:

    print(settings)
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

    if (settings.get("show_table") is not None and settings.get("show_table") == "true" or
            settings.get("show_table") == "on"):
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
                         markerfacecolor=f_color, markeredgecolor=f_color, markeredgewidth=1, marker=marker, color=color)
            else:
                marker = 'X'
                f_color = 'red'
                ax1.plot(timestamps[i:i + 2], times[i:i + 2], linestyle='-', markersize=8,
                         markerfacecolor=f_color, markeredgecolor=f_color, markeredgewidth=1, marker=marker, color=color)

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
    if (settings.get("show_table") is not None and settings.get("show_table") == "true" or
            settings.get("show_table") == "on"):
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


if __name__ == '__main__':
    print("This is a module for API_HUB.")