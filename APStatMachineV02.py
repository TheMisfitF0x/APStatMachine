# Import Block
import PySimpleGUI as sg
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as mpl
import matplotlib
import statMachComponents as appComps
import logparser as lp

# Set MatPlotLib to use the proper backend for PySimpleGUI
matplotlib.use("TkAgg")



# Global 2D arrays for events generated by the parser
sentEvents = []
hintEvents = []
gameCompletedEvents = []

# Methods


# Initialization of a figure, don't use this repeatedly.
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg




# Init
window = sg.Window("AP Statistic Machine", appComps.layout, finalize=True)

# Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
window.close()
