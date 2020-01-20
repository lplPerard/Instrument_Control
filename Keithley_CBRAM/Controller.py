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
from numpy import concatenate

import pickle

class Controller():
    """Class containing the Controller for the CBRAM software

    """

    def __init__(self, resource):
    #Constructor for the Model class
        self.resource = resource

    def generateRampSequence(self, ramp_startValue, ramp_stopValue, ramp_param):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        ramp_span = ramp_stopValue - ramp_startValue
        ramp_T_max = ramp_span / ramp_param

        ramp_time = linspace(0, ramp_T_max, ramp_T_max/self.resource.stepDelay)
        ramp_signal = ramp_param * ramp_time - ramp_startValue

        return(ramp_time, ramp_signal)

    def generatePulseSequence(self, pulse_startValue, pulse_stopValue, pulse_param):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        pulse_span = -abs(pulse_stopValue - pulse_startValue)
        pulse_T_max = pulse_param

        pulse_time = linspace(0, pulse_T_max, pulse_T_max/self.resource.stepDelay)
        pulse_signal = pulse_span * ones(len(pulse_time)) + pulse_startValue
            
        return(pulse_time, pulse_signal)

    def generateMixedSequence(self, pulse_time, pulse_signal, ramp_time, ramp_signal):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        total_T_max = ramp_time[-1] + pulse_time[-1]
        total_time = linspace(0, total_T_max, len(ramp_time) + len(pulse_time))
        total_signal = concatenate((pulse_signal, ramp_signal))
            
        return(total_time, total_signal)

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