# Import Block
import PySimpleGUI as sg
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as mpl
import matplotlib
import statMachComponents as ac
from logparser import LogParser, EventType
import datahandler as dh
from settings import FSettingName, FocusSettings

# Set MatPlotLib to use the proper backend for PySimpleGUI
matplotlib.use("TkAgg")

# Global vars, added here for clarity
# Log Parser
lp = None
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
    value_counts = 

# Initialization of a figure, don't use this repeatedly.
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# Init
# Draw the Window
window = sg.Window("AP Statistic Machine", ac.layout, finalize=True)

# Collect Canvas References
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas

# Focus graph init
ff = mpl.Figure()
ffAx = ff.add_subplot(111)
ffAgg = FigureCanvasTkAgg(ff, window["-CANVAS-"].TKCanvas)

# Shotgun graphs init
sgf, sgfAxesRaw = mpl.subplots(2,2)
sgfAxes = sgfAxesRaw.flatten()

fs = FocusSettings()

# Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == ac.eventKeys["Update"]["Log"]:
        lp = LogParser(window["-LOG PATH-"].get())
        dh = DataHandler()
        window[ac.eventKeys["Table"]].update(values=lp.GetEvents(EventType.Sent))
    elif event == ac.eventKeys["Generate"]["Shotgun"]:
        pass
    elif event == ac.eventKeys["FocusSelfSends"][True]:
        print("Exclude Self Sends")
        fs.UpdateSettings(FSettingName.ExcludeSelfSends, True)
    elif event == ac.eventKeys["FocusSelfSends"][False]:
        print("Do not exclude self sends")
        fs.UpdateSettings(FSettingName.ExcludeSelfSends, False)
        
window.close()
