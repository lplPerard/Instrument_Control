"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Sequence. Sequence is the superclass for the different test bench.

"""

from Parameters import Parameters
from CBRAM import CBRAM

from tkinter import LabelFrame
from tkinter import Button

class Sequence_view(Parameters):
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self, root):
    #Constructor for the Sequence_view superclass
        Parameters.__init__(self)

        self.state = ""
        self.model = Sequence_model()
        self.frame = LabelFrame(root)
        self.button_startSequence = Button(self.frame, text="Start Sequence", command=self.button_startSequence_callBack)

        self.cell = CBRAM()

        self.Graph = [] #Graph list containing all the figures linked to the test bench

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        print('Not implemented yet')

    def initFrame(self, text="", padx=15, pady=15, bg=""):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=bg)
        self.frame.grid(column=0, row=0)

class Sequence_model(Parameters):
    """Class containing the model for a typical testbench.

    """

    def __init__(self):
    #Constructor for the Sequence_model superclass
        Parameters.__init__(self)
                
        self.signal = []
        self.time = []
        self.compliance = 0

    def generateSequence(self):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        print('NCY')