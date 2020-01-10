"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Parameters. Parameters is the superclass containing all the parameters of the CBRAM software application.
Parameters are stored in a specific configuration file.

"""


class Parameters():
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
        self.stepDelay = 0.011
        self.source = "VOLT"
        self.sense = "CURR"

        self.timeUnit = "s"
        self.voltUnit = "V"
        self.currUnit = "mA"
        self.powerunit = "mW"
        self.resistanceUnit = "Ohm"

        self.Graph_bgColor = "white"
        self.Graph_showCompliance = True

        self.bgColor = "gainsboro"
        self.textColor = "black"