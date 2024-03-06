# Import Block
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
import demo

# Set MatPlotLib to use the proper backend for PySimpleGUI
matplotlib.use("TkAgg")

# Global Vars
# Game Code Dictionary for LogParser (may also be used for lazy typing)
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

# Global 2D arrays for events generated by the parser
sentEvents = []
hintEvents = []
gameCompletedEvents = []

# Methods


def parseEvents(logFilePath, type="Sent"):
    global sentEventsDF
    global sentEvents
    # Open the text file for reading and CSV file for writing (create if not exists)
    with open(logFilePath, 'r') as infile:
        # Event Patterns
        sentPattern = re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: \(Team #\d\) (\w+) sent (.+?) to (\w+)")

        # Hint Pattern (not currently in use)
        hintPattern = re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: Notice \(Team #1\): \[Hint\]: (\w+)'s (.+?) is at (.+?) in (\w+)'s World\.")

        # To become a 2D Array, convertable into a dataframe.
        sentEvents = []

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

# Initialization of a figure, don't use this repeatedly.


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# Layouts (using notation from PySimpleGui)

# Settings for the shotgun of four pie charts that show items sent/received by player or game.
shotgun_graphs_settings = [
    [sg.Text("Items sent to self:"),
     sg.Radio("Include", "SG-Exlusion-Options"), sg.Radio("Exclude", "SG-Exlusion-Options", True)],
    [sg.Button("Generate", enable_events=True, key="-GENERATE SHOTGUN-"),
     sg.Button("Push Out", enable_events=True, key="-POP OUT SHOTGUN-")]
]

focus_graph_settings = [
    [sg.Text("Items sent to self:"),
     sg.Radio("Include", "F-Exlusion-Options"), sg.Radio("Exclude", "F-Exlusion-Options", True)],
    [sg.Button("Generate", enable_events=True, key="-GENERATE FOCUS-"),
     sg.Button("Push Out", enable_events=True, key="-POP OUT FOCUS-")]
]

paths_and_settings_column = [
    [
        sg.Text("Spoiler Path:"),
        sg.In(size=(25, 1), enable_events=True,
              key="-SPOILER PATH-", default_text="Optional"),
        sg.FileBrowse()
    ],
    [
        sg.Text("Log Path:"),
        sg.In(size=(25, 1), enable_events=True,
              key="-LOG PATH-", default_text="Required"),
        sg.FileBrowse()
    ],
    [  # Thinking of moving this into a tab view sort of system...
        sg.Table(key="-TABLE PREVIEW-", headings=[
                 "Date/Time (UTC)", "Sender", "Sender Game", "Receiver", "Receiver Game", "Item"], values=sentEvents)
    ],
    [
        sg.Frame("Shotgun Pies View Settings", shotgun_graphs_settings),
        sg.Frame("Focus Graph Settings", focus_graph_settings)
    ]
]


# For now will only show the name of the file that was chosen
canvas_column = [
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
        sg.Column(canvas_column),
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Text("Currently, only offline mode is available")
    ]
]

# Init
window = sg.Window("AP Statistic Machine", layout, finalize=True)

# Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
window.close()