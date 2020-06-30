"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
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
from tkinter import messagebox

from numpy import ones
from numpy import linspace
from numpy import concatenate
from numpy import asarray

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Cycling(Sequence):
    """Class containing the Cycling testbench.

    """

    def __init__(self, root, resource, terminal):
    #Constructor for the Single class
        Sequence.__init__(self, root, resource, terminal)
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
        self.Graph = [Multilayer_Graph(self.frame, self.resource, "Voltage"),
                      Multilayer_Graph(self.frame, self.resource, "Current"),
                      Multilayer_Graph(self.frame, self.resource, "Resistance/time"),
                      Multilayer_Graph(self.frame, self.resource, "Power"),
                      Multilayer_Graph(self.frame, self.resource, "IV curve"),
                      Multilayer_Graph(self.frame, self.resource, "Butterfly Curve"),
                      Multilayer_Graph(self.frame, self.resource, "RV curve"),
                      Multilayer_Graph(self.frame, self.resource, "Resistance/iteration"),
                      Histogram_Graph(self.frame, self.resource, "Resistance")]

        self.graph_TL = self.Graph[0]
        self.graph_TR = self.Graph[1]
        self.graph_BL = self.Graph[2]
        self.graph_BR = self.Graph[3]

        self.Graph[4].frame.grid_forget()
        self.Graph[5].frame.grid_forget()        
        self.Graph[6].frame.grid_forget()
        self.Graph[7].frame.grid_forget()  
        self.Graph[8].frame.grid_forget()

        self.graph_TL.frame.grid(column=2, row=0, rowspan=4)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=4)
        self.graph_BL.frame.grid(column=2, row=4, rowspan=4)
        self.graph_BR.frame.grid(column=3, row=4, rowspan=4)

    def __initLabelFrames(self):
    #This method instanciates all the LabelFrames used in the Cycling test bench GUI
        self.labelFrame_signal1 = LabelFrame(self.frame, text="Signal 1")
        self.labelFrame_signal1.configure(bg=self.resource.bgColor)
        self.labelFrame_signal1.grid(column=0, columnspan=2, row=1, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_signal2 = LabelFrame(self.frame, text="Signal 2")
        self.labelFrame_signal2.configure(bg=self.resource.bgColor)
        self.labelFrame_signal2.grid(column=0, columnspan=2, row=2, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_graph = LabelFrame(self.frame, text="Graphs")
        self.labelFrame_graph.configure(bg=self.resource.bgColor)
        self.labelFrame_graph.grid(column=0, columnspan=2, row=7, padx=self.resource.padx, pady=self.resource.pady)

    def __initButtons(self):
    #This method instanciates all the buttons used by the Cycling test bench GUI
        self.button_graph_actualizeGraphs = Button(self.labelFrame_graph, text="Actualize Graphs", command=self.button_graph_actualizeGraphs_callBack, padx=5, pady=10)
        self.button_graph_actualizeGraphs.grid(column=1, columnspan=2, row=7, padx=self.resource.padx, pady=self.resource.pady)

        self.button_actualizeSequence.grid(column=0, row=3, rowspan=1, padx=10, pady=5)
        self.button_startSequence.grid(column=1, row=3, rowspan=1, padx=10, pady=5)
        self.button_measureResistance_pos.grid(column=0, row=6, rowspan=1, padx=10, pady=5)
        self.button_measureResistance_neg.grid(column=1, row=6, rowspan=1, padx=10, pady=5)

    def button_graph_actualizeGraphs_callBack(self):
    #Callback method for actualizeGraphs buttons
        self.button_actualizeSequence_callBack()
        self.combo_graph_callback()

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.button_actualizeSequence_callBack()

        self.results.cell_ident = self.stringVar_CBRAM_ident.get()
        [self.results.iteration, self.results.nbTry, self.results.resistance, self.results.signal_1, self.results.signal_2, error] = self.service.generateCyclingVoltageWaveform(self.term_text, self.resource.voltCoeff*self.signal1_signal, self.resource.currCoeff*self.signal1_compliance, self.resource.voltCoeff*self.signal2_signal, self.resource.currCoeff*self.signal2_compliance)
        self.button_measureResistance_pos_callBack()

        self.param2result()
        path=self.autoExport()
        self.loadResults()

        if error != 0:
            messagebox.showinfo(title="Sequence ERROR", message=("An error occured during Measurement.\n Sequence were ended."))

            if self.resource.mailNotification == True :            
                message = "A cycling test was terminated with an error on your computer."
                self.service.sendEmailNotification(message)

        else :
            messagebox.showinfo(title="End of Sequence", message=("CYCLING Sequence ended with : " + str(self.results.nbTry) + " cycles\n"))

            if self.resource.mailNotification == True :
                message = "A cycling test was succesfully terminated on your computer.\n\n A total of " + str(self.results.nbTry) + " cycles were achieved, and data were saved at :\n\n" + path 
                self.service.sendEmailNotification(message)

            if self.resource.autoExport == True:
                messagebox.showinfo(title="Auto Export", message=("Result files have been exported to the following PATH :\n" + path))
        
    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.results.cell_ident = self.stringVar_CBRAM_ident.get()

        self.results.ramp_start_value = self.doubleVar_signal1_startValue.get()
        self.results.ramp_stop_value = self.doubleVar_signal1_stopValue.get()
        self.results.ramp_param = self.doubleVar_signal1_param.get()                    
        self.results.ramp_compliance = self.doubleVar_signal1_compliance.get()

        self.results.pulse_start_value = self.doubleVar_signal2_startValue.get()
        self.results.pulse_stop_value = self.doubleVar_signal2_stopValue.get()
        self.results.pulse_param = self.doubleVar_signal2_param .get()                    
        self.results.pulse_compliance = self.doubleVar_signal2_compliance.get()

        if self.combo_signal1.current() == 0 :
            [self.signal1_time, self.signal1_signal] = self.controller.generatePulseSequence(self.doubleVar_signal1_startValue.get(), self.doubleVar_signal1_stopValue.get(), self.doubleVar_signal1_param.get())
        else :
            [self.signal1_time, self.signal1_signal] = self.controller.generateRampSequence(self.doubleVar_signal1_startValue.get(), self.doubleVar_signal1_stopValue.get(), self.doubleVar_signal1_param.get())
       
        if self.combo_signal2.current() == 0 :
            [self.signal2_time, self.signal2_signal] = self.controller.generatePulseSequence(self.doubleVar_signal2_startValue.get(), self.doubleVar_signal2_stopValue.get(), self.doubleVar_signal2_param .get())
        else : 
            [self.signal2_time, self.signal2_signal] = self.controller.generateRampSequence(self.doubleVar_signal2_startValue.get(), self.doubleVar_signal2_stopValue.get(), self.doubleVar_signal2_param .get())
        
        self.signal1_compliance = self.doubleVar_signal1_compliance.get()
        self.signal2_compliance = self.doubleVar_signal2_compliance.get()

        [self.time, self.signal] = self.controller.generateMixedSequence(self.signal1_time, self.signal1_signal, self.signal2_time, self.signal2_signal)
                        
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()
        self.Graph[4].clearGraph()
        self.Graph[5].clearGraph()       
        self.Graph[6].clearGraph()
        self.Graph[7].clearGraph()   

        marker = [self.intVar_marker_position.get()]

        if self.resource.Graph_compliance == True:
            self.compliance = concatenate((self.signal1_compliance*ones(len(self.signal1_time)),self.signal2_compliance*ones(len(self.signal2_time))))
            self.Graph[1].addStepGraph(x=self.time, y=self.compliance, color="red", grid=self.resource.Graph_grid) 
            self.Graph[1].addStepGraph(x=self.time, y=-1*self.compliance, color="red", grid=self.resource.Graph_grid) 
        
        elif self.resource.Graph_compliance == False:
            self.Graph[1].addStepGraph(x=[], y=[], grid=self.resource.Graph_grid) 

        self.Graph[0].addStepGraph(x=self.time, xlabel="time", y=self.signal, ylabel=self.resource.source, grid=self.resource.Graph_grid) 
        self.Graph[2].addStepGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid) 
        self.Graph[3].addStepGraph(x=[], y=[], color="red", grid=self.resource.Graph_grid) 
        
    def button_measureResistance_pos_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [R, error] = self.service.measureResistance(output=self.term_text)
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        self.results.cell_resistance = R
        
    def button_measureResistance_neg_callBack(self):
    #This method is a callBack funtion for button_startSequence
        [R, error] = self.service.measureResistance(negative=True, output=self.term_text)
        self.doubleVar_CBRAM_resistance.set(R/self.resource.resistanceCoeff)
        self.results.cell_resistance = R

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI            
        self.stringVar_signal1_param = StringVar()
        self.stringVar_signal1_param.set('Pulse')

        self.doubleVar_signal1_startValue = DoubleVar()
        self.doubleVar_signal1_startValue.set(0)

        self.doubleVar_signal1_stopValue = DoubleVar()
        self.doubleVar_signal1_stopValue.set(20)    

        self.doubleVar_signal1_param = DoubleVar()
        self.doubleVar_signal1_param.set(0.5)

        self.doubleVar_signal1_compliance = DoubleVar()
        self.doubleVar_signal1_compliance.set(3)     
        
        self.stringVar_signal2_param = StringVar()
        self.stringVar_signal2_param.set('Pulse')

        self.doubleVar_signal2_startValue = DoubleVar()
        self.doubleVar_signal2_startValue.set(0)

        self.doubleVar_signal2_stopValue = DoubleVar()
        self.doubleVar_signal2_stopValue.set(-20)   

        self.doubleVar_signal2_param  = DoubleVar()
        self.doubleVar_signal2_param .set(0.5)

        self.doubleVar_signal2_compliance = DoubleVar()
        self.doubleVar_signal2_compliance.set(300)

        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("35u:1000n:600n:ddmmyyss:00x00")

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)

        self.intVar_marker_position = IntVar()
        self.intVar_marker_position.set(0)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench is made to determine \nthe maximum number of cycles that can be reached \nby a single cell.", padx=self.resource.padx, pady=self.resource.pady)
        self.label_description.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_description.grid(column=0, columnspan=2, row=0)

        self.label_ramp_startValue = Label(self.labelFrame_signal1, text="Start Value : ")
        self.label_ramp_startValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_startValue.grid(column=0, row=1)

        self.label_ramp_stopValue = Label(self.labelFrame_signal1, text="Stop Value : ")
        self.label_ramp_stopValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_stopValue.grid(column=0, row=2)

        self.label_ramp_param = Label(self.labelFrame_signal1, textvariable=self.stringVar_signal1_param)
        self.label_ramp_param.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_param.grid(column=0, row=3)

        self.label_ramp_compliance = Label(self.labelFrame_signal1, text="Compliance : ")
        self.label_ramp_compliance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_compliance.grid(column=0, row=4)

        self.label_pulse_startValue = Label(self.labelFrame_signal2, text="Start Value : ")
        self.label_pulse_startValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_startValue.grid(column=0, row=1)

        self.label_pulse_stopValue = Label(self.labelFrame_signal2, text="Stop Value : ")
        self.label_pulse_stopValue.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_stopValue.grid(column=0, row=2)

        self.label_pulse_param = Label(self.labelFrame_signal2, textvariable=self.stringVar_signal2_param)
        self.label_pulse_param.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_param.grid(column=0, row=3)

        self.label_pulse_compliance = Label(self.labelFrame_signal2, text="Compliance : ")
        self.label_pulse_compliance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_pulse_compliance.grid(column=0, row=4)

        self.label_CBRAM_ident = Label(self.frame, text="CBRAM cell's identifier : ")
        self.label_CBRAM_ident.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_ident.grid(column=0, row=4)

        self.label_CBRAM_resistance = Label(self.frame, text="CBRAM cell's resistance : ")
        self.label_CBRAM_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_resistance.grid(column=0, row=5)

        self.label_graph_graph1 = Label(self.labelFrame_graph, text="Graph TL : ")
        self.label_graph_graph1.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph1.grid(column=0, row=0)

        self.label_graph_graph2 = Label(self.labelFrame_graph, text="Graph TR : ")
        self.label_graph_graph2.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph2.grid(column=0, row=1)

        self.label_graph_graph3 = Label(self.labelFrame_graph, text="Graph BL : ")
        self.label_graph_graph3.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph3.grid(column=0, row=2)

        self.label_graph_graph4 = Label(self.labelFrame_graph, text="Graph BR : ")
        self.label_graph_graph4.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_graph4.grid(column=0, row=3)

        self.label_graph_iterationStart = Label(self.labelFrame_graph, text="Iteration from : ")
        self.label_graph_iterationStart.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_iterationStart.grid(column=0, row=4)      

        self.label_graph_iterationStop = Label(self.labelFrame_graph, text="Iteration to : ")
        self.label_graph_iterationStop.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_graph_iterationStop.grid(column=2, row=4)   

        self.label_marker_position = Label(self.labelFrame_graph, text="Position Marker : ")
        self.label_marker_position.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_marker_position.grid(column=0, row=5)    

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_signal1 = Combobox(self.labelFrame_signal1, state="readonly", width=25, values=["Pulse", "Ramp"])
        self.combo_signal1.bind("<<ComboboxSelected>>", self.combo_signal1_callback)
        self.combo_signal1.configure(background=self.resource.bgColor)
        self.combo_signal1.grid(column=0, row=0, columnspan=2, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_signal1.current(0)

        self.combo_signal2 = Combobox(self.labelFrame_signal2, state="readonly", width=25, values=["Pulse", "Ramp"])
        self.combo_signal2.bind("<<ComboboxSelected>>", self.combo_signal2_callback)
        self.combo_signal2.configure(background=self.resource.bgColor)
        self.combo_signal2.grid(column=0, row=0, columnspan=2, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_signal2.current(0)

        self.combo_graph1 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/time", "Current/time",
                                                                                                "Resistance/time", "Power/time",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "R/V curve", "Resistance/iteration",
                                                                                                "Resistance Histogram"])
        self.combo_graph1.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph1.configure(background=self.resource.bgColor)
        self.combo_graph1.grid(column=1, row=0, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph1.current(0)

        self.combo_graph2 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/time", "Current/time",
                                                                                                "Resistance/time", "Power/time",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "R/V curve", "Resistance/iteration",
                                                                                                "Resistance Histogram"])
        self.combo_graph2.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph2.configure(background=self.resource.bgColor)
        self.combo_graph2.grid(column=1, row=1, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph2.current(1)

        self.combo_graph3 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/time", "Current/time",
                                                                                                "Resistance/time", "Power/time",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "R/V curve", "Resistance/iteration",
                                                                                                "Resistance Histogram"])
        self.combo_graph3.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph3.configure(background=self.resource.bgColor)
        self.combo_graph3.grid(column=1, row=2, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph3.current(2)

        self.combo_graph4 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/time", "Current/time",
                                                                                                "Resistance/time", "Power/time",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "R/V curve", "Resistance/iteration",
                                                                                                "Resistance Histogram"])
        self.combo_graph4.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph4.configure(background=self.resource.bgColor)
        self.combo_graph4.grid(column=1, row=3, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph4.current(3)

        self.combo_iterationStart = Combobox(self.labelFrame_graph, state="readonly", width=5, values=[])
        self.combo_iterationStart.bind("<<ComboboxSelected>>", self.combo_iteration_callback)
        self.combo_iterationStart.configure(background=self.resource.bgColor)
        self.combo_iterationStart.grid(column=1, row=4, padx=self.resource.padx, pady=self.resource.pady)

        self.combo_iterationStop = Combobox(self.labelFrame_graph, state="readonly", width=5, values=[])
        self.combo_iterationStop.bind("<<ComboboxSelected>>", self.combo_iteration_callback)
        self.combo_iterationStop.configure(background=self.resource.bgColor)
        self.combo_iterationStop.grid(column=3, row=4, padx=self.resource.padx, pady=self.resource.pady)

    def combo_signal1_callback(self, args=[]):
    #This method is called when an action is made on combo_signal1  
        if self.combo_signal1.current() == 0:
            self.stringVar_signal1_param.set("Pulse width : ")
            self.doubleVar_signal1_startValue.set(0)
            self.doubleVar_signal1_stopValue.set(20)
            self.doubleVar_signal1_param.set(0.5)
            self.doubleVar_signal1_compliance.set(3)    

        elif self.combo_signal1.current() == 1:
            self.stringVar_signal1_param.set("Ramp : ")
            self.doubleVar_signal1_startValue.set(0)
            self.doubleVar_signal1_stopValue.set(15)
            self.doubleVar_signal1_param.set(3)
            self.doubleVar_signal1_compliance.set(0.5)
        
    def combo_signal2_callback(self, args=[]):
    #This method is called when an action is made on combo_signal2      
        if self.combo_signal2.current() == 0:
            self.stringVar_signal2_param.set("Pulse Width : ")
            self.doubleVar_signal2_startValue.set(0)
            self.doubleVar_signal2_stopValue.set(-20)
            self.doubleVar_signal2_param.set(0.5)
            self.doubleVar_signal2_compliance.set(300)

        elif self.combo_signal2.current() == 1:
            self.stringVar_signal2_param.set("Ramp : ")
            self.doubleVar_signal2_startValue.set(0)
            self.doubleVar_signal2_stopValue.set(15)
            self.doubleVar_signal2_param.set(3)
            self.doubleVar_signal2_compliance.set(0.5)

    def combo_graph_callback(self, args=[]):
    #This method is called when an action is made on combo_graph
        self.graph_TL.frame.grid_forget()
        self.graph_TR.frame.grid_forget()
        self.graph_BL.frame.grid_forget()
        self.graph_BR.frame.grid_forget()

        self.graph_TL = self.Graph[self.combo_graph1.current()]
        self.graph_TR = self.Graph[self.combo_graph2.current()]
        self.graph_BL = self.Graph[self.combo_graph3.current()]
        self.graph_BR = self.Graph[self.combo_graph4.current()]

        self.graph_TL.frame.grid(column=2, row=0, rowspan=4)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=4)
        self.graph_BL.frame.grid(column=2, row=4, rowspan=4)
        self.graph_BR.frame.grid(column=3, row=4, rowspan=4)

        self.printResult()

    def combo_iteration_callback(self, args=[]):
    #Callback method for combo Iteration
        self.printResult()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_ramp_startValue = Entry(self.labelFrame_signal1, textvariable=self.doubleVar_signal1_startValue, width=12)
        self.entry_ramp_startValue.grid(column=1, row=1, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_ramp_stopValue = Entry(self.labelFrame_signal1, textvariable=self.doubleVar_signal1_stopValue, width=12)
        self.entry_ramp_stopValue.grid(column=1, row=2, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_ramp_param = Entry(self.labelFrame_signal1, textvariable=self.doubleVar_signal1_param, width=12)
        self.entry_ramp_param.grid(column=1, row=3, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_ramp_compliance = Entry(self.labelFrame_signal1, textvariable=self.doubleVar_signal1_compliance, width=12)
        self.entry_ramp_compliance.grid(column=1, row=4, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_startValue = Entry(self.labelFrame_signal2, textvariable=self.doubleVar_signal2_startValue, width=12)
        self.entry_pulse_startValue.grid(column=1, row=1, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_stopValue = Entry(self.labelFrame_signal2, textvariable=self.doubleVar_signal2_stopValue, width=12)
        self.entry_pulse_stopValue.grid(column=1, row=2, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_param = Entry(self.labelFrame_signal2, textvariable=self.doubleVar_signal2_param , width=12)
        self.entry_pulse_param.grid(column=1, row=3, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_pulse_compliance = Entry(self.labelFrame_signal2, textvariable=self.doubleVar_signal2_compliance, width=12)
        self.entry_pulse_compliance.grid(column=1, row=4, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=25)
        self.entry_CBRAM_ident.grid(column=1, row=4, pady=self.resource.pady, padx=self.resource.padx)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12)
        self.entry_CBRAM_resistance.grid(column=1, row=5, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_marker_position = Entry(self.labelFrame_graph, textvariable=self.intVar_marker_position, width=15)
        self.entry_marker_position.grid(column=1, row=5, pady=self.resource.pady)

    def printResult(self):
    #This method add results to Graphs
        self.Graph[0].clearGraph()
        self.Graph[1].clearGraph()
        self.Graph[2].clearGraph()
        self.Graph[3].clearGraph()
        self.Graph[4].clearGraph()
        self.Graph[5].clearGraph()       
        self.Graph[6].clearGraph()      
        self.Graph[7].clearGraph()    
        self.Graph[8].clearGraph()

        istart = self.combo_iterationStart.current()        
        istop = self.combo_iterationStop.current()

        source = []
        sense = []
        resistance = []

        i = istart
        while i <= istop :
            source = source + (self.results.signal_1[i])
            sense = sense + (self.results.signal_2[i])
            i+=1

        source = asarray(source)
        sense = asarray(sense)
        resistance_time = abs(asarray(source / sense))
        resistance = asarray(self.results.resistance[istart:istop])
        power = asarray(source * sense)

        marker = [self.intVar_marker_position.get()]
        length = len(source)   
        time = linspace(0, length*self.resource.stepDelay, length)
        iteration = linspace(0, len(resistance), len(resistance))

        self.Graph[0].addStepGraph(x=time, xlabel="time",
                                   y=source / self.results.voltCoeff, ylabel=self.resource.source,
                                   color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 
        self.Graph[1].addStepGraph(x=time, xlabel="time",
                                   y=sense / self.results.currCoeff, ylabel=self.resource.sense,
                                   color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 

        self.Graph[2].addLinGraph(x=time, xlabel="time",
                                  y=self.resource.R_low_lim*ones(len(time)), color="red", grid=self.resource.Graph_grid, marker_pos=marker) 
        self.Graph[2].addLinGraph(x=time, xlabel="time",
                                  y=self.resource.R_high_lim*ones(len(time)), color="red", grid=self.resource.Graph_grid, marker_pos=marker) 
        self.Graph[2].addLinGraph(x=time, xlabel="time",
                                  y=resistance_time / self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 

        self.Graph[3].addStepGraph(x=time, xlabel="time",
                                   y=power / self.results.powerCoeff, ylabel="Power",
                                   color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 

        self.Graph[4].addLinGraph(x=source / self.resource.voltCoeff, xlabel="Voltage",
                                  y=sense / self.resource.currCoeff, ylabel="Current",
                                  color="orange", grid=self.resource.Graph_grid)
        self.Graph[5].addLinGraph(x=source / self.resource.voltCoeff, xlabel="Voltage",
                                  y=abs(sense)/self.resource.currCoeff, ylabel="Current",
                                  yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 
                                  
        self.Graph[6].addLinGraph(x=source/self.resource.voltCoeff, xlabel="Voltage",
                                  y=resistance_time / self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 
         
        self.Graph[7].addLinGraph(x=iteration, xlabel="Iteration",
                                  y=self.resource.R_low_lim*ones(len(iteration)), color="red", grid=self.resource.Graph_grid) 
        self.Graph[7].addLinGraph(x=iteration, xlabel="Iteration",
                                  y=self.resource.R_high_lim*ones(len(iteration)), color="red", grid=self.resource.Graph_grid)                        
        self.Graph[7].addScatteredGraph(x=iteration, xlabel="Iteration",
                                  y=resistance / self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="orange", grid=self.resource.Graph_grid)   

        self.Graph[8].addGraph(x=resistance, xlabel="Resistance",
                               ylabel="Iteration", xscale="log",
                               color="orange", grid=self.resource.Graph_grid)

        self.Graph[0].setIteration(istart+1, istop+1)
        self.Graph[1].setIteration(istart+1, istop+1)
        self.Graph[2].setIteration(istart+1, istop+1)
        self.Graph[3].setIteration(istart+1, istop+1)
        self.Graph[4].setIteration(istart+1, istop+1)
        self.Graph[5].setIteration(istart+1, istop+1)
        self.Graph[6].setIteration(istart+1, istop+1)

    def loadResults(self):
    #This methods loads results into the different widgets
        self.doubleVar_signal1_startValue.set(self.results.ramp_start_value)
        self.doubleVar_signal1_stopValue.set(self.results.ramp_stop_value)
        self.doubleVar_signal1_param.set(self.results.ramp_param)
        self.doubleVar_signal1_compliance.set(self.results.ramp_compliance)

        self.doubleVar_signal2_startValue.set(self.results.pulse_start_value)
        self.doubleVar_signal2_stopValue.set(self.results.pulse_stop_value)
        self.doubleVar_signal2_param .set(self.results.pulse_param)
        self.doubleVar_signal2_compliance.set(self.results.pulse_compliance)

        self.stringVar_CBRAM_ident.set(self.results.cell_ident)
        self.doubleVar_CBRAM_resistance.set(self.results.cell_resistance)

        self.combo_iterationStart.config(values=linspace(1,self.results.iteration-1, self.results.iteration-1).tolist())
        self.combo_iterationStart.current(0)
        self.combo_iterationStop.config(values=linspace(1,self.results.iteration-1, self.results.iteration-1).tolist())
        self.combo_iterationStop.current(0)

        self.printResult()