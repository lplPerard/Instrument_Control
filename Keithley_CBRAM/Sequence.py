"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Sequence. Sequence is the superclass for the different test bench.

"""

from Controller import Controller
from Service import Service
from Results import Results

from tkinter import LabelFrame
from tkinter import Button

class Sequence():
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self, root, resource):
    #Constructor for the Sequence_view superclass
        self.state = ""
        self.signal = []
        self.time = []
        self.compliance = 0
        self.results = Results()

        self.resource = resource
        self.controller = Controller(resource)
        self.service = Service(resource)

        self.frame = LabelFrame(root)
        self.button_startSequence = Button(self.frame, text="Start Sequence", command=self.button_startSequence_callBack, padx=5, pady=10)
        self.button_actualizeSequence = Button(self.frame, text="Actualize Sequence", command=self.button_actualizeSequence_callBack, padx=5, pady=10)
        self.button_measureResistance = Button(self.frame, text="Measure", command=self.button_measureResistance_callBack, padx=5, pady=10)
        self.Graph = [] #Graph list containing all the figures linked to the test bench

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        print('Not implemented yet')

    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        print('Not implemented yet')

    def button_measureResistance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        print('Not implemented yet')

    def initFrame(self, text="",column=0, columnspan=1, row=0, rowspan=1, padx=15, pady=15, bg=""):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=bg)
        self.frame.grid(column=column, columnspan=columnspan, row=row, rowspan=rowspan)
        
    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.frame.grid_forget()
