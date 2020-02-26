"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for the IV test bench. IV sequence is made to characterize the cell's IV curve.

"""

from Sequence import Sequence

from Graph import Graph

from tkinter import Label
from tkinter import LabelFrame
from tkinter import Button
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter.ttk import Combobox

from numpy import ones
from numpy import linspace
from numpy import asarray

class IV(Sequence):
    """Class containing the IV testbench.

    """

    def __init__(self, root, resource):
    #Constructor for the Single class
        Sequence.__init__(self, root, resource)
        self.state = "IV"

        self.__initWidgets()
        self.button_actualizeSequence_callBack()

    def __initWidgets(self):
    #The method creates/actualize all the Widgets displayed in the Single sequence frame
        self.__initGraphs()
        self.__initLabelFrames()
        self.__initButtons()
        self.__initVars()
        self.__initLabels()
        self.__initCombobox()
        self.__initEntries()

    def __initGraphs(self):
    #This method instancitaes all the Graphs used by the Cycling test bench GUI
        self.Graph = [Graph(self.frame, self.resource, "Voltage"), Graph(self.frame, self.resource, "Current"), Graph(self.frame, self.resource, "IV Curve"), Graph(self.frame, self.resource, "Resistance"), Graph(self.frame, self.resource, "Power")]
       
        self.graph_TL = self.Graph[0]
        self.graph_TR = self.Graph[1]
        self.graph_BL = self.Graph[2]
        self.graph_BR = self.Graph[3]

        self.Graph[4].frame.grid_forget()

        self.graph_TL.frame.grid(column=2, row=0, rowspan=10)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=10)
        self.graph_BL.frame.grid(column=2, row=10, rowspan=10)
        self.graph_BR.frame.grid(column=3, row=10, rowspan=10)

    def __initLabelFrames(self):
    #This method instanciates all the LabelFrames used in the Cycling test bench GUI
        self.labelFrame_signal = LabelFrame(self.frame, text="Signal")
        self.labelFrame_signal.configure(bg=self.resource.bgColor)
        self.labelFrame_signal.grid(column=0, columnspan=2, row=1, rowspan=6, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_graph = LabelFrame(self.frame, text="Graphs")
        self.labelFrame_graph.configure(bg=self.resource.bgColor)
        self.labelFrame_graph.grid(column=0, columnspan=2, row=11, padx=self.resource.padx, pady=self.resource.pady)
        
    def __initButtons(self):
    #This method instanciates all the buttons used by the Cycling test bench GUI
        self.button_graph_actualizeGraphs = Button(self.labelFrame_graph, text="Actualize Graphs", command=self.button_graph_actualizeGraphs_callBack, padx=5, pady=10)
        self.button_graph_actualizeGraphs.grid(column=1, columnspan=2, row=6, padx=self.resource.padx, pady=self.resource.pady)

        self.button_actualizeSequence.grid(column=0, row=7, padx=10, pady=5)
        self.button_startSequence.grid(column=1, row=7, padx=10, pady=5)
        self.button_measureResistance.grid(column=1, row=10, rowspan=1, padx=10, pady=5)
        
    def button_graph_actualizeGraphs_callBack(self):
    #Callback method for actualizeGraphs buttons
        self.button_actualizeSequence_callBack()
        self.combo_graph_callback()

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("35u:1000n:600n:ddmmyyss:00x00")

        self.stringVar_CBRAM_resistance = StringVar()
        self.stringVar_CBRAM_resistance.set(" CBRAM cell's resistance : ")

        self.doubleVar_peakValue = DoubleVar()
        self.doubleVar_peakValue.set(15)

        self.doubleVar_ramp = DoubleVar()
        self.doubleVar_ramp.set(1)

        self.doubleVar_compliance = DoubleVar()
        self.doubleVar_compliance.set(0.5)

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench provides signal configuration to determine the \nIV characteristic of a CBRAM. The triangular signal is generated\nby steps using a SourceMeter Unit.", padx=10, pady=20)
        self.label_description.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_description.grid(column=0, columnspan=2, row=0)

        self.label_peakValue = Label(self.labelFrame_signal, text = "Peak Value : ")
        self.label_peakValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_peakValue.grid(column=0, row=0)

        self.label_ramp = Label(self.labelFrame_signal, text = "Ramp : ")
        self.label_ramp.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp.grid(column=0, row=1)

        self.label_compliance = Label(self.labelFrame_signal, text = "Compliance : ")
        self.label_compliance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_compliance.grid(column=0, row=2)

        self.label_CBRAM_ident = Label(self.frame, text="CBRAM cell's identifier : ")
        self.label_CBRAM_ident.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_ident.grid(column=0, row=8)

        self.label_CBRAM_resistance = Label(self.frame, textvariable=self.stringVar_CBRAM_resistance)
        self.label_CBRAM_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_resistance.grid(column=0, row=9)

        self.label_graph_graph1 = Label(self.labelFrame_graph, text="Graph1 : ")
        self.label_graph_graph1.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph1.grid(column=0, row=0)

        self.label_graph_graph2 = Label(self.labelFrame_graph, text="Graph2 : ")
        self.label_graph_graph2.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph2.grid(column=0, row=1)

        self.label_graph_graph3 = Label(self.labelFrame_graph, text="Graph3 : ")
        self.label_graph_graph3.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph3.grid(column=0, row=2)

        self.label_graph_graph4 = Label(self.labelFrame_graph, text="Graph4 : ")
        self.label_graph_graph4.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph4.grid(column=0, row=3)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_graph1 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration", "I/V curve", "Resistance/iteration", "Power/iteration"])
        self.combo_graph1.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph1.configure(background=self.resource.bgColor)
        self.combo_graph1.grid(column=1, row=0, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph1.current(0)

        self.combo_graph2 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration", "I/V curve", "Resistance/iteration", "Power/iteration"])
        self.combo_graph2.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph2.configure(background=self.resource.bgColor)
        self.combo_graph2.grid(column=1, row=1, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph2.current(1)

        self.combo_graph3 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration", "I/V curve", "Resistance/iteration", "Power/iteration"])
        self.combo_graph3.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph3.configure(background=self.resource.bgColor)
        self.combo_graph3.grid(column=1, row=2, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph3.current(2)

        self.combo_graph4 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration", "I/V curve", "Resistance/iteration", "Power/iteration"])
        self.combo_graph4.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph4.configure(background=self.resource.bgColor)
        self.combo_graph4.grid(column=1, row=3, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph4.current(3)

    def combo_graph_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        self.graph_TL.frame.grid_forget()
        self.graph_TR.frame.grid_forget()
        self.graph_BL.frame.grid_forget()
        self.graph_BR.frame.grid_forget()

        self.graph_TL = self.Graph[self.combo_graph1.current()]
        self.graph_TR = self.Graph[self.combo_graph2.current()]
        self.graph_BL = self.Graph[self.combo_graph3.current()]
        self.graph_BR = self.Graph[self.combo_graph4.current()]

        self.graph_TL.frame.grid(column=2, row=0, rowspan=10)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=10)
        self.graph_BL.frame.grid(column=2, row=10, rowspan=10)
        self.graph_BR.frame.grid(column=3, row=10, rowspan=10)

        self.printResult()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_peakValue = Entry(self.labelFrame_signal, textvariable=self.doubleVar_peakValue, width=12)
        self.entry_peakValue.grid(column=1, row=0, pady=self.resource.pady)

        self.entry_ramp = Entry(self.labelFrame_signal, textvariable=self.doubleVar_ramp, width=12)
        self.entry_ramp.grid(column=1, row=1, pady=self.resource.pady)

        self.entry_compliance = Entry(self.labelFrame_signal, textvariable=self.doubleVar_compliance, width=12)
        self.entry_compliance.grid(column=1, row=2, pady=self.resource.pady)

        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=30)
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

        self.results.ramp_stop_value = self.doubleVar_peakValue.get()
        self.results.ramp_param = self.doubleVar_ramp.get()                    
        self.results.ramp_compliance = self.doubleVar_compliance.get()

        [self.time, self.signal] = self.controller.generateTriangularSequence(self.doubleVar_peakValue.get(), self.doubleVar_ramp.get())

        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()

        if self.resource.Graph_compliance == True:
            self.Graph[1].addStepGraph(x=self.time, y=self.results.ramp_compliance*ones(len(self.time)), color="red", grid=self.resource.Graph_grid)            
            self.Graph[1].addStepGraph(x=self.time, y=-1*self.results.ramp_compliance*ones(len(self.time)), color="red", grid=self.resource.Graph_grid)
        
        elif self.resource.Graph_compliance == False:
            self.Graph[1].addStepGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)

        self.Graph[0].addStepGraph(x=self.time, xlabel="time", y=self.signal, ylabel=self.resource.source, grid=self.resource.Graph_grid)
        self.Graph[2].addStepGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)
        self.Graph[3].addStepGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)
        
    def button_measureResistance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        R = self.service.measureResistance()
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        return(R)

    def printResult(self):
    #This method add results to Graphs
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()
        
        time = linspace(0, len(self.results.signal_1)*self.resource.stepDelay, len(self.results.signal_1))

        self.Graph[0].addStepGraph(x=time, xlabel="time", y=asarray(self.results.signal_1)/self.resource.voltCoeff, ylabel=self.resource.source, color="orange", grid=self.resource.Graph_grid)
        self.Graph[1].addStepGraph(x=time, xlabel="time", y=asarray(self.results.signal_2)/self.resource.currCoeff, ylabel=self.resource.sense, color="orange", grid=self.resource.Graph_grid)
        self.Graph[2].addLinGraph(x=asarray(self.results.signal_1)/self.resource.voltCoeff, xlabel="Voltage", y=asarray(self.results.signal_2)/self.resource.currCoeff, ylabel="Current", color="orange", grid=self.resource.Graph_grid)
        self.Graph[3].addLinGraph(x=time, xlabel="time", y=(asarray(self.results.signal_1)/self.results.signal_2)/self.resource.resistanceCoeff, ylabel="Resistance", yscale="log", color="orange", grid=self.resource.Graph_grid)
        self.Graph[4].addStepGraph(x=time, xlabel="time", y=(asarray(self.results.signal_1)*self.results.signal_2)/self.resource.powerCoeff, ylabel="Power", color="orange", grid=self.resource.Graph_grid)
        
    def loadResults(self):
    #This methods load results in the different widgets  
        self.doubleVar_peakValue.set(self.results.ramp_stop_value)
        self.doubleVar_ramp.set(self.results.ramp_param)
        self.doubleVar_compliance.set(self.results.ramp_compliance)

        self.stringVar_CBRAM_ident.set(self.results.cell_ident)
        self.doubleVar_CBRAM_resistance.set(self.results.cell_resistance)

        self.printResult()
