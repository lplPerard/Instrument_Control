"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for the Single test bench. Single Sequence allow to modify the state of a CBRAM cell once.

"""

from Sequence import Sequence

from Graph import Graph

from tkinter import Label
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter.ttk import Combobox

from numpy import ones
from numpy import linspace
from numpy import asarray

class Single(Sequence):
    """Class containing the Single testbench.

    """

    def __init__(self, root, resource):
    #Constructor for the Single class
        Sequence.__init__(self, root, resource)
        self.state = "SINGLE"

        self.__initWidgets()
        self.button_actualizeSequence_callBack()

    def __initWidgets(self):
    #The method creates/actualize all the Widgets displayed in the Single sequence frame
        self.__initVars()
        self.__initLabels()
        self.__initCombobox()
        self.__initEntries()

        self.button_actualizeSequence.grid(column=0, row=6, rowspan=2, padx=10, pady=5)
        self.button_startSequence.grid(column=1, row=6, rowspan=2, padx=10, pady=5)
        self.button_measureResistance.grid(column=1, row=10, rowspan=1, padx=10, pady=5)

        self.Graph = [Graph(self.frame, self.resource, "Voltage"), Graph(self.frame, self.resource, "Current"), Graph(self.frame, self.resource, "Resistance"), Graph(self.frame, self.resource, "Power")]
        self.Graph[0].frame.grid(column=2, row=0, rowspan=10)
        self.Graph[1].frame.grid(column=3, row=0, rowspan=10)
        self.Graph[2].frame.grid(column=2, row=10, rowspan=10)
        self.Graph[3].frame.grid(column=3, row=10, rowspan=10)

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.stringVar_startValue = StringVar()
        self.stringVar_startValue.set("Start value : ")
        
        self.stringVar_stopValue = StringVar()
        self.stringVar_stopValue.set("Stop value : ")

        self.stringVar_param = StringVar()
        self.stringVar_param.set("Ramp : ")

        self.stringVar_compliance = StringVar()
        self.stringVar_compliance.set(self.resource.sense + " compliance : ")

        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("600:1000:600:cell:00x00")

        self.stringVar_CBRAM_resistance = StringVar()
        self.stringVar_CBRAM_resistance.set(" CBRAM cell's resistance : ")

        self.doubleVar_startValue = DoubleVar()
        self.doubleVar_startValue.set(0)

        self.doubleVar_stopValue = DoubleVar()
        self.doubleVar_stopValue.set(15)

        self.doubleVar_param = DoubleVar()
        self.doubleVar_param.set(1)

        self.doubleVar_compliance = DoubleVar()
        self.doubleVar_compliance.set(0.5)

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench provides signal configuration to\nprogram a CBRAM cell. The signal is generated\nby steps using a SourceMeter Unit.", padx=10, pady=20)
        self.label_description.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_description.grid(column=0, columnspan=2, row=0)

        self.label_startValue = Label(self.frame, textvariable=self.stringVar_startValue)
        self.label_startValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_startValue.grid(column=0, row=2)

        self.label_stopValue = Label(self.frame, textvariable=self.stringVar_stopValue)
        self.label_stopValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_stopValue.grid(column=0, row=3)

        self.label_param = Label(self.frame, textvariable=self.stringVar_param)
        self.label_param.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_param.grid(column=0, row=4)

        self.label_compliance = Label(self.frame, textvariable=self.stringVar_compliance)
        self.label_compliance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_compliance.grid(column=0, row=5)

        self.label_CBRAM_ident = Label(self.frame, text="CBRAM cell's identifier : ")
        self.label_CBRAM_ident.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_ident.grid(column=0, row=8)

        self.label_CBRAM_resistance = Label(self.frame, textvariable=self.stringVar_CBRAM_resistance)
        self.label_CBRAM_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_resistance.grid(column=0, row=9)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_aimingState = Combobox(self.frame, state="readonly", width=30, values=["SET cell in LOW state", "SET cell in HIGH state"])
        self.combo_aimingState.bind("<<ComboboxSelected>>", self.combo_aimingState_callback)
        self.combo_aimingState.configure(background=self.resource.bgColor)
        self.combo_aimingState.grid(column=0, columnspan=2, row=1)
        self.combo_aimingState.current(0)

    def combo_aimingState_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        if self.combo_aimingState.current() == 0:
            self.stringVar_param.set("Ramp : ")
            self.doubleVar_startValue.set(0)
            self.doubleVar_stopValue.set(15)
            self.doubleVar_param.set(3)
            self.doubleVar_compliance.set(0.5)

        elif self.combo_aimingState.current() == 1:
            self.stringVar_param.set("Pulse width : ")
            self.doubleVar_startValue.set(0)
            self.doubleVar_stopValue.set(20)
            self.doubleVar_param.set(1)
            self.doubleVar_compliance.set(150)

        self.button_actualizeSequence_callBack()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_startValue = Entry(self.frame, textvariable=self.doubleVar_startValue, width=12)
        self.entry_startValue.grid(column=1, row=2, pady=self.resource.pady)

        self.entry_stopValue = Entry(self.frame, textvariable=self.doubleVar_stopValue, width=12)
        self.entry_stopValue.grid(column=1, row=3, pady=self.resource.pady)

        self.entry_param = Entry(self.frame, textvariable=self.doubleVar_param, width=12)
        self.entry_param.grid(column=1, row=4, pady=self.resource.pady)

        self.entry_compliance = Entry(self.frame, textvariable=self.doubleVar_compliance, width=12)
        self.entry_compliance.grid(column=1, row=5, pady=self.resource.pady)

        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=25)
        self.entry_CBRAM_ident.grid(column=1, row=8, padx=self.resource.padx)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12, state="readonly")
        self.entry_CBRAM_resistance.grid(column=1, row=9, pady=self.resource.pady)

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.button_actualizeSequence_callBack()

        [self.results.signal_1, self.results.signal_2] = self.service.generateSingleVoltageWaveform(self.resource.voltCoeff*self.signal, self.resource.currCoeff*self.results.ramp_compliance)

        self.results.cell_resistance = self.button_measureResistance_callBack()       

        self.printResult()
        self.param2result()
        self.autoExport()
        
    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.results.cell_ident = self.stringVar_CBRAM_ident.get()

        self.results.ramp_start_value = self.doubleVar_startValue.get()
        self.results.ramp_stop_value = self.doubleVar_stopValue.get()
        self.results.ramp_param = self.doubleVar_param.get()                    
        self.results.ramp_compliance = self.doubleVar_compliance.get()

        if self.combo_aimingState.current() == 0:
            [self.time, self.signal] = self.controller.generateRampSequence(self.doubleVar_startValue.get(), self.doubleVar_stopValue.get(), self.doubleVar_param.get())
        
        elif self.combo_aimingState.current() == 1:
            [self.time, self.signal] = self.controller.generatePulseSequence(self.doubleVar_startValue.get(), self.doubleVar_stopValue.get(), self.doubleVar_param.get())
                        
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()

        if self.resource.Graph_compliance == True:
            self.Graph[1].addGraph(x=self.time, y=self.results.ramp_compliance*ones(len(self.time)), color="red", grid=self.resource.Graph_grid)            
            self.Graph[1].addGraph(x=self.time, y=-1*self.results.ramp_compliance*ones(len(self.time)), color="red", grid=self.resource.Graph_grid)
        
        elif self.resource.Graph_compliance == False:
            self.Graph[1].addGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)

        self.Graph[0].addGraph(x=self.time, xlabel="time", y=self.signal, ylabel=self.resource.source, grid=self.resource.Graph_grid)
        self.Graph[2].addGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)
        self.Graph[3].addGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)
        
    def button_measureResistance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        R = self.service.measureResistance()
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        return(R)

    def printResult(self):
    #This method add results to Graphs
        self.doubleVar_startValue.set(self.results.ramp_start_value)
        self.doubleVar_stopValue.set(self.results.ramp_stop_value)
        self.doubleVar_param.set(self.results.ramp_param)
        self.doubleVar_compliance.set(self.results.ramp_compliance)

        self.stringVar_CBRAM_ident.set(self.results.cell_ident)
        self.doubleVar_CBRAM_resistance.set(self.results.cell_resistance)

        self.button_actualizeSequence_callBack()

        time = linspace(0, len(self.results.signal_1)*self.resource.stepDelay, len(self.results.signal_1))

        self.Graph[0].addGraph(x=time, xlabel="time", y=asarray(self.results.signal_1)/self.resource.voltCoeff, ylabel=self.resource.source, color="orange", grid=self.resource.Graph_grid)
        self.Graph[1].addGraph(x=time, xlabel="time", y=asarray(self.results.signal_2)/self.resource.currCoeff, ylabel=self.resource.sense, color="orange", grid=self.resource.Graph_grid)
        self.Graph[2].addGraph(x=time, xlabel="time", y=(asarray(self.results.signal_1)/self.results.signal_2)/self.resource.resistanceCoeff, ylabel="Resistance", yscale="log", color="orange", grid=self.resource.Graph_grid)
        self.Graph[3].addGraph(x=time, xlabel="time", y=(asarray(self.results.signal_1)*self.results.signal_2)/self.resource.powerCoeff, ylabel="Power", color="orange", grid=self.resource.Graph_grid)


   
