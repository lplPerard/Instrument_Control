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
import json

class Controller():
    """Class containing the Controller for the CBRAM software

    """

    def __init__(self, resource):
    #Constructor for the Model class
        self.resource = resource

    def generateRampSequence(self, ramp_startValue, ramp_stopValue, ramp_param):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        ramp_span = ramp_stopValue - ramp_startValue
        ramp_T_max = ramp_span / abs(ramp_param)

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

    def generateTriangularSequence(self, peakValue_set, ramp_set, peakValue_reset, ramp_reset):
    #This method generates the IV sequence based on parameters extracted from the view
        if peakValue_reset == 0:
            peakValue_reset = peakValue_set
        if ramp_reset == 0:
            ramp_reset = ramp_set

        ramp_T_max_set = peakValue_set / abs(ramp_set)
        ramp_time_set = linspace(0, ramp_T_max_set, ramp_T_max_set/self.resource.stepDelay)

        ramp_T_max_reset = abs(peakValue_reset / ramp_reset)
        ramp_time_reset = linspace(0, ramp_T_max_reset, ramp_T_max_reset/self.resource.stepDelay)

        signal1=[]        
        signal2=[]
        
        signal1 = (ramp_set * ramp_time_set)
        signal1 = concatenate((signal1, peakValue_set - ramp_set * ramp_time_set))  
        signal2 = concatenate((signal1, -abs(ramp_reset) * ramp_time_reset))
        signal2 = concatenate((signal2, -abs(peakValue_reset)  + abs(ramp_reset) * ramp_time_reset))

        time = linspace(0, 2*ramp_T_max_set + 2*ramp_T_max_reset, len(signal2))
        return(time, signal2, len(signal1))

    def generateMixedSequence(self, pulse_time, pulse_signal, ramp_time, ramp_signal):
    #This method override parent's method. It generates the single sequence based on parameters extracted from the view
        total_T_max = ramp_time[-1] + pulse_time[-1]
        total_time = linspace(0, total_T_max, len(ramp_time) + len(pulse_time))
        total_signal = concatenate((pulse_signal, ramp_signal))
            
        return(total_time, total_signal)

    def serialize(self, object):
    #This method serialize an object result and write it into the specified file
        path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("all files","*.*"), ("Binary results files","*.result"), ("Text results files","*.txt")))
        if path != "":
            File_pickle = open(path + ".pickle", 'wb')
            pickle.dump(object, File_pickle, pickle.HIGHEST_PROTOCOL)   
            File_pickle.close()

            File_json  = open(path + ".txt", 'w')       
            json.dump(object.__dict__, File_json, indent=4)

            File_json.close()

    def autoSerialize(self, object, path):
    #This method serialize an object result and write it into teh resultat directory
        if path != "":
            File_pickle = open(path + ".pickle", 'wb')
            pickle.dump(object, File_pickle, pickle.HIGHEST_PROTOCOL) 
            File_pickle.close()  

            File_json  = open(path + ".txt", 'w')       
            json.dump(object.__dict__, File_json, indent=4)

            File_json.close()
        
    def load(self):
    #This method import a serialized object result into the software
        path =  filedialog.askopenfilename(title = "Select file",filetypes = (("Binary results files","*.pickle"), ("Text results files","*.txt"), ("all files","*.*")))
        if path != "":
            File = open(path, 'rb')
            object = pickle.load(File)
            File.close()

            if path.find('SINGLE') != -1:
                state = 'SINGLE'
            elif path.find('CYCLING') != -1:
                state = 'CYCLING'
            elif path.find('IV') != -1:
                state = 'IV'

            return(state, object)