"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Multilayer Graph.

"""
from Graph import Graph

from tkinter import Label
from tkinter.ttk import Combobox

class Multilayer_Graph(Graph):
    """Class containing a multilayer Graph.

    """

    def __init__(self, frame, resource, name):
    #Constructor for the Multilayer_Graph class
        Graph.__init__(self, frame, resource, name)

        self.__initLabels()
        self.__initCombobox()

    def __initLabels(self):
    #This method creates all Labels widgets for Multilayer Graph
        self.label_iteration = Label(self.frame, text="Iteration : ")
        self.label_iteration.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_iteration.grid(column=0, row=1)

        self.label_nbTry = Label(self.frame, text="nbTry : ")
        self.label_nbTry.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_nbTry.grid(column=2, row=1)

    def __initCombobox(self):
    #This method creates all Combobox widget for Multilayer Graph
        self.combo_iteration = Combobox(self.frame, state="readonly", values=[])
        self.combo_iteration.bind("<<ComboboxSelected>>", self.combo_iteration_callback)
        self.combo_iteration.configure(background=self.resource.bgColor)
        self.combo_iteration.grid(column=1, row=1)

    def combo_iteration_callback(self):
    #Callback method for combo_iteration
        print('bla')

    def setIteration(self, iteration):
    #Method to modify combo_iteration values
        self.combo_iteration.configure(values=iteration)
