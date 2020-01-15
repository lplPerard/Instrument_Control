"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Parameters. Parameters is the superclass containing all the parameters of the CBRAM software application.
Parameters are stored in a specific configuration file.

"""


class Resource():
    """Superclass containing all the application's general parameters. Every class inherit this superclass. 
    Attributes :

    - Machine Parameters
        - Communication protocol
        - Adress
        - Step delay
        - NPLC
        - Delay
        - Resistance measurement method
        - Source
        - Sense
        - Units

    - Display parameters
        - Background color
        - Texts size

    - Export parameters
        - Include date
        - Include time

    - Graph parameters
        - Display Current Compliance on graph
        - Display grid

    - Sequence specific parameters

    """

    def __init__(self):
    #Constructor for the Parameters superclass

        #SMUParameters
        self.stepDelay = 0.0093
        self.NPLC= 0.01
        self.source = "VOLT"
        self.sense = "CURR"

        #generalParameters
        self.deviceAdress = ""
        self.bgColor = "gainsboro"
        self.textColor = "black"
        self.timeCoeff = 1
        self.voltCoeff = 1
        self.currCoeff = 1e-3
        self.powerCoeff = 1e-3
        self.resistanceCoeff = 1

        #graphParameters
        self.Graph_bgColor = "black"
        self.Graph_grid = True
        self.Graph_compliance = True
        self.Graph_size = 60

        #Non editable parameters

        self.pady=2
        self.padx=5
