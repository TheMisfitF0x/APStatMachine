# img_viewer.py

import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path
import csv
import re
import matplotlib.pyplot

# Log File Parser, rebuilt for the APStatMachine
sentEvents = []


def parseLogFile(logFilePath):
    # Open the text file for reading and CSV file for writing (create if not exists)
    currentRow = 0
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


fig = matplotlib.pyplot.Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

matplotlib.use("TkAgg")


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Code to Game Dictionary, may not be required for future, but leaving it in for now as a just in case.
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
    "TR": "Terraria",
    "WG": "Wargroove"
}

# First the window layout in 2 columns. Intend to utilize this still as a framework:
# First column for File Input and stat readout, second column for chart generation.

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

draw_figure(window["-CANVAS-"].TKCanvas, fig)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-LOG PATH-":
        parseLogFile(window["-LOG PATH-"].get())
        window["-TABLEPREVIEW-"].update(values=sentEvents)


window.close()
