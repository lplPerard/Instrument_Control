"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Parameters. Parameters is the superclass containing all the parameters of the CBRAM software application.

"""


class Parameters():
    """Superclass containing all the application's general parameters. Every class inherit this superclass.
    Attributes :

    - Step delay
    - Background color
    - Resistance measurement method
    - Export parameters
        - Include date
        - Include time
    - Graph parameters
        - Display Current Compliance on graph
        - Display grid

    """

    def __init__(self):
        #Constructor for the Graph superclass
        self.stepDelay = 0.011
        self.bgColor = "gainsboro"