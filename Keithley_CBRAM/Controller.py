"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Model.

"""

from tkinter import filedialog

from numpy import ones
from numpy import linspace

import pickle

class Controller():
    """Class containing the Controller for the CBRAM software

    """

    def __init__(self, resource):
    #Constructor for the Model class
        self.resource = resource

    def generateSingleSequence(self, combo_aimingState, startValue, stopValue, param):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        if combo_aimingState == 0:
            span = stopValue - startValue
            T_max = span / param

            time = linspace(0, T_max, T_max/self.resource.stepDelay)
            signal = param * time - startValue
                              
        elif combo_aimingState == 1:
            span = -abs(stopValue - startValue)
            T_max = param

            time = linspace(0, T_max, T_max/self.resource.stepDelay)
            signal = span * ones(len(time)) + startValue
            
        return(time, signal)

    def serialize(self, object):
    #This method serialize an object result and write it into the specified file
        path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("config files","*.ini"),("results files","*.result"),("all files","*.*")))
        if path != "":
            File = open(path, 'wb')
            pickle.dump(object, File, pickle.HIGHEST_PROTOCOL)

            File.close()
        

    def load(self):
    #This method import a serialized object result into the software
        path =  filedialog.askopenfilename(title = "Select file",filetypes = (("config files","*.ini"),("results files","*.result"),("all files","*.*")))
        if path != "":
            File = open(path, 'rb')
            object = pickle.load(File)
            File.close()

            return(object)