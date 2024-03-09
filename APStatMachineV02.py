# Import Block
import PySimpleGUI as sg
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as mpl
import matplotlib
import statMachComponents as appComps
from logparser import LogParser

# Set MatPlotLib to use the proper backend for PySimpleGUI
matplotlib.use("TkAgg")

# Global vars
# Log Parser
lp = None
# Focus Settings
fs = None
# Focus Figure
ff = None
# Shotgun Figure
sgf = None

# Settings Class
class FocusSettings:
    def __init__(self):
        self.excludeSelfSends = True
        self.column = "Sender"
        pass
    

# Methods


# Initialization of a figure, don't use this repeatedly.
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# Init
window = sg.Window("AP Statistic Machine", appComps.layout, finalize=True)

canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas

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
window.close()
