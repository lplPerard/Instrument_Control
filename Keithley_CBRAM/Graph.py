"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Graph. Graph is the superclass for the different figures displayed by the software.

"""

from Controller import Controller
from tkinter import LabelFrame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph():
    """Class containing the Graph superclass. 

    """

    def __init__(self, root, resource, name):
    #Constructor for the Graph superclass
        self.controller = Controller(resource)

        self.resource = resource
        
        self.__initFrame(root, text=name)
        self.__initFigure()

    def __initFrame(self, root, text="", padx=0, pady=0):
    #This method generates the Frame's parameters for the sequence
        self.frame = LabelFrame(root)
        self.frame.configure(text=text, padx=padx, pady=pady, bg=self.resource.bgColor)
        self.frame.grid(column=0, row=0)

    def __initFigure(self):
    #This method creates the canva for the Graph
        self.fig = Figure(figsize=(9, 6), dpi=self.resource.Graph_size, facecolor=self.resource.bgColor)

        self.plot = self.fig.add_subplot(111)
        self.plot.set_facecolor(self.resource.Graph_bgColor)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().configure(bg=self.resource.Graph_bgColor)
        self.canvas.get_tk_widget().grid(column=0, columnspan=10, row=0)
        self.canvas.draw()

    def addGraph(self, x=[], y=[], xlabel="", ylabel="", title="", xscale="linear", yscale='linear', color="blue", grid=True):
    #This method is called to add data to be plotted on self.fig    
        self.plot.step(x,y, color=color)

        self.plot.set_xlabel(xlabel)
        self.plot.set_xscale(xscale)

        self.plot.set_ylabel(ylabel)
        self.plot.set_yscale(yscale)

        self.plot.grid(grid)

        self.canvas.draw()

    def clearGraph(self):
    #This method is called to clear all data from a Graph
        self.plot.clear()

        self.fig.set_facecolor(self.resource.bgColor)
        self.canvas.get_tk_widget().configure(bg=self.resource.bgColor)
        self.plot.set_facecolor(self.resource.Graph_bgColor)