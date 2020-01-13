"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Model.

"""

from Resource import Resource
from Service import Service

from numpy import ones
from numpy import linspace

class Controller(Resource):
    """Class containing the Controller for the CBRAM software

    """

    def __init__(self):
    #Constructor for the Model class
        Resource.__init__(self)

        self.service = Service()

    def generateSingleSequence(self, combo_aimingState, startValue, stopValue, param):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        if combo_aimingState == 0:
            span = stopValue - startValue
            T_max = span / param

            time = linspace(0, T_max, T_max/self.stepDelay)
            signal = param * time - startValue
                              
        elif combo_aimingState == 1:
            span = -abs(stopValue - startValue)
            T_max = param

            time = linspace(0, T_max, T_max/self.stepDelay)
            signal = span * ones(len(time)) + startValue
            
        return(time, signal)