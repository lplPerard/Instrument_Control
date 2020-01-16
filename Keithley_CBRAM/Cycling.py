"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for the Cycling test bench. Cycling Sequence intend to determinate the maximum number of cycles a CBRAM cell can execute.

"""

from Sequence import Sequence

from Graph import Graph
from MultiLayer_Graph import Multilayer_Graph

from tkinter import Label
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter.ttk import Combobox

from numpy import ones

class Cycling(Sequence):
    """Class containing the Cycling testbench.

    """

    def __init__(self, root, resource):
    #Constructor for the Single class
        Sequence.__init__(self, root, resource)
        self.state = "CYCLING"

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

        self.Graph = [Multilayer_Graph(self.frame, self.resource, "Voltage"), Multilayer_Graph(self.frame, self.resource, "Current"), Multilayer_Graph(self.frame, self.resource, "Resistance"), Multilayer_Graph(self.frame, self.resource, "Power")]
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
        self.stringVar_CBRAM_ident.set("CU:XXX:NF:XXX:AL:XXX:n:0000")

        self.stringVar_CBRAM_resistance = StringVar()
        self.stringVar_CBRAM_resistance.set(" CBRAM cell's resistance : ")

        self.doubleVar_startValue = DoubleVar()
        self.doubleVar_startValue.set(0)

        self.doubleVar_stopValue = DoubleVar()
        self.doubleVar_stopValue.set(20)

        self.doubleVar_param = DoubleVar()
        self.doubleVar_param.set(50)

        self.doubleVar_compliance = DoubleVar()
        self.doubleVar_compliance.set(1e-1)

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

        elif self.combo_aimingState.current() == 1:
            self.stringVar_param.set("Pulse width : ")

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

        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=22)
        self.entry_CBRAM_ident.grid(column=1, row=8, pady=self.resource.pady)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12)
        self.entry_CBRAM_resistance.grid(column=1, row=9, pady=self.resource.pady)

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.button_actualizeSequence_callBack()
        self.button_measureResistance_callBack()

        [self.results.signal_1, self.results.signal_2] = self.service.generateSingleVoltageWaveform(self.resource.voltCoeff*self.signal, self.resource.currCoeff*self.compliance)

        self.button_measureResistance_callBack()

        self.printResult()
        
    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [self.time, self.signal] = self.controller.generateSingleSequence(self.combo_aimingState.current(), self.doubleVar_startValue.get(), self.doubleVar_stopValue.get(), self.doubleVar_param.get())
        self.compliance = self.doubleVar_compliance.get()
                        
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()

        if self.resource.Graph_compliance == True:
            self.Graph[1].addGraph(x=self.time, y=self.compliance*ones(len(self.time)), color="red", grid=self.resource.Graph_grid)

        self.Graph[0].addGraph(x=self.time, xlabel="time", y=self.signal, ylabel=self.resource.source, grid=self.resource.Graph_grid)
        
    def button_measureResistance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        R = self.service.measureResistance()
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)

    def printResult(self):
    #This method add results to Graphs

        self.Graph[0].addGraph(x=self.time, xlabel="time", y=self.results.signal_1/self.resource.voltCoeff, ylabel=self.resource.source, color="orange", grid=self.resource.Graph_grid)
        self.Graph[1].addGraph(x=self.time, xlabel="time", y=self.results.signal_2/self.resource.currCoeff, ylabel=self.resource.sense, color="orange", grid=self.resource.Graph_grid)
        self.Graph[2].addGraph(x=self.time, xlabel="time", y=(self.results.signal_1/self.results.signal_2)/self.resource.resistanceCoeff, ylabel="Resistance", yscale="log", color="orange", grid=self.resource.Graph_grid)
        self.Graph[3].addGraph(x=self.time, xlabel="time", y=(self.results.signal_1*self.results.signal_2)/self.resource.powerCoeff, ylabel="Power", color="orange", grid=self.resource.Graph_grid)


   
