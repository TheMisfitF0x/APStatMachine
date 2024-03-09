# Import Block
import PySimpleGUI as sg
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as mpl
import matplotlib
import statMachComponents as appComps
from logparser import LogParser, EventType

# Set MatPlotLib to use the proper backend for PySimpleGUI
matplotlib.use("TkAgg")

# Global vars, added here for clarity
# Log Parser
lp = None
# Focus Settings
fs = None
# Focus Figure and subplot
ff = None
ffAx = None
# Shotgun Figure and subplots
sgf = None
sgfAxesRaw = None
sgfAxes = None

# Methods


# Initialization of a figure, don't use this repeatedly.
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# Init
# Draw the Window
window = sg.Window("AP Statistic Machine", appComps.layout, finalize=True)

# Collect Canvas References
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas

# Focus graph init
ff = mpl.Figure()
ffAx = ff.add_subplot(111)

# Shotgun graphs init

# Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-LOG PATH-":
        lp = LogParser(window["-LOG PATH-"].get())
        window["-TABLE PREVIEW-"].update(values=lp.GetSentEvents())
    elif event == "-GENERATE GRAPH-":
        pass
    elif event == "-F EXCLUSION":
        fs.UpdateSettings(window["-F EXCLUSION-"].get())
window.close()
