"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for Sequence. Sequence is the superclass for the different test bench.

"""
import os

from datetime import date

from Controller import Controller
from Service import Service
from Results import Results

from tkinter import LabelFrame
from tkinter import Button
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END

class Sequence():
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self, root, resource, terminal):
    #Constructor for the Sequence_view superclass
        self.state = ""
        self.signal = []
        self.time = []
        self.compliance = 0
        self.results = Results()

        self.resource = resource
        self.controller = Controller(resource)
        self.service = Service(root, resource)

        self.term_text = terminal

        self.frame = LabelFrame(root)

        self.button_startSequence = Button(self.frame, text="Start Sequence", command=self.button_startSequence_callBack, padx=5, pady=10)
        self.button_actualizeSequence = Button(self.frame, text="Refresh Sequence", command=self.button_actualizeSequence_callBack, padx=5, pady=10)
        
        self.button_measureResistance_pos = Button(self.frame, text="Measure +", command=self.button_measureResistance_pos_callBack, padx=5, pady=10)
        self.button_measureResistance_neg = Button(self.frame, text="Measure -", command=self.button_measureResistance_neg_callBack, padx=5, pady=10)
        self.button_measureImpedance = Button(self.frame, text="Measure RLC", command=self.button_measureImpedance_callBack, padx=5, pady=10)

        self.Graph = [] #Graph list containing all the figures linked to the test bench

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        print('Not implemented yet')

    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        print('Not implemented yet')

    def button_measureResistance_neg_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [R, error] = self.service.measureResistance(negative=True, output=self.term_text)
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        self.results.cell_resistance = R
        return(R)
        
    def button_measureResistance_pos_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [R, error] = self.service.measureResistance(output=self.term_text)
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        return(R)

    def button_measureImpedance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [Z, error] = self.service.measureImpedance(output=self.term_text)
        self.doubleVar_CBRAM_resistance.set(Z)
        return(Z)

    def initFrame(self, text="",column=0, columnspan=1, row=0, rowspan=1, padx=15, pady=15, bg=""):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=bg)
        self.frame.grid(column=column, columnspan=columnspan, row=row, rowspan=rowspan)
        
    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.frame.grid_forget()

    def param2result(self):
    #This method saves current parameters in result attribute
        self.results.source = self.resource.source
        self.results.sense = self.resource.sense
        self.results.stepDelay = self.resource.stepDelay
        self.results.NPLC = self.resource.NPLC
        self.results.voltCoeff = self.resource.voltCoeff
        self.results.currCoeff = self.resource.currCoeff
        self.results.powerCoeff = self.resource.powerCoeff
        self.results.resistanceCoeff = self.resource.resistanceCoeff

    def autoExport(self):
    #This method is used to automatically export results if needed
        if self.resource.autoExport == True:
            today = str(date.today())
            path = self.resource.exportPath + "\\" + self.results.cell_ident[-14:-6]

            if os.path.isdir(path) == True:
                path = path + "\\" + self.state
                if os.path.isdir(path) == True:
                    path = path + "\\" + today 
                    if os.path.isdir(path) == True:
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5:] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))

                    elif os.path.isdir(path) == False:
                        os.mkdir(path)
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5:] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))

                elif os.path.isdir(path) == False:                    
                    os.mkdir(path)
                    path = path + "\\" + today 
                    if os.path.isdir(path) == True:
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5:] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))

                    elif os.path.isdir(path) == False:
                        os.mkdir(path)
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))
            
            elif os.path.isdir(path) == False:
                os.mkdir(path)
                path = path + "\\" + self.state
                if os.path.isdir(path) == True:
                    path = path + "\\" + today 
                    if os.path.isdir(path) == True:
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5:] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))

                    elif os.path.isdir(path) == False:
                        os.mkdir(path)
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5:] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))

                elif os.path.isdir(path) == False:                    
                    os.mkdir(path)
                    path = path + "\\" + today 
                    if os.path.isdir(path) == True:
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5:] + "_" + today + "_"

                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))

                    elif os.path.isdir(path) == False:
                        os.mkdir(path)
                        path = path + "\\" + self.state + "_" + self.results.cell_ident[-5] + "_" + today + "_"
                        i=1
                        while os.path.isfile(path + str(i) + ".pickle") == True:
                            i+=1

                        self.controller.autoSerialize(self.results, path + str(i))
            
            return(path + str(i))

        elif self.resource.autoExport == False:
            return("")

        
