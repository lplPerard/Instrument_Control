"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

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
        self.SMUAdress = ""
        self.stepDelay = 0.0116
        self.NPLC= 0.01
        self.source = "VOLT"
        self.sense = "CURR"

        #RLCParameters
        self.RLCAdress = ""

        #generalParameters
        self.bgColor = "gainsboro"
        self.textColor = "black"

        self.timeCoeff = 1
        self.voltCoeff = 1
        self.currCoeff = 1e-3
        self.powerCoeff = 1e-3
        self.resistanceCoeff = 1

        self.autoExport = False
        self.mailNotification = False
        self.mailTo = "luc.perard@lcis.grenoble-inp.fr"
        self.exportPath = 'C:\\Users\\perardl\\Desktop\\OneDrive\\Resultats\\CBRAM'

        #graphParameters
        self.Graph_bgColor = "white"
        self.Graph_grid = True
        self.Graph_compliance = True
        self.Graph_size = 65

        #Sequence parameters
        self.R_low_lim = 100
        self.R_high_lim = 1000
        self.nbTry = 25

        #Non editable parameters
        self.pady=4
        self.padx=4
        self.state="SINGLE"
