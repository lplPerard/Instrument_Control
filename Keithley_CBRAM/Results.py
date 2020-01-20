"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Results. Results is a class containing data coming back from the SMU.

"""
from CBRAM import CBRAM

class Results():
    """Class containing data coming back from the SMU.

    """

    def __init__(self):
    #Constructor for the CBRAM class

        self.iteration = 0
        self.nbTry = []
        self.signal_1 = []
        self.signal_2 = []
        self.resistance = []
        self.cell = CBRAM()