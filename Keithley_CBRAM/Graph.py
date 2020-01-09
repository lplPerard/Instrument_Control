"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Graph. Graph is the superclass for the different figures displayed by the software.

"""

from Parameters import Parameters

class Graph(Parameters):
    """Class containing the Graph superclass

    """

    def __init__(self):
        #Constructor for the Graph superclass
        Parameters.__init__(self)