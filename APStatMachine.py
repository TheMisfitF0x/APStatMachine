# img_viewer.py

import PySimpleGUI as sg
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path
import csv
import re
import tkinter as tk
import matplotlib.pyplot as mpl
import matplotlib

# Log File Parser, rebuilt for the APStatMachine
sentEvents = []
graphsGenerated = False
figure_canvas_agg = None
gameCodeDict = {
    "CL": "Clique",
    "DS": "Dark Souls III",
    "DM": "Doom 1993",
    "FT": "Factorio",
    "HK": "Hollow Knight",
    "KH": "Kingdom Hearts 2",
    "LZ": "Legend of Zelda",
    "MM": "Megaman Battle Network 3",
    "MC": "Minecraft",
    "NA": "Noita",
    "OT": "Ocarina of Time",
    "PE": "Pokemon Emerald",
    "PB": "Pokemon Blue",
    "PR": "Pokemon Red",
    "RT": "Raft",
    "RR": "Risk of Rain 2",
    "SS": "Slay the Spire",
    "SC": "StarCraft 2",
    "SV": "Stardew Valley",
    "SB": "Subnautica",
    "SM": "Super Mario World",
    "TR": "Terraria",
    "WG": "Wargroove"
}


def parseSentEvents(logFilePath):
    global sentEventsDF
    # Open the text file for reading and CSV file for writing (create if not exists)
    with open(logFilePath, 'r') as infile:
        # Event Patterns
        sentPattern = re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: \(Team #\d\) (\w+) sent (.+?) to (\w+)")

        for line in infile:
            # Iterate over the sent events
            match = sentPattern.search(line)
            if match:
                print("Match Found")
                newRow = []
                # Date and Time
                date = match.group(1)
                time = match.group(2)
                dateTime = date + " " + time
                newRow.append(dateTime)

                # Sender
                senderComp = match.group(3)
                sender = senderComp[:-2]
                try:
                    senderGame = gameCodeDict[senderComp[-2:]]
                except:
                    senderGame = senderComp[-2:]

                newRow.append(sender)
                newRow.append(senderGame)

                # Receiver
                receiverComp = match.group(5)
                receiver = receiverComp[:-2]
                try:
                    receiverGame = gameCodeDict[receiverComp[-2:]]
                except:
                    receiverGame = receiverComp[-2:]

                newRow.append(receiver)
                newRow.append(receiverGame)

                # Item
                item = match.group(4)
                print("Sent Match")
                if item.startswith("+"):
                    item = "\'" + item
                    print("Weird starting character found")
                newRow.append(item)
                sentEvents.append(newRow)
    sentEventsDF = pd.DataFrame(
        sentEvents, columns=[
            "Date/Time (UTC)", "Sender", "Sender Game", "Receiver", "Receiver Game", "Item"])
    print(sentEventsDF)


matplotlib.use("TkAgg")


def draw_figures(canvas):
    global graphsGenerated
    global figure_canvas_agg
    print(graphsGenerated)
    if (graphsGenerated == False):
        # Plot the pie chart
        global fig
        global axes
        fig, axGrid = mpl.subplots(2, 2, figsize=(8, 8))
        axes = axGrid.flatten()
        generate_plot_for_ax(0, "Sender")
        generate_plot_for_ax(1, "Sender Game")
        generate_plot_for_ax(2, "Receiver")
        generate_plot_for_ax(3, "Receiver Game")
        graphsGenerated = True
        print(graphsGenerated)
        
    else:
        generate_plot_for_ax(0, "Sender")
        generate_plot_for_ax(1, "Sender Game")
        generate_plot_for_ax(2, "Receiver")
        generate_plot_for_ax(3, "Receiver Game")
        
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)


def generate_plot_for_ax(ax_index, column_name):
    value_counts = sentEventsDF[column_name].value_counts()
    axes[ax_index].pie(value_counts, labels=value_counts.index,
                       autopct='%1.1f%%', startangle=140)
    axes[ax_index].axis('equal')
    axes[ax_index].set_title(f'Pie Chart of {column_name}')


def draw_plot_to_alt_window():
    mpl.show()


# First the window layout in 2 columns. Intend to utilize this still as a framework:
# First column for File Input and stat readout, second column for chart generation.
settings_frame = [
    [sg.Text("Items sent to self:"),
     sg.Radio("Include", "Exlusion-Options"), sg.Radio("Exclude", "Exlusion-Options", True)],
    [sg.Text("By player or by game?"), sg.OptionMenu(
        ["By Player", "By Game"])],
    [sg.Button("Generate", enable_events=True, key="-GENERATE GRAPH-"),
     sg.Button("Push Out", enable_events=True, key="-POP OUT GRAPH-")]
]

paths_and_settings_column = [
    [
        sg.Text("Spoiler Path:"),
        sg.In(size=(25, 1), enable_events=True, key="-SPOILER PATH-"),
        sg.FileBrowse()
    ],
    [
        sg.Text("Log Path:"),
        sg.In(size=(25, 1), enable_events=True, key="-LOG PATH-"),
        sg.FileBrowse()
    ],
    [
        sg.Table(key="-TABLEPREVIEW-", headings=[
                 "Date/Time (UTC)", "Sender", "Sender Game", "Receiver", "Receiver Game", "Item"], values=sentEvents)
    ],
    [
        sg.Frame("Settings", settings_frame)
    ]
]


# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Canvas(key="-CANVAS-")]
]

# ----- Full layout -----
layout = [
    [
        sg.Text("Online or Offline?"),
        sg.Radio("Online", "connectionMode", False, enable_events=True),
        sg.Radio("Offline", "connectionMode", True, enable_events=True)
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Column(paths_and_settings_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Text("Currently, only offline mode is available")
    ]
]

window = sg.Window("AP Statistic Machine", layout, finalize=True)


# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-LOG PATH-":
        parseSentEvents(window["-LOG PATH-"].get())
        window["-TABLEPREVIEW-"].update(values=sentEvents)
    elif event == "-GENERATE GRAPH-":
        if graphsGenerated:
            window["-CANVAS-"].TKCanvas.delete("all")
            draw_figures(window["-CANVAS-"].TKCanvas)
        else:
            draw_figures(window["-CANVAS-"].TKCanvas)
    elif event == "-UPDATE SETTINGS-":
        print("Settings")
    elif event == "-POP OUT GRAPH-":
        draw_plot_to_alt_window()
window.close()
