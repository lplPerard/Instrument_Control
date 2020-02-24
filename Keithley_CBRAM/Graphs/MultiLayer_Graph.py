"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
File description : Class container for Multilayer Graph.

"""
from Graphs.Graph import Graph

from tkinter import IntVar
from tkinter import Label
from tkinter import Entry
from tkinter.ttk import Combobox

from numpy import linspace

class Multilayer_Graph(Graph):
    """Class containing a multilayer Graph.

    """

    def __init__(self, frame, resource, name):
    #Constructor for the Multilayer_Graph class
        Graph.__init__(self, frame, resource, name)

        self.__initVars()
        self.__initLabels()
        self.__initEntries()

    def __initVars(self):
        self.intVar_iterationFrom = IntVar()
        self.intVar_iterationFrom.set(1)

        self.intVar_iterationTo = IntVar()
        self.intVar_iterationTo.set(1)

    def __initLabels(self):
    #This method creates all Labels widgets for Multilayer Graph
        self.label_iterationFrom = Label(self.frame, text="Iteration from : ")
        self.label_iterationFrom.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_iterationFrom.grid(column=0, row=1)

        self.label_iterationTo = Label(self.frame, text="Iteration to : ")
        self.label_iterationTo.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_iterationTo.grid(column=2, row=1)

    def __initEntries(self):
    #This method creates all Combobox widget for Multilayer Graph
        self.entry_iterationFrom = Entry(self.frame, textvariable = self.intVar_iterationFrom, state="readonly", width=4)
        self.entry_iterationFrom.grid(column=1, row=1)

        self.entry_iterationTo = Entry(self.frame, textvariable = self.intVar_iterationTo, state="readonly", width=4)
        self.entry_iterationTo.grid(column=3, row=1)

    def setIteration(self, iterationFrom, iterationTo):
    #Method to modify combo_iteration values
        self.intVar_iterationFrom.set(iterationFrom)
        self.intVar_iterationTo.set(iterationTo)
