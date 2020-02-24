"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for Histogram Graph.

"""
from Graph import Graph

from tkinter import IntVar
from tkinter import Label
from tkinter import Entry
from tkinter.ttk import Combobox

class Histogram_Graph(Graph):
    """Class containing a multilayer Graph.

    """

    def __init__(self, frame, resource, name):
    #Constructor for the Multilayer_Graph class
        Graph.__init__(self, frame, resource, name)

    def addGraph(self, x=[], bins='auto', xlabel="", ylabel="", xscale="linear", yscale='linear', title="", color="blue", grid=True):
    #This method is called to add data to be plotted on self.fig    
        self.plot.hist(x, bins=bins, color=color)

        self.plot.set_xlabel(xlabel)
        self.plot.set_xscale(xscale)

        self.plot.set_ylabel(ylabel)
        self.plot.set_yscale(yscale)

        self.plot.grid(grid)

        self.canvas.draw()