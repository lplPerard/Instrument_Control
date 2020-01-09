"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Sequence. Sequence is the superclass for the different test bench.

"""

from Graph import Graph
from Parameters import Parameters

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
        self.Graph = [] #Graph list containing all the figures linked to the test bench

class Sequence_model():
    """Class containing the GUI for the CBRAM software according to the MCV model.

    """

    def __init__(self):
    #Constructor for the Sequence_model superclass
        print('bla')
