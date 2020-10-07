"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for the CBRAM Modelling. Modelling sequence is made to extract physical parameters from previous test results. It is based on a numerical
model developped by YU at Stanford University.

"""

import pickle
import json

from Sequence import Sequence

from Graph import Graph
from CBRAM import CBRAM

from tkinter import Label
from tkinter import LabelFrame
from tkinter import Button
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog

from numpy import ones
from numpy import linspace
from numpy import asarray
import numpy as np

class Modelling(Sequence):
    """Class containing the Modelling sequence.

    """

    def __init__(self, root, resource, terminal):
    #Constructor for the Single class
        Sequence.__init__(self, root, resource, terminal)
        self.state = "Modelling"
        self.CBRAM = CBRAM()

        self.__initWidgets()
        self.button_simulate_callBack()

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
        self.Graph = [Graph(self.frame, self.resource, "Voltage"),
                      Graph(self.frame, self.resource, "Current"),
                      Graph(self.frame, self.resource, "I/V Curve"),
                      Graph(self.frame, self.resource, "Butterfly Curve"),
                      Graph(self.frame, self.resource, "I/V Curve (Command)"),
                      Graph(self.frame, self.resource, "Butterfly Curve (Command)"),
                      Graph(self.frame, self.resource, "R/V Curve"),
                      Graph(self.frame, self.resource, "R/V Curve (Command)"),
                      Graph(self.frame, self.resource, "Resistance"),
                      Graph(self.frame, self.resource, "Resistance (Command)"),
                      Graph(self.frame, self.resource, "Power"),
                      Graph(self.frame, self.resource, "Temperature"),
                      Graph(self.frame, self.resource, "T/V curve")]
       
        self.graph_TL = self.Graph[0]
        self.graph_TR = self.Graph[1]
        self.graph_BL = self.Graph[2]
        self.graph_BR = self.Graph[3]

        self.Graph[4].frame.grid_forget()
        self.Graph[5].frame.grid_forget()
        self.Graph[6].frame.grid_forget()
        self.Graph[7].frame.grid_forget()
        self.Graph[8].frame.grid_forget()
        self.Graph[9].frame.grid_forget()
        self.Graph[10].frame.grid_forget()
        self.Graph[11].frame.grid_forget()
        self.Graph[12].frame.grid_forget()

        self.graph_TL.frame.grid(column=2, row=0, rowspan=6)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=6)
        self.graph_BL.frame.grid(column=2, row=6, rowspan=6)
        self.graph_BR.frame.grid(column=3, row=6, rowspan=6)

    def __initLabelFrames(self):
    #This method instanciates all the LabelFrames used in the Cycling test bench GUI
        self.labelFrame_geometry = LabelFrame(self.frame, text="Cell's geometry")
        self.labelFrame_geometry.configure(bg=self.resource.bgColor)
        self.labelFrame_geometry.grid(column=0, columnspan=2, row=3, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_fitting = LabelFrame(self.frame, text="Fitting parameters")
        self.labelFrame_fitting.configure(bg=self.resource.bgColor)
        self.labelFrame_fitting.grid(column=0, columnspan=2, row=4, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_physical = LabelFrame(self.frame, text="Physical parameters")
        self.labelFrame_physical.configure(bg=self.resource.bgColor)
        self.labelFrame_physical.grid(column=0, columnspan=2, row=5, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_signal_set = LabelFrame(self.frame, text="Set Signal")
        self.labelFrame_signal_set.configure(bg=self.resource.bgColor)
        self.labelFrame_signal_set.grid(column=0, columnspan=1, row=6, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_signal_reset = LabelFrame(self.frame, text="Reset Signal")
        self.labelFrame_signal_reset.configure(bg=self.resource.bgColor)
        self.labelFrame_signal_reset.grid(column=1, columnspan=1, row=6, padx=self.resource.padx, pady=self.resource.pady)

        self.labelFrame_graph = LabelFrame(self.frame, text="Graphs")
        self.labelFrame_graph.configure(bg=self.resource.bgColor)
        self.labelFrame_graph.grid(column=0, columnspan=2, row=8, padx=self.resource.padx, pady=self.resource.pady)
        
    def __initButtons(self):
    #This method instanciates all the buttons used by the Cycling test bench GUI
        self.button_graph_actualizeGraphs = Button(self.labelFrame_graph, text="Actualize Graphs", command=self.button_graph_actualizeGraphs_callBack, padx=5, pady=10)
        self.button_graph_actualizeGraphs.grid(column=1, columnspan=2, row=5, pady=self.resource.pady)

        self.button_extract = Button(self.frame, text="Extract from result file", command=self.button_extract_callBack, padx=5, pady=10)
        self.button_extract.grid(column=0, row=7, padx=self.resource.padx, pady=self.resource.pady)

        self.button_simulate = Button(self.frame, text="Simulate", command=self.button_simulate_callBack, padx=5, pady=10)
        self.button_simulate.grid(column=1, row=7, padx=self.resource.padx, pady=self.resource.pady)
        
    def button_graph_actualizeGraphs_callBack(self, args=[]):
    #Callback method for actualizeGraphs buttons
        self.button_simulate_callBack()
        self.combo_graph_callback()

    def button_extract_callBack(self):
    #This method is a callBack function for button_extract    
        path =  filedialog.askopenfilename(title = "Select file",filetypes = (("Binary results files","*.pickle"), ("Text results files","*.txt"), ("all files","*.*")))
        if path != "":
            File = open(path, 'rb')
            self.results = pickle.load(File)
            File.close()

        self.stringVar_CBRAM_ident.set(self.results.cell_ident)
        self.doubleVar_CBRAM_resistance.set(self.results.cell_resistance)

        tampon = self.stringVar_CBRAM_ident.get().split(":")

        if "u" in tampon[0]:
            value = float(tampon[0][:-1])
            self.doubleVar_Cu_th.set(format(value * 1e-6, '.4g'))
        elif "n" in tampon[0]:
            value = float(tampon[0][:-1])
            self.doubleVar_Cu_th.set(format(value * 1e-9, '.4g'))
        
        if "u" in tampon[1]:
            value = float(tampon[1][:-1])
            self.doubleVar_Nafion_th.set(format(value * 1e-6, '.4g'))
        elif "n" in tampon[1]:
            value = float(tampon[1][:-1])
            self.doubleVar_Nafion_th.set(format(value * 1e-9, '.4g'))
        
        if "u" in tampon[2]:
            value = float(tampon[2][:-1])
            self.doubleVar_Al_th.set(format(value * 1e-6, '.4g'))
        elif "n" in tampon[2]:
            value = float(tampon[2][:-1])
            self.doubleVar_Al_th.set(format(value * 1e-9, '.4g'))

        Fresistance = self.controller.filterResultSignal(asarray(self.results.signal_1) / asarray(self.results.signal_2))

        Rmax = max(abs(Fresistance))
        Rmin = min(abs(Fresistance))

        rho_off = abs(Rmax) * (np.pi * (self.doubleVar_ext_radius.get())**2) / self.doubleVar_Nafion_th.get()
        rho_on = abs(Rmin) * (np.pi * (self.doubleVar_CF_radius.get()*3)**2) / self.doubleVar_Nafion_th.get()

        self.doubleVar_resistivity_off_ohm.set(format(rho_off, '.4g'))
        self.doubleVar_resistivity_on.set(format(rho_on, '.4g'))

        self.doubleVar_peakValue_set.set(self.results.ramp_stop_value)
        self.doubleVar_ramp_set.set(self.results.ramp_param)                    
        self.doubleVar_compliance_set.set(self.results.ramp_compliance )

        try:
            self.doubleVar_peakValue_reset.set(self.results.pulse_stop_value)
            self.doubleVar_ramp_reset.set(self.results.pulse_param)                    
            self.doubleVar_compliance_reset.set(self.results.pulse_compliance)
        except :
            print("exception")

        if self.results.pulse_compliance == 0:
            self.doubleVar_peakValue_reset.set(self.results.ramp_stop_value)
            self.doubleVar_ramp_reset.set(self.results.ramp_param)                    
            self.doubleVar_compliance_reset.set(self.results.ramp_compliance )

        self.button_simulate_callBack()
        
    def button_simulate_callBack(self, args=[]):
    #This method is a callBack funtion for button_simulate
        self.CBRAM.Al_th = float(self.entry_Al_th.get())
        self.CBRAM.Cu_th = float(self.entry_Cu_th.get())
        self.CBRAM.nafion_th = float(self.entry_Nafion_th.get())
        self.CBRAM.ext_radius = float(self.entry_ext_radius.get())
        self.CBRAM.CF_radius = float(self.entry_CF_radius.get())
        self.CBRAM.velocity_h = float(self.entry_velocity_h.get())
        self.CBRAM.alpha = float(self.entry_alpha.get())
        self.CBRAM.velocity_r = float(self.entry_velocity_r.get())
        self.CBRAM.beta = float(self.entry_beta.get())
        self.CBRAM.sigmaPF = float(self.entry_sigmaPF.get())
        self.CBRAM.phiPF = float(self.entry_phiPF.get())
        self.CBRAM.temperature = float(self.entry_temperature.get())
        self.CBRAM.thermal_resistance = float(self.entry_thermal_resistance.get())
        self.CBRAM.resistivity_on = float(self.entry_resistivity_on.get())
        self.CBRAM.resistivity_off_ohm = float(self.entry_resistivity_off_ohm.get())
        self.CBRAM.resistivity_off_PF = float(self.entry_resistivity_off_PF.get())
        self.CBRAM.negative_offset = float(self.entry_negative_offset.get())
        self.CBRAM.negative_offset_threshold = float(self.entry_negative_offset_threshold.get())

        self.results.cell_ident = self.stringVar_CBRAM_ident.get()

        self.results.ramp_stop_value = self.doubleVar_peakValue_set.get()
        self.results.ramp_param = self.doubleVar_ramp_set.get()                    
        self.results.ramp_compliance = self.doubleVar_compliance_set.get()
        self.results.pulse_stop_value = self.doubleVar_peakValue_reset.get()
        self.results.pulse_param = self.doubleVar_ramp_reset.get()                    
        self.results.pulse_compliance = self.doubleVar_compliance_reset.get()

        [self.time, self.signal, self.index_Ilim2] = self.controller.generateTriangularSequence(self.doubleVar_peakValue_set.get(), self.doubleVar_ramp_set.get(),self.doubleVar_peakValue_reset.get(), self.doubleVar_ramp_reset.get())
        [signal, I, R, h, dh, r, dr, T, problem] = self.service.simulateVoltageWaveform(self.signal*self.resource.voltCoeff, self.doubleVar_compliance_set.get()*self.resource.currCoeff, self.doubleVar_compliance_reset.get()*self.resource.currCoeff, self.CBRAM)

        if problem == 1:
            messagebox.showwarning(title = "Simulation error", message="Cannot solve compliance current.")

        else:
            self.printSimulation(signal, I, R, T)

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("35u:1000n:600n:ddmmyyss:00x00")

        self.doubleVar_Nafion_th = DoubleVar()
        self.doubleVar_Nafion_th.set(1e-6)

        self.doubleVar_Cu_th = DoubleVar()
        self.doubleVar_Cu_th.set(35e-6)

        self.doubleVar_Al_th = DoubleVar()
        self.doubleVar_Al_th.set(1e-6)

        self.doubleVar_ext_radius = DoubleVar()
        self.doubleVar_ext_radius.set(1e-3)

        self.doubleVar_CF_radius = DoubleVar()
        self.doubleVar_CF_radius.set(33e-9)

        self.doubleVar_velocity_h = DoubleVar()
        self.doubleVar_velocity_h.set(15)

        self.doubleVar_alpha = DoubleVar()
        self.doubleVar_alpha.set(8e-2)

        self.doubleVar_velocity_r = DoubleVar()
        self.doubleVar_velocity_r.set(30)

        self.doubleVar_beta = DoubleVar()
        self.doubleVar_beta.set(0.012)

        self.doubleVar_sigmaPF = DoubleVar()
        self.doubleVar_sigmaPF.set(150)

        self.doubleVar_phiPF = DoubleVar()
        self.doubleVar_phiPF.set(0.015)

        self.doubleVar_temperature = DoubleVar()
        self.doubleVar_temperature.set(300)

        self.doubleVar_thermal_resistance = DoubleVar()
        self.doubleVar_thermal_resistance.set(format(1e5, '.4g'))

        self.doubleVar_negative_offset= DoubleVar()
        self.doubleVar_negative_offset.set(0)

        self.doubleVar_negative_offset_threshold = DoubleVar()
        self.doubleVar_negative_offset_threshold.set(0)

        self.doubleVar_resistivity_on = DoubleVar()
        self.doubleVar_resistivity_on.set(7e-6)

        self.doubleVar_resistivity_off_ohm = DoubleVar()
        self.doubleVar_resistivity_off_ohm.set(format(3e7, '.4g'))

        self.doubleVar_resistivity_off_PF = DoubleVar()
        self.doubleVar_resistivity_off_PF.set(format(1e8, '.4g'))

        self.doubleVar_peakValue_set = DoubleVar()
        self.doubleVar_peakValue_set.set(5)

        self.doubleVar_ramp_set = DoubleVar()
        self.doubleVar_ramp_set.set(5)

        self.doubleVar_compliance_set = DoubleVar()
        self.doubleVar_compliance_set.set(0.5)

        self.doubleVar_peakValue_reset = DoubleVar()
        self.doubleVar_peakValue_reset.set(5)

        self.doubleVar_ramp_reset = DoubleVar()
        self.doubleVar_ramp_reset.set(5)

        self.doubleVar_compliance_reset = DoubleVar()
        self.doubleVar_compliance_reset.set(0.5)

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)

        self.intVar_marker_position = IntVar()
        self.intVar_marker_position.set(0)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_CBRAM_ident = Label(self.frame, text="CBRAM cell's identifier : ")
        self.label_CBRAM_ident.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_ident.grid(column=0, row=1)

        self.label_CBRAM_resistance = Label(self.frame, text = "CBRAM cell's resistance : ")
        self.label_CBRAM_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_resistance.grid(column=0, row=2)

        self.label_Nafion_th = Label(self.labelFrame_geometry, text = "Nafion's thickness (m) : ")
        self.label_Nafion_th.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_Nafion_th.grid(column=0, row=0)

        self.label_Cu_th = Label(self.labelFrame_geometry, text = "Copper's thickness (m) : ")
        self.label_Cu_th.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_Cu_th.grid(column=0, row=1)

        self.label_Al_th = Label(self.labelFrame_geometry, text = "Aluminium's thickness (m) : ")
        self.label_Al_th.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_Al_th.grid(column=0, row=2)

        self.label_ext_radius = Label(self.labelFrame_geometry, text = "Cell's Radius (m) : ")
        self.label_ext_radius.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ext_radius.grid(column=0, row=3)

        self.label_CF_radius = Label(self.labelFrame_geometry, text = "Filament's base Radius (m) : ")
        self.label_CF_radius.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CF_radius.grid(column=0, row=4)

        self.label_velocity_h = Label(self.labelFrame_fitting, text = "Vh (m/s) : ")
        self.label_velocity_h.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_velocity_h.grid(column=0, row=0)

        self.label_alpha = Label(self.labelFrame_fitting, text = "Alpha : ")
        self.label_alpha.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_alpha.grid(column=2, row=0)

        self.label_velocity_r = Label(self.labelFrame_fitting, text = "Vr (m/s) : ")
        self.label_velocity_r.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_velocity_r.grid(column=0, row=1)

        self.label_beta = Label(self.labelFrame_fitting, text = "Beta : ")
        self.label_beta.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_beta.grid(column=2, row=1)

        self.label_sigmaPF = Label(self.labelFrame_fitting, text = "Sigma PF : ")
        self.label_sigmaPF.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_sigmaPF.grid(column=0, row=2)

        self.label_phiPF = Label(self.labelFrame_fitting, text = "Phi PF : ")
        self.label_phiPF.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_phiPF.grid(column=2, row=2)

        self.label_temperature = Label(self.labelFrame_fitting, text = "Temperature (K) : ")
        self.label_temperature.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_temperature.grid(column=0, row=3)

        self.label_thermal_resistance = Label(self.labelFrame_fitting, text = "Rth : ")
        self.label_thermal_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_thermal_resistance.grid(column=2, row=3)

        self.label_negative_offset = Label(self.labelFrame_fitting, text = "Negative Offset (V): ")
        self.label_negative_offset.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_negative_offset.grid(column=0, row=4)

        self.label_negative_offset_threshold = Label(self.labelFrame_fitting, text = "Threshold (V) : ")
        self.label_negative_offset_threshold .configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_negative_offset_threshold .grid(column=2, row=4)

        self.label_resistivity_on = Label(self.labelFrame_physical, text = "ON Resistivity (Ohm/m) : ")
        self.label_resistivity_on.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_resistivity_on.grid(column=0, row=0)

        self.label_resistivity_off_ohm = Label(self.labelFrame_physical, text = "Ohm OFF Resistivity (Ohm/m) : ")
        self.label_resistivity_off_ohm.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_resistivity_off_ohm.grid(column=0, row=1)

        self.label_resistivity_off_PF = Label(self.labelFrame_physical, text = "PF OFF Resistivity (Ohm/m) : ")
        self.label_resistivity_off_PF.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_resistivity_off_PF.grid(column=0, row=2)

        self.label_peakValue_set = Label(self.labelFrame_signal_set, text = "Peak Value : ")
        self.label_peakValue_set.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_peakValue_set.grid(column=0, row=0)

        self.label_ramp_set = Label(self.labelFrame_signal_set, text = "Ramp : ")
        self.label_ramp_set.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_set.grid(column=0, row=1)

        self.label_compliance_set = Label(self.labelFrame_signal_set, text = "Compliance : ")
        self.label_compliance_set.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_compliance_set.grid(column=0, row=2)

        self.label_peakValue_reset = Label(self.labelFrame_signal_reset, text = "Peak Value : ")
        self.label_peakValue_reset.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_peakValue_reset.grid(column=0, row=0)

        self.label_ramp_reset = Label(self.labelFrame_signal_reset, text = "Ramp : ")
        self.label_ramp_reset.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_ramp_reset.grid(column=0, row=1)

        self.label_compliance_reset = Label(self.labelFrame_signal_reset, text = "Compliance : ")
        self.label_compliance_reset.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_compliance_reset.grid(column=0, row=2)

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

        self.label_marker_position = Label(self.labelFrame_graph, text="Position Marker : ")
        self.label_marker_position.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_marker_position.grid(column=0, row=4)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_graph1 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "I/V curve (Command)", "Butterfly curve (Command)",
                                                                                                "R/V curve", "R/V curve (Command)",
                                                                                                "Resistance/iteration", "Resistance/iteration (Command)",
                                                                                                "Power/iteration", "Temperature", "T/V curve"])
        self.combo_graph1.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph1.configure(background=self.resource.bgColor)
        self.combo_graph1.grid(column=1, row=0, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph1.current(0)

        self.combo_graph2 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "I/V curve (Command)", "Butterfly curve (Command)",
                                                                                                "R/V curve", "R/V curve (Command)",
                                                                                                "Resistance/iteration", "Resistance/iteration (Command)",
                                                                                                "Power/iteration", "Temperature", "T/V curve"])
        self.combo_graph2.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph2.configure(background=self.resource.bgColor)
        self.combo_graph2.grid(column=1, row=1, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph2.current(1)

        self.combo_graph3 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "I/V curve (Command)", "Butterfly curve (Command)",
                                                                                                "R/V curve", "R/V curve (Command)",
                                                                                                "Resistance/iteration", "Resistance/iteration (Command)",
                                                                                                "Power/iteration", "Temperature", "T/V curve"])
        self.combo_graph3.bind("<<ComboboxSelected>>", self.combo_graph_callback)
        self.combo_graph3.configure(background=self.resource.bgColor)
        self.combo_graph3.grid(column=1, row=2, columnspan=3, padx=self.resource.padx, pady=self.resource.pady)
        self.combo_graph3.current(2)

        self.combo_graph4 = Combobox(self.labelFrame_graph, state="readonly", width=25, values=["Voltage/iteration", "Current/iteration",
                                                                                                "I/V curve", "Butterfly curve",
                                                                                                "I/V curve (Command)", "Butterfly curve (Command)",
                                                                                                "R/V curve", "R/V curve (Command)",
                                                                                                "Resistance/iteration", "Resistance/iteration (Command)",
                                                                                                "Power/iteration", "Temperature", "T/V curve"])
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

        self.graph_TL.frame.grid(column=2, row=0, rowspan=6)
        self.graph_TR.frame.grid(column=3, row=0, rowspan=6)
        self.graph_BL.frame.grid(column=2, row=6, rowspan=6)
        self.graph_BR.frame.grid(column=3, row=6, rowspan=6)

        if self.intVar_marker_position.get() > len(self.signal):
            self.intVar_marker_position.set(len(self.signal))
        elif self.intVar_marker_position.get() < 0:
            self.intVar_marker_position.set(0)

        self.button_simulate_callBack()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=30)
        self.entry_CBRAM_ident.grid(column=1, row=1, padx=self.resource.padx)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12, state="readonly")
        self.entry_CBRAM_resistance.grid(column=1, row=2, padx=self.resource.padx)

        self.entry_Nafion_th = Entry(self.labelFrame_geometry, textvariable=self.doubleVar_Nafion_th, width=10)
        self.entry_Nafion_th.grid(column=1, row=0, padx=self.resource.padx)
        self.entry_Nafion_th.bind("<Return>", self.button_simulate_callBack)        

        self.entry_Cu_th = Entry(self.labelFrame_geometry, textvariable=self.doubleVar_Cu_th,width=10)
        self.entry_Cu_th.grid(column=1, row=1, padx=self.resource.padx)
        self.entry_Cu_th.bind("<Return>", self.button_simulate_callBack)

        self.entry_Al_th = Entry(self.labelFrame_geometry, textvariable=self.doubleVar_Al_th, width=10)
        self.entry_Al_th.grid(column=1, row=2, padx=self.resource.padx)
        self.entry_Al_th.bind("<Return>", self.button_simulate_callBack)

        self.entry_ext_radius = Entry(self.labelFrame_geometry, textvariable=self.doubleVar_ext_radius, width=10)
        self.entry_ext_radius.grid(column=1, row=3, padx=self.resource.padx)
        self.entry_ext_radius.bind("<Return>", self.button_simulate_callBack)

        self.entry_CF_radius = Entry(self.labelFrame_geometry, textvariable=self.doubleVar_CF_radius, width=10)
        self.entry_CF_radius.grid(column=1, row=4, padx=self.resource.padx)
        self.entry_CF_radius.bind("<Return>", self.button_simulate_callBack)

        self.entry_velocity_h = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_velocity_h, width=7)
        self.entry_velocity_h.grid(column=1, row=0, padx=self.resource.padx)
        self.entry_velocity_h.bind("<Return>", self.button_simulate_callBack)

        self.entry_alpha = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_alpha, width=7)
        self.entry_alpha.grid(column=3, row=0, padx=self.resource.padx)
        self.entry_alpha.bind("<Return>", self.button_simulate_callBack)

        self.entry_velocity_r = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_velocity_r, width=7)
        self.entry_velocity_r.grid(column=1, row=1, padx=self.resource.padx)
        self.entry_velocity_r.bind("<Return>", self.button_simulate_callBack)

        self.entry_beta = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_beta, width=7)
        self.entry_beta.grid(column=3, row=1, padx=self.resource.padx)
        self.entry_beta.bind("<Return>", self.button_simulate_callBack)

        self.entry_sigmaPF = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_sigmaPF, width=7)
        self.entry_sigmaPF.grid(column=1, row=2, padx=self.resource.padx)
        self.entry_sigmaPF.bind("<Return>", self.button_simulate_callBack)

        self.entry_phiPF = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_phiPF, width=7)
        self.entry_phiPF.grid(column=3, row=2, padx=self.resource.padx)
        self.entry_phiPF.bind("<Return>", self.button_simulate_callBack)

        self.entry_temperature = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_temperature, width=5)
        self.entry_temperature.grid(column=1, row=3, padx=self.resource.padx)
        self.entry_temperature.bind("<Return>", self.button_simulate_callBack)

        self.entry_thermal_resistance = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_thermal_resistance, width=8)
        self.entry_thermal_resistance.grid(column=3, row=3, padx=self.resource.padx)
        self.entry_thermal_resistance.bind("<Return>", self.button_simulate_callBack)

        self.entry_negative_offset = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_negative_offset, width=5)
        self.entry_negative_offset.grid(column=1, row=4, padx=self.resource.padx)
        self.entry_negative_offset.bind("<Return>", self.button_simulate_callBack)

        self.entry_negative_offset_threshold = Entry(self.labelFrame_fitting, textvariable=self.doubleVar_negative_offset_threshold, width=5)
        self.entry_negative_offset_threshold.grid(column=3, row=4, padx=self.resource.padx)
        self.entry_negative_offset_threshold.bind("<Return>", self.button_simulate_callBack)

        self.entry_resistivity_on = Entry(self.labelFrame_physical, textvariable=self.doubleVar_resistivity_on, width=10)
        self.entry_resistivity_on.grid(column=1, row=0, padx=self.resource.padx)
        self.entry_resistivity_on.bind("<Return>", self.button_simulate_callBack)

        self.entry_resistivity_off_ohm = Entry(self.labelFrame_physical, textvariable=self.doubleVar_resistivity_off_ohm, width=10)
        self.entry_resistivity_off_ohm.grid(column=1, row=1, padx=self.resource.padx)
        self.entry_resistivity_off_ohm.bind("<Return>", self.button_simulate_callBack)

        self.entry_resistivity_off_PF = Entry(self.labelFrame_physical, textvariable=self.doubleVar_resistivity_off_PF, width=10)
        self.entry_resistivity_off_PF.grid(column=1, row=2, padx=self.resource.padx)
        self.entry_resistivity_off_PF.bind("<Return>", self.button_simulate_callBack)

        self.entry_peakValue_set = Entry(self.labelFrame_signal_set, textvariable=self.doubleVar_peakValue_set, width=6)
        self.entry_peakValue_set.grid(column=1, row=0, pady=self.resource.pady)
        self.entry_peakValue_set.bind("<Return>", self.button_simulate_callBack)

        self.entry_ramp_set = Entry(self.labelFrame_signal_set, textvariable=self.doubleVar_ramp_set, width=6)
        self.entry_ramp_set.grid(column=1, row=1, pady=self.resource.pady)
        self.entry_ramp_set.bind("<Return>", self.button_simulate_callBack)

        self.entry_compliance_set = Entry(self.labelFrame_signal_set, textvariable=self.doubleVar_compliance_set, width=6)
        self.entry_compliance_set.grid(column=1, row=2, pady=self.resource.pady)
        self.entry_compliance_set.bind("<Return>", self.button_simulate_callBack)

        self.entry_peakValue_reset = Entry(self.labelFrame_signal_reset, textvariable=self.doubleVar_peakValue_reset, width=6)
        self.entry_peakValue_reset.grid(column=1, row=0, pady=self.resource.pady)
        self.entry_peakValue_reset.bind("<Return>", self.button_simulate_callBack)

        self.entry_ramp_reset = Entry(self.labelFrame_signal_reset, textvariable=self.doubleVar_ramp_reset, width=6)
        self.entry_ramp_reset.grid(column=1, row=1, pady=self.resource.pady)
        self.entry_ramp_reset.bind("<Return>", self.button_simulate_callBack)

        self.entry_compliance_reset = Entry(self.labelFrame_signal_reset, textvariable=self.doubleVar_compliance_reset, width=6)
        self.entry_compliance_reset.grid(column=1, row=2, pady=self.resource.pady)
        self.entry_compliance_reset.bind("<Return>", self.button_simulate_callBack)

        self.entry_marker_position = Entry(self.labelFrame_graph, textvariable=self.intVar_marker_position, width=4)
        self.entry_marker_position.grid(column=1, row=4, pady=self.resource.pady)
        self.entry_marker_position.bind("<Return>", self.button_graph_actualizeGraphs_callBack)
    
    def printSimulation(self, signal, I, R, Temperature):
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
        self.Graph[9].clearGraph()
        self.Graph[10].clearGraph()
        self.Graph[11].clearGraph()
        self.Graph[12].clearGraph()
        
        marker = [self.intVar_marker_position.get()]
        time = linspace(0, len(signal)*self.resource.stepDelay, len(signal))

        for elem in self.results.signal_1:
            if elem == 0:
                elem = 1e-6

        if len(self.results.signal_1) != 0:

            self.Graph[0].addStepGraph(x=time, xlabel="time",
                                    y=asarray(self.results.signal_1)/self.resource.voltCoeff,
                                    ylabel=self.resource.source, color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[1].addStepGraph(x=time, xlabel="time",
                                       y=asarray(self.results.signal_2)/self.resource.currCoeff,
                                       ylabel=self.resource.sense, color="orange", grid=self.resource.Graph_grid, marker_pos=marker) 
            self.Graph[2].addLinGraph(x=asarray(self.results.signal_1)/self.resource.voltCoeff, xlabel="Voltage",
                                    y=asarray(self.results.signal_2)/self.resource.currCoeff, ylabel="Current",
                                    color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[3].addLinGraph(x=asarray(self.results.signal_1)/self.resource.voltCoeff, xlabel="Voltage",
                                    y=abs(asarray(self.results.signal_2))/self.resource.currCoeff, ylabel="Current",
                                    yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[4].addLinGraph(x=asarray(self.signal)/self.resource.voltCoeff, xlabel="Voltage (Command)",
                                    y=asarray(self.results.signal_2)/self.resource.currCoeff, ylabel="Current",
                                    color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[5].addLinGraph(x=asarray(self.signal)/self.resource.voltCoeff, xlabel="Voltage (Command)",
                                    y=abs(asarray(self.results.signal_2))/self.resource.currCoeff, ylabel="Current",
                                    yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[6].addLinGraph(x=asarray(self.results.signal_1)/self.resource.voltCoeff, xlabel="Voltage",
                                    y=abs((asarray(self.results.signal_1)/self.results.signal_2))/self.resource.resistanceCoeff, ylabel="Resistance",
                                    yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[7].addLinGraph(x=asarray(self.signal)/self.resource.voltCoeff, xlabel="Voltage (Command)",
                                    y=abs((asarray(self.results.signal_1)/self.results.signal_2))/self.resource.resistanceCoeff, ylabel="Resistance",
                                    yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
        
            self.Graph[8].addLinGraph(x=time, xlabel="time",
                                    y=abs((asarray(self.results.signal_1)/self.results.signal_2))/self.resource.resistanceCoeff, ylabel="Resistance",
                                    yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[9].addLinGraph(x=time, xlabel="time",
                                    y=abs((asarray(self.results.signal_1)/self.results.signal_2))/self.resource.resistanceCoeff, ylabel="Resistance (Command)",
                                    yscale="log", color="orange", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[10].addStepGraph(x=time, xlabel="time",
                                    y=(asarray(self.results.signal_1)*self.results.signal_2)/self.resource.powerCoeff, ylabel="Power",
                                    color="orange", grid=self.resource.Graph_grid, marker_pos=marker)

        self.Graph[0].addStepGraph(x=time, xlabel="time",
                                   y=asarray(self.signal)/self.resource.voltCoeff,
                                   ylabel=self.resource.source, color="blue", grid=self.resource.Graph_grid, marker_pos=marker)
        self.Graph[0].addStepGraph(x=time, xlabel="time",
                                   y=asarray(signal)/self.resource.voltCoeff,
                                   ylabel=self.resource.source, color="red", grid=self.resource.Graph_grid, marker_pos=marker)

                                   
        compliance1 = self.results.ramp_compliance*ones(self.index_Ilim2)
        compliance1 =[element for element in compliance1]
        compliance2 = self.results.pulse_compliance*ones(len(self.time) - self.index_Ilim2)
        compliance2 =[element for element in compliance2]
        compliance = asarray(compliance1 + compliance2)

        if self.resource.Graph_compliance == True:
            self.Graph[1].addStepGraph(x=self.time, y=compliance, color="blue", grid=self.resource.Graph_grid, marker_pos=marker)       
            self.Graph[1].addStepGraph(x=self.time, y=-1*compliance, color="blue", grid=self.resource.Graph_grid, marker_pos=marker)
            self.Graph[1].addStepGraph(x=time, xlabel="time",
                                       y=asarray(I)/self.resource.currCoeff,
                                       ylabel=self.resource.sense, color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        elif self.resource.Graph_compliance == False:
            self.Graph[1].addStepGraph(x=time, xlabel="time",
                                       y=asarray(I)/self.resource.currCoeff,
                                       ylabel=self.resource.sense, color="red", grid=self.resource.Graph_grid, marker_pos=marker)            

        self.Graph[2].addLinGraph(x=asarray(signal)/self.resource.voltCoeff, xlabel="Voltage",
                                  y=asarray(I)/self.resource.currCoeff, ylabel="Current",
                                  color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        self.Graph[3].addLinGraph(x=asarray(signal)/self.resource.voltCoeff, xlabel="Voltage",
                                  y=abs(asarray(I))/self.resource.currCoeff, ylabel="Current",
                                  yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        
        self.Graph[4].addLinGraph(x=asarray(self.signal)/self.resource.voltCoeff, xlabel="Voltage (Command)",
                                  y=asarray(I)/self.resource.currCoeff, ylabel="Current",
                                  color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        self.Graph[5].addLinGraph(x=asarray(self.signal)/self.resource.voltCoeff, xlabel="Voltage (Command)",
                                  y=abs(asarray(I))/self.resource.currCoeff, ylabel="Current",
                                  yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)
                                  
        self.Graph[6].addLinGraph(x=asarray(signal)/self.resource.voltCoeff, xlabel="Voltage",
                                  y=abs(asarray(R))/self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        self.Graph[7].addLinGraph(x=asarray(self.signal)/self.resource.voltCoeff, xlabel="Voltage (Command)",
                                  y=abs(asarray(R))/self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        
        self.Graph[8].addLinGraph(x=time, xlabel="time",
                                  y=abs(asarray(R))/self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)        
        self.Graph[9].addLinGraph(x=time, xlabel="time",
                                    y=abs((asarray(self.signal)/I))/self.resource.resistanceCoeff, ylabel="Resistance (Command)",
                                    yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        self.Graph[10].addStepGraph(x=time, xlabel="time",
                                   y=asarray(signal*I)/self.resource.powerCoeff, ylabel="Power",
                                   color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        
        self.Graph[11].addLinGraph(x=time, xlabel="time",
                                  y=Temperature, ylabel="Temperature (°K)",
                                  yscale="log", color="red", grid=self.resource.Graph_grid, marker_pos=marker)
        self.Graph[12].addStepGraph(x=asarray(signal)/self.resource.voltCoeff, xlabel="Voltage",
                                   y=Temperature, ylabel="Temperature (°K)",
                                   color="red", grid=self.resource.Graph_grid, marker_pos=marker)
