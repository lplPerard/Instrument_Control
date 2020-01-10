"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for CBRAM. CBRAM is a class containing data about the cell under test. It also contains an ampiric model of a CBRAM behavior

"""


class CBRAM():
    """Class containing data about the cell under test.
    Attributes :

    - Identifier
    - State (binary)
    - State (Resistance)

    """

    def __init__(self):
    #Constructor for the CBRAM class

        self.ident = ""
        self.currentState = ""
        self.currentResistance = 0
        