"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
File description : Class container for Graph. Graph is the superclass for the different figures displayed by the software.

"""

from Controller import Controller

from tkinter import filedialog
from tkinter import LabelFrame
from tkinter import Button

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
        
        self.button_saveGraph = Button(self.frame, text="Save Graph", command=self.button_saveGraph_callBack, padx=5, pady=10)
        self.button_saveGraph.grid(column=4, columnspan=2, row=1, padx=self.resource.padx, pady=self.resource.pady)

    def button_saveGraph_callBack(self):
    #Callback method for button saveJPG
        path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("all files","*.*"), (".jpg file","*.jpg"), (".png file","*.png"), (".pdf file","*.pdf")))
        if path != "":
            File = open(path, 'wb')
            self.fig.savefig(path)

            File.close()

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
        self.canvas.get_tk_widget().grid(column=0, columnspan=5, row=0)
        self.canvas.draw()

    def addStepGraph(self, x=[], y=[], xlabel="", ylabel="", title="", xscale="linear", yscale='linear', color="blue", grid=True, marker_pos=[]):
    #This method is called to add data to be plotted on self.fig    
        self.plot.step(x, y, '-gD', color=color, markevery=marker_pos, markerfacecolor="green", markeredgecolor="black")

        self.plot.set_xlabel(xlabel)
        self.plot.set_xscale(xscale)

        self.plot.set_ylabel(ylabel)
        self.plot.set_yscale(yscale)

        self.plot.grid(grid)

        self.canvas.draw()
        
    def addLinGraph(self, x=[], y=[], xlabel="", ylabel="", title="", xscale="linear", yscale='linear', color="blue", grid=True, marker_pos=[]):
    #This method is called to add data to be plotted on self.fig    
        self.plot.plot(x, y, '-gD', color=color, markevery=marker_pos, markerfacecolor="green", markeredgecolor="black")

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