"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Multilayer Graph.

"""
from Graph import Graph

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
        self.intVar_iteration = IntVar()
        self.intVar_iteration.set(1)

        self.intVar_nbTry = IntVar()
        self.intVar_nbTry.set(1)

    def __initLabels(self):
    #This method creates all Labels widgets for Multilayer Graph
        self.label_iteration = Label(self.frame, text="Iteration : ")
        self.label_iteration.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_iteration.grid(column=0, row=1)

        self.label_nbTry = Label(self.frame, text="nbTry : ")
        self.label_nbTry.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_nbTry.grid(column=2, row=1)

    def __initEntries(self):
    #This method creates all Combobox widget for Multilayer Graph
        self.entry_iteration = Entry(self.frame, textvariable = self.intVar_iteration, state="readonly", width=4)
        self.entry_iteration.grid(column=1, row=1)

        self.entry_nbTry = Entry(self.frame, textvariable = self.intVar_nbTry, state="readonly", width=4)
        self.entry_nbTry.grid(column=3, row=1)

    def setIteration(self, iteration, nbTry):
    #Method to modify combo_iteration values
        self.intVar_iteration.set(iteration)
        self.intVar_nbTry.set(nbTry)
