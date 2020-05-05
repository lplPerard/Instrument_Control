"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for the CBRAM Modelling. Modelling sequence is made to extract physical parameters from previous test results. It is based on a numerical
model developped by YU at Stanford University.

"""

class CBRAM ():
    """Class containing the CBRAM model parameters.

    """

    def __init__(self):
    #Constructor for the CBRAM class
        self.nafion_th = 1e-6
        self.Cu_th = 35e-6
        self.Al_th = 1e-6
        self.ext_radius = 1e-3
        self.CF_radius = 33e-9

        self.velocity_h = 0.35
        self.velocity_r = 7
        self.temperature = 300
        self.thermal_resistance = 1e5
        self.alpha = 2.4
        self.beta = 70

        self.resistivity_on = 4e-7
        self.resistivity_off = 3e8