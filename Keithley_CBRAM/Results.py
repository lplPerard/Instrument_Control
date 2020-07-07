"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for Results. Results is a class containing data coming back from the measurement device.

"""

class Results():
    """Class containing data coming back from the SMU.

    """

    def __init__(self):
    #Constructor for the Results class

        #SMU parameters

        self.source = "VOLT"
        self.sense = "CURR"
        self.stepDelay = 0.0093
        self.NPLC= 0.01

        # Display parameters

        self.voltCoeff = 1
        self.currCoeff = 1e-3
        self.powerCoeff = 1e-3
        self.resistanceCoeff = 1

        # Cycling parameters
        
        self.R_low_lim = 1e2
        self.R_high_lim = 1e3
        self.nbTry_max = 5

        self.ramp_start_value = 0
        self.ramp_stop_value = 0
        self.ramp_param = 0
        self.ramp_compliance = 0

        self.pulse_start_value = 0
        self.pulse_stop_value = 0
        self.pulse_param = 0
        self.pulse_compliance = 0

        self.cell_ident = ""
        self.cell_resistance = 0

        self.iteration = 0
        self.nbTry = []
        self.signal_1_type = "Pulse"
        self.signal_1 = []
        self.signal_2_type = "Pulse"
        self.signal_2 = []
        self.resistance = []

        # Stability parameters

        self.delay = []
        self.duration = "15mn"
        self.measurementType = "Linear"
        self.measurementMethod = "positive"
