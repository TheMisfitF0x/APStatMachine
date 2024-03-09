import PySimpleGUI as sg

# Global Vars
# Game Code Dictionary for LogParser (may also be used for lazy typing)
gameCodes = {
    "CL": "Clique",
    "DS": "Dark Souls III",
    "DM": "Doom 1993",
    "FT": "Factorio",
    "HK": "Hollow Knight",
    "IN": "Inscryption",
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
     sg.Radio("Include", "F-Exlusion-Options", key = "-F EX UPDATE-"), sg.Radio("Exclude", "F-Exlusion-Options", True, key = "-F EX UPDATE-")],
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
                 "Date/Time (UTC)", "Sender", "Sender Game", "Receiver", "Receiver Game", "Item"], values=[])
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
