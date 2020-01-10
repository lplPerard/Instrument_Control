"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Graph. Graph is the superclass for the different figures displayed by the software.

"""

from Parameters import Parameters
from tkinter import LabelFrame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph(Parameters):
    """Class containing the Graph superclass. 

    """

    def __init__(self, root, name):
    #Constructor for the Graph superclass
        Parameters.__init__(self)
        
        self.__initFrame(root, text=name)
        self.__initFigure()

    def __initFrame(self, root, text="", padx=15, pady=15):
    #This method generates the Frame's parameters for the sequence
        self.frame = LabelFrame(root)
        self.frame.configure(text=text, padx=padx, pady=pady, bg=self.bgColor)
        self.frame.grid(column=0, row=0)

    def __initFigure(self):
    #This method creates the canva for the Graph
        self.fig = Figure(figsize=(10, 6), dpi=50, facecolor=self.Graph_bgColor)

        self.plot = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0)
        #self.canvas.get_tk_widget().configure(bg="gainsboro")

    def addGraph(self, x="", y="", xlabel="", ylabel="", title="", xlog=True, ylog=True, grid=True):
    #This method is called to add data to be plotted on self.fig    
        self.plot.step(x,y)
        self.plot.set_xlabel(xlabel)
        self.plot.set_ylabel(ylabel)
        self.plot.grid(grid)

        self.canvas.draw()

    def clearGraph(self):
    #This method is called to clear all data from a Graph
        self.plot.clear()