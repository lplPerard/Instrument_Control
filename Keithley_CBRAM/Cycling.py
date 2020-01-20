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

from tkinter import LabelFrame
from tkinter import Label
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter.ttk import Combobox

from numpy import ones
from numpy import concatenate

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
        self.__initVars()
        self.__initLabels()
        self.__initCombobox()
        self.__initEntries()

        self.button_actualizeSequence.grid(column=0, row=3, rowspan=1, padx=10, pady=5)
        self.button_startSequence.grid(column=1, row=3, rowspan=1, padx=10, pady=5)
        self.button_measureResistance.grid(column=1, row=6, rowspan=1, padx=10, pady=5)

    def __initGraphs(self):
    #This method instancitaes all the Graphs used by the Cycling test bench GUI
        self.Graph = [Multilayer_Graph(self.frame, self.resource, "Voltage"), Multilayer_Graph(self.frame, self.resource, "Current"), Multilayer_Graph(self.frame, self.resource, "Resistance"), Multilayer_Graph(self.frame, self.resource, "Power")]

        self.graph_TL = self.Graph[0]
        self.graph_TR = self.Graph[1]
        self.graph_BL = self.Graph[2]
        self.graph_BR = self.Graph[3]

        self.graph_TL.frame.grid(column=2, row=0, rowspan=6)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=6)
        self.graph_BL.frame.grid(column=2, row=6, rowspan=6)
        self.graph_BR.frame.grid(column=3, row=6, rowspan=6)

    def __initLabelFrames(self):
    #This method instanciates all the LabelFrames used in the Cycling test bench GUI
        self.labelFrame_ramp = LabelFrame(self.frame, text="Ramp")
        self.labelFrame_ramp.configure(bg=self.resource.bgColor)
        self.labelFrame_ramp.grid(column=0, columnspan=2, row=1)

        self.labelFrame_pulse = LabelFrame(self.frame, text="Pulse")
        self.labelFrame_pulse.configure(bg=self.resource.bgColor)
        self.labelFrame_pulse.grid(column=0, columnspan=2, row=2)

        self.labelFrame_graph = LabelFrame(self.frame, text="Graphs")
        self.labelFrame_graph.configure(bg=self.resource.bgColor)
        self.labelFrame_graph.grid(column=0, columnspan=2, row=7)

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.doubleVar_ramp_startValue = DoubleVar()
        self.doubleVar_ramp_startValue.set(0)

        self.doubleVar_ramp_stopValue = DoubleVar()
        self.doubleVar_ramp_stopValue.set(20)

        self.doubleVar_ramp_param = DoubleVar()
        self.doubleVar_ramp_param.set(50)

        self.doubleVar_ramp_compliance = DoubleVar()
        self.doubleVar_ramp_compliance.set(1e-1)

        self.doubleVar_pulse_startValue = DoubleVar()
        self.doubleVar_pulse_startValue.set(0)

        self.doubleVar_pulse_stopValue = DoubleVar()
        self.doubleVar_pulse_stopValue.set(20)

        self.doubleVar_pulse_param = DoubleVar()
        self.doubleVar_pulse_param.set(1)

        self.doubleVar_pulse_compliance = DoubleVar()
        self.doubleVar_pulse_compliance.set(1e-1)

        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("CU:XXX:NF:XXX:AL:XXX:n:0000")

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench provides signal configuration to\nprogram a CBRAM cell. The signal is generated\nby steps using a SourceMeter Unit.", padx=10, pady=20)
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

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_graph1 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "R_low Histogram", "R_high Histogram", "R_low/time", "R_high/time"])
        self.combo_graph1.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph1.configure(background=self.resource.bgColor)
        self.combo_graph1.grid(column=1, row=0)
        self.combo_graph1.current(0)

        self.combo_graph2 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "R_low Histogram", "R_high Histogram", "R_low/time", "R_high/time"])
        self.combo_graph2.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph2.configure(background=self.resource.bgColor)
        self.combo_graph2.grid(column=1, row=1)
        self.combo_graph2.current(1)

        self.combo_graph3 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "R_low Histogram", "R_high Histogram", "R_low/time", "R_high/time"])
        self.combo_graph3.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph3.configure(background=self.resource.bgColor)
        self.combo_graph3.grid(column=1, row=2)
        self.combo_graph3.current(2)

        self.combo_graph4 = Combobox(self.labelFrame_graph, state="readonly", width=30, values=["Voltage/iteration", "Current/iteration", "Resistance/iteration", "Power/iteration", "R_low Histogram", "R_high Histogram", "R_low/time", "R_high/time"])
        self.combo_graph4.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph4.configure(background=self.resource.bgColor)
        self.combo_graph4.grid(column=1, row=3)
        self.combo_graph4.current(3)

    def combo_graph_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        self.graph_TL.frame.grid_forget()
        self.graph_TR.frame.grid_forget()
        self.graph_BL.frame.grid_forget()
        self.graph_BR.frame.grid_forget()

        self.graph_TL = self.Graph[self.combo_graph1.current()]
        print(self.combo_graph1.current())
        self.graph_TR = self.Graph[self.combo_graph2.current()]
        self.graph_BL = self.Graph[self.combo_graph3.current()]
        self.graph_BR = self.Graph[self.combo_graph4.current()]

        self.graph_TL.frame.grid(column=2, row=0, rowspan=6)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=6)
        self.graph_BL.frame.grid(column=2, row=6, rowspan=6)
        self.graph_BR.frame.grid(column=3, row=6, rowspan=6)

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_ramp_startValue = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_startValue, width=12)
        self.entry_ramp_startValue.grid(column=1, row=0, pady=self.resource.pady)

        self.entry_ramp_stopValue = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_stopValue, width=12)
        self.entry_ramp_stopValue.grid(column=1, row=1, pady=self.resource.pady)

        self.entry_ramp_param = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_param, width=12)
        self.entry_ramp_param.grid(column=1, row=2, pady=self.resource.pady)

        self.entry_ramp_compliance = Entry(self.labelFrame_ramp, textvariable=self.doubleVar_ramp_compliance, width=12)
        self.entry_ramp_compliance.grid(column=1, row=3, pady=self.resource.pady)

        self.entry_pulse_startValue = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_startValue, width=12)
        self.entry_pulse_startValue.grid(column=1, row=0, pady=self.resource.pady)

        self.entry_pulse_stopValue = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_stopValue, width=12)
        self.entry_pulse_stopValue.grid(column=1, row=1, pady=self.resource.pady)

        self.entry_pulse_param = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_param, width=12)
        self.entry_pulse_param.grid(column=1, row=2, pady=self.resource.pady)

        self.entry_pulse_compliance = Entry(self.labelFrame_pulse, textvariable=self.doubleVar_pulse_compliance, width=12)
        self.entry_pulse_compliance.grid(column=1, row=3, pady=self.resource.pady)

        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=22)
        self.entry_CBRAM_ident.grid(column=1, row=4, pady=self.resource.pady)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12)
        self.entry_CBRAM_resistance.grid(column=1, row=5, pady=self.resource.pady)

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.button_actualizeSequence_callBack()

        self.results.cell.ident = self.stringVar_CBRAM_ident.get()
        [self.results.signal_1, self.results.signal_2] = self.service.generateSingleVoltageWaveform(self.resource.voltCoeff*self.signal, self.resource.currCoeff*self.compliance)

        self.button_measureResistance_callBack()

        self.printResult()
        
    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [self.ramp_time, self.ramp_signal, ] = self.controller.generateRampSequence(self.doubleVar_ramp_startValue.get(), self.doubleVar_ramp_stopValue.get(), self.doubleVar_ramp_param.get())
        [self.pulse_time, self.pulse_signal, ] = self.controller.generatePulseSequence(self.doubleVar_pulse_startValue.get(), self.doubleVar_pulse_stopValue.get(), self.doubleVar_pulse_param.get())
        self.ramp_compliance = self.doubleVar_ramp_compliance.get()
        self.pulse_compliance = self.doubleVar_pulse_compliance.get()

        [self.time, self.signal, ] = self.controller.generateMixedSequence(self.ramp_time, self.ramp_signal, self.pulse_time, self.pulse_signal)
                        
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()

        if self.resource.Graph_compliance == True:
            self.compliance = concatenate((self.ramp_compliance*ones(len(self.ramp_time)),self.pulse_compliance*ones(len(self.pulse_time))))
            self.Graph[1].addGraph(x=self.time, y=self.compliance, color="red", grid=self.resource.Graph_grid)

        self.Graph[0].addGraph(x=self.time, xlabel="time", y=self.signal, ylabel=self.resource.source, grid=self.resource.Graph_grid)
        
    def button_measureResistance_callBack(self):
    #This method is a callBack funtion for button_startSequence
        R = self.service.measureResistance()
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)

    def printResult(self):
    #This method add results to Graphs
        self.graph_TL.clearGraph()
        self.graph_TR.clearGraph()
        self.graph_BL.clearGraph()
        self.graph_BR.clearGraph()

        self.Graph[0].addGraph(x=self.time, xlabel="time", y=self.results.signal_1/self.resource.voltCoeff, ylabel=self.resource.source, color="orange", grid=self.resource.Graph_grid)
        self.Graph[1].addGraph(x=self.time, xlabel="time", y=self.results.signal_2/self.resource.currCoeff, ylabel=self.resource.sense, color="orange", grid=self.resource.Graph_grid)
        self.Graph[2].addGraph(x=self.time, xlabel="time", y=(self.results.signal_1/self.results.signal_2)/self.resource.resistanceCoeff, ylabel="Resistance", yscale="log", color="orange", grid=self.resource.Graph_grid)
        self.Graph[3].addGraph(x=self.time, xlabel="time", y=(self.results.signal_1*self.results.signal_2)/self.resource.powerCoeff, ylabel="Power", color="orange", grid=self.resource.Graph_grid)
