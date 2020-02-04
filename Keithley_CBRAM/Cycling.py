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
from Histogram_Graph import Histogram_Graph

from tkinter import Button
from tkinter import LabelFrame
from tkinter import Label
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter.ttk import Combobox

from numpy import ones
from numpy import linspace
from numpy import concatenate
from numpy import asarray

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
        self.__initGraphs()
        self.__initLabelFrames()
        self.__initButtons()
        self.__initVars()
        self.__initLabels()
        self.__initCombobox()
        self.__initEntries()

    def __initGraphs(self):
    #This method instancitaes all the Graphs used by the Cycling test bench GUI
        self.Graph = [Multilayer_Graph(self.frame, self.resource, "Voltage"), Multilayer_Graph(self.frame, self.resource, "Current"), Multilayer_Graph(self.frame, self.resource, "Resistance"), Multilayer_Graph(self.frame, self.resource, "Power"), Histogram_Graph(self.frame, self.resource, "Resistance")]

        self.graph_TL = self.Graph[0]
        self.graph_TR = self.Graph[1]
        self.graph_BL = self.Graph[2]
        self.graph_BR = self.Graph[3]

        self.Graph[4].frame.grid_forget()

        self.graph_TL.frame.grid(column=2, row=0, rowspan=6)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=6)
        self.graph_BL.frame.grid(column=2, row=6, rowspan=6)
        self.graph_BR.frame.grid(column=3, row=6, rowspan=6)

    def __initLabelFrames(self):
    #This method instanciates all the LabelFrames used in the Cycling test bench GUI
        self.labelFrame_ramp = LabelFrame(self.frame, text="Ramp")
        self.labelFrame_ramp.configure(bg=self.resource.bgColor)
        self.labelFrame_ramp.grid(column=0, columnspan=2, row=1, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_pulse = LabelFrame(self.frame, text="Pulse")
        self.labelFrame_pulse.configure(bg=self.resource.bgColor)
        self.labelFrame_pulse.grid(column=0, columnspan=2, row=2, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_graph = LabelFrame(self.frame, text="Graphs")
        self.labelFrame_graph.configure(bg=self.resource.bgColor)
        self.labelFrame_graph.grid(column=0, columnspan=2, row=7, padx=self.resource.padx, pady=self.resource.pady)

    def __initButtons(self):
    #This method instanciates all the buttons used by the Cycling test bench GUI
        self.button_graph_actualizeGraphs = Button(self.labelFrame_graph, text="Actualize Graphs", command=self.button_graph_actualizeGraphs_callBack, padx=5, pady=10)
        self.button_graph_actualizeGraphs.grid(column=0, columnspan=2, row=5, padx=self.resource.padx, pady=self.resource.pady)

        self.button_actualizeSequence.grid(column=0, row=3, rowspan=1, padx=10, pady=5)
        self.button_startSequence.grid(column=1, row=3, rowspan=1, padx=10, pady=5)
        self.button_measureResistance.grid(column=1, row=6, rowspan=1, padx=10, pady=5)

    def button_graph_actualizeGraphs_callBack(self):
    #Callback method for actualizeGraphs buttons
        self.button_actualizeSequence_callBack()
        self.combo_graph_callback()

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.button_actualizeSequence_callBack()

        self.results.cell_ident = self.stringVar_CBRAM_ident.get()
        [self.results.iteration, self.results.nbTry, self.results.resistance, self.results.signal_1, self.results.signal_2] = self.service.generateCyclingVoltageWaveform(self.resource.voltCoeff*self.ramp_signal, self.resource.currCoeff*self.ramp_compliance, self.resource.voltCoeff*self.pulse_signal, self.resource.currCoeff*self.pulse_compliance)
        self.button_measureResistance_callBack()

        self.printResult()
        self.param2result()
        self.autoExport()
        
    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.results.cell_ident = self.stringVar_CBRAM_ident.get()

        self.results.ramp_start_value = self.doubleVar_ramp_startValue.get()
        self.results.ramp_stop_value = self.doubleVar_ramp_stopValue.get()
        self.results.ramp_param = self.doubleVar_ramp_param.get()                    
        self.results.ramp_compliance = self.doubleVar_ramp_compliance.get()

        self.results.pulse_start_value = self.doubleVar_pulse_startValue.get()
        self.results.pulse_stop_value = self.doubleVar_pulse_stopValue.get()
        self.results.pulse_param = self.doubleVar_pulse_param.get()                    
        self.results.pulse_compliance = self.doubleVar_pulse_compliance.get()

        [self.ramp_time, self.ramp_signal] = self.controller.generateRampSequence(self.doubleVar_ramp_startValue.get(), self.doubleVar_ramp_stopValue.get(), self.doubleVar_ramp_param.get())
        [self.pulse_time, self.pulse_signal] = self.controller.generatePulseSequence(self.doubleVar_pulse_startValue.get(), self.doubleVar_pulse_stopValue.get(), self.doubleVar_pulse_param.get())
        self.ramp_compliance = self.doubleVar_ramp_compliance.get()
        self.pulse_compliance = self.doubleVar_pulse_compliance.get()

        [self.time, self.signal] = self.controller.generateMixedSequence(self.ramp_time, self.ramp_signal, self.pulse_time, self.pulse_signal)
                        
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()

        if self.resource.Graph_compliance == True:
            self.compliance = concatenate((self.ramp_compliance*ones(len(self.ramp_time)),self.pulse_compliance*ones(len(self.pulse_time))))
            self.Graph[1].addGraph(x=self.time, y=self.compliance, color="red", grid=self.resource.Graph_grid)
            self.Graph[1].addGraph(x=self.time, y=-1*self.compliance, color="red", grid=self.resource.Graph_grid)
        
        elif self.resource.Graph_compliance == False:
            self.Graph[1].addGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)

        self.Graph[0].addGraph(x=self.time, xlabel="time", y=self.signal, ylabel=self.resource.source, grid=self.resource.Graph_grid)
        self.Graph[2].addGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)
        self.Graph[3].addGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid)
        
    def button_measureResistance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        R = self.service.measureResistance()
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        self.results.cell_resistance = R

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.doubleVar_ramp_startValue = DoubleVar()
        self.doubleVar_ramp_startValue.set(0)

        self.doubleVar_ramp_stopValue = DoubleVar()
        self.doubleVar_ramp_stopValue.set(15)

        self.doubleVar_ramp_param = DoubleVar()
        self.doubleVar_ramp_param.set(3)

        self.doubleVar_ramp_compliance = DoubleVar()
        self.doubleVar_ramp_compliance.set(0.5)

        self.doubleVar_pulse_startValue = DoubleVar()
        self.doubleVar_pulse_startValue.set(0)

        self.doubleVar_pulse_stopValue = DoubleVar()
        self.doubleVar_pulse_stopValue.set(20)

        self.doubleVar_pulse_param = DoubleVar()
        self.doubleVar_pulse_param.set(1)

        self.doubleVar_pulse_compliance = DoubleVar()
        self.doubleVar_pulse_compliance.set(150)

        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("600:1000:600:cell:00x00")

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench is made to determine \nthe maximum number of cycles that can be reached \nby a single cell.", padx=10, pady=20)
        self.label_description.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_description.grid(column=0, columnspan=2, row=0)

        self.label_ramp_startValue = Label(self.labelFrame_ramp, text="Start Value : ")
        self.label_ramp_startValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_startValue.grid(column=0, row=0)

        self.label_ramp_stopValue = Label(self.labelFrame_ramp, text="Stop Value : ")
        self.label_ramp_stopValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_stopValue.grid(column=0, row=1)

        self.label_ramp_param = Label(self.labelFrame_ramp, text="Ramp : ")
        self.label_ramp_param.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_param.grid(column=0, row=2)

        self.label_ramp_compliance = Label(self.labelFrame_ramp, text="Compliance : ")
        self.label_ramp_compliance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_compliance.grid(column=0, row=3)

        self.label_pulse_startValue = Label(self.labelFrame_pulse, text="Start Value : ")
        self.label_pulse_startValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_startValue.grid(column=0, row=0)

        self.label_pulse_stopValue = Label(self.labelFrame_pulse, text="Stop Value : ")
        self.label_pulse_stopValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_stopValue.grid(column=0, row=1)

        self.label_pulse_param = Label(self.labelFrame_pulse, text="Pulse width : ")
        self.label_pulse_param.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_param.grid(column=0, row=2)

        self.label_pulse_compliance = Label(self.labelFrame_pulse, text="Compliance : ")
        self.label_pulse_compliance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_compliance.grid(column=0, row=3)

        self.label_CBRAM_ident = Label(self.frame, text="CBRAM cell's identifier : ")
        self.label_CBRAM_ident.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_ident.grid(column=0, row=4)

        self.label_CBRAM_resistance = Label(self.frame, text="CBRAM cell's resistance : ")
        self.label_CBRAM_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_resistance.grid(column=0, row=5)

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

        self.label_graph_iteration = Label(self.labelFrame_graph, text="Iteration : ")
        self.label_graph_iteration.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_iteration.grid(column=0, row=4)        

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_graph1 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "Resistance Histogram"])
        self.combo_graph1.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph1.configure(background=self.resource.bgColor)
        self.combo_graph1.grid(column=1, row=0, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph1.current(0)

        self.combo_graph2 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "Resistance Histogram"])
        self.combo_graph2.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph2.configure(background=self.resource.bgColor)
        self.combo_graph2.grid(column=1, row=1, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph2.current(1)

        self.combo_graph3 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "Resistance Histogram"])
        self.combo_graph3.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph3.configure(background=self.resource.bgColor)
        self.combo_graph3.grid(column=1, row=2, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph3.current(2)

        self.combo_graph4 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "Resistance Histogram"])
        self.combo_graph4.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph4.configure(background=self.resource.bgColor)
        self.combo_graph4.grid(column=1, row=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph4.current(3)

        self.combo_iteration = Combobox(self.labelFrame_graph, state="readonly", width=30, values=[])
        self.combo_iteration.bind("<<ComboboxSelected>>", self.combo_iteration_callback)
        self.combo_iteration.configure(background=self.resource.bgColor)
        self.combo_iteration.grid(column=1, row=4, padx=self.resource.padx, pady=self.resource.pady)

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

        self.graph_TL.frame.grid(column=2, row=0, rowspan=6)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=6)
        self.graph_BL.frame.grid(column=2, row=6, rowspan=6)
        self.graph_BR.frame.grid(column=3, row=6, rowspan=6)

        self.printResult()

    def combo_iteration_callback(self, args=[]):
    #Callback method for combo Iteration
        self.button_graph_actualizeGraphs_callBack()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_ramp_startValue = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_startValue, width=12)
        self.entry_ramp_startValue.grid(column=1, row=0, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_ramp_stopValue = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_stopValue, width=12)
        self.entry_ramp_stopValue.grid(column=1, row=1, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_ramp_param = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_param, width=12)
        self.entry_ramp_param.grid(column=1, row=2, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_ramp_compliance = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_compliance, width=12)
        self.entry_ramp_compliance.grid(column=1, row=3, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_startValue = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_startValue, width=12)
        self.entry_pulse_startValue.grid(column=1, row=0, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_stopValue = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_stopValue, width=12)
        self.entry_pulse_stopValue.grid(column=1, row=1, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_param = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_param, width=12)
        self.entry_pulse_param.grid(column=1, row=2, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_compliance = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_compliance, width=12)
        self.entry_pulse_compliance.grid(column=1, row=3, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=25)
        self.entry_CBRAM_ident.grid(column=1, row=4, pady=self.resource.pady, padx=self.resource.padx)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12)
        self.entry_CBRAM_resistance.grid(column=1, row=5, padx=self.resource.padx, pady=self.resource.pady)

    def printResult(self):
    #This method add results to Graphs
        self.doubleVar_ramp_startValue.set(self.results.ramp_start_value)
        self.doubleVar_ramp_stopValue.set(self.results.ramp_stop_value)
        self.doubleVar_ramp_param.set(self.results.ramp_param)
        self.doubleVar_ramp_compliance.set(self.results.ramp_compliance)

        self.doubleVar_pulse_startValue.set(self.results.pulse_start_value)
        self.doubleVar_pulse_stopValue.set(self.results.pulse_stop_value)
        self.doubleVar_pulse_param.set(self.results.pulse_param)
        self.doubleVar_pulse_compliance.set(self.results.pulse_compliance)

        self.stringVar_CBRAM_ident.set(self.results.cell_ident)
        self.doubleVar_CBRAM_resistance.set(self.results.cell_resistance)

        self.combo_iteration.config(values=linspace(1,self.results.iteration-1, self.results.iteration-1).tolist())

        self.graph_TL.clearGraph()
        self.graph_TR.clearGraph()
        self.graph_BL.clearGraph()
        self.graph_BR.clearGraph()

        i = self.combo_iteration.current()
        length = len(self.results.signal_1[i])   
        time = linspace(0, length*self.resource.stepDelay, length)

        self.Graph[0].addGraph(x=time, xlabel="time", y=asarray(self.results.signal_1[i])/self.resource.voltCoeff, ylabel=self.resource.source, color="orange", grid=self.resource.Graph_grid)
        self.Graph[1].addGraph(x=time, xlabel="time", y=asarray(self.results.signal_2[i])/self.resource.currCoeff, ylabel=self.resource.sense, color="orange", grid=self.resource.Graph_grid)
        self.Graph[2].addGraph(x=time, xlabel="time", y=(asarray(self.results.signal_1[i])/asarray(self.results.signal_2[i]))/self.resource.resistanceCoeff, ylabel="Resistance", yscale="log", color="orange", grid=self.resource.Graph_grid)
        self.Graph[3].addGraph(x=time, xlabel="time", y=(asarray(self.results.signal_1[i])*asarray(self.results.signal_2[i]))/self.resource.powerCoeff, ylabel="Power", color="orange", grid=self.resource.Graph_grid)
        
        resistance = [x/self.resource.resistanceCoeff for x in self.results.resistance]
        
        self.Graph[4].addGraph(x=resistance, xlabel="Resistance", ylabel="Iteration", xscale="log", color="orange", grid=self.resource.Graph_grid)

        self.Graph[0].setIteration(i+1, self.results.nbTry[i])
        self.Graph[1].setIteration(i+1, self.results.nbTry[i])
        self.Graph[2].setIteration(i+1, self.results.nbTry[i])
        self.Graph[3].setIteration(i+1, self.results.nbTry[i])
