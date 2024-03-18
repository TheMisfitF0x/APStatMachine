# Import Block
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as mpl
import matplotlib
from statMachComponents import EventType, eventKeys, layout
from logparser import LogParser, EventType
from datahandler import DataHandler
from settings import FSettingName, FocusSettings

# Set MatPlotLib to use the proper backend for PySimpleGUI
matplotlib.use("TkAgg")

# Global vars, added here for clarity
# Log Parser
lp = None
# Data Handler
dh = DataHandler()
# Focus Settings
fs = FocusSettings()
# Focus Figure and subplot
ff = None
ffAx = None
# Shotgun Figure and subplots
sgf = None
sgfAxesRaw = None
sgfAxes = None

# Methods


def GenerateFocusGraph():
    global ffAx
    global ffAgg
    value_counts = dh.ToDataframe(lp.GetEvents(EventType.Sent))[
        fs.column].value_counts()
    ffAx.cla()
    ffAx.pie(value_counts, labels=value_counts.index,
             autopct='%1.1f%%', startangle=140)
    ffAx.axis('equal')
    ffAx.set_title(f'Pie Chart of {fs.column}')
    ffAgg.get_tk_widget().pack(side="top", fill="both", expand=1)
    ffAgg.draw()


def PopOutFocusGraph():
    global ffAx
    global ffAgg
    value_counts = dh.ToDataframe(lp.GetEvents(EventType.Sent))[
        fs.column].value_counts()
    ffAx.cla()
    ffAx.pie(value_counts, labels=value_counts.index,
             autopct='%1.1f%%', startangle=140)
    ffAx.axis('equal')
    ffAx.set_title(f'Pie Chart of {fs.column}')
    ff.show()
    ffAgg.get_tk_widget().pack(side="top", fill="both", expand=1)


# Init
# Draw the Window
window = sg.Window("AP Statistic Machine", layout, finalize=True)

# Collect Canvas References
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas

# Focus graph init
ff = mpl.Figure(figsize=(8, 8))
ffAx = ff.add_subplot(111)
ffAgg = FigureCanvasTkAgg(ff, window["-CANVAS-"].TKCanvas)

# Shotgun graphs init
sgf, sgfAxesRaw = mpl.subplots(2, 2)
sgfAxes = sgfAxesRaw.flatten()

fs = FocusSettings()

# Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == eventKeys["Update"]["Log"]:
        lp = LogParser(window["-LOG PATH-"].get())
        window["-TABLE PREVIEW-"].update(values=lp.GetEvents(EventType.Sent))
    elif event == eventKeys["Generate"]["Shotgun"]:
        pass
    elif event == eventKeys["Generate"]["Focus"]:
        GenerateFocusGraph()
    elif event == eventKeys["Pop"]["Focus"]:
        PopOutFocusGraph()
    elif event == eventKeys["FocusSelfSends"][True]:
        print("Exclude Self Sends")
        fs.UpdateSettings(FSettingName.ExcludeSelfSends, True)
    elif event == eventKeys["FocusSelfSends"][False]:
        print("Do not exclude self sends")
        fs.UpdateSettings(FSettingName.ExcludeSelfSends, False)

window.close()
