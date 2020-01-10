"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Sequence. Sequence is the superclass for the different test bench.

"""

from Graph import Graph
from Parameters import Parameters
from CBRAM import CBRAM

from tkinter import LabelFrame

class Sequence_view(Parameters):
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self, root):
    #Constructor for the Sequence_view superclass
        Parameters.__init__(self)

        self.state = ""
        self.model = Sequence_model()
        self.frame = LabelFrame(root)

        self.cell = CBRAM()

        self.Graph = [] #Graph list containing all the figures linked to the test bench

    def initFrame(self, text="", padx=15, pady=15, bg=""):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=bg)
        self.frame.grid(column=0, row=0)

class Sequence_model():
    """Class containing the model for a typical testbench.

    """

    def __init__(self):
    #Constructor for the Sequence_model superclass
        print('bla1')
