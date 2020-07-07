"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for the Stability test bench. Stability is made to measure the evolution of the resistance state through time.

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
from tkinter import messagebox
from tkinter.ttk import Combobox

from numpy import ones
from numpy import linspace
from numpy import asarray
from numpy import concatenate
from numpy import any

class Stability(Sequence):
    """Class containing the Stability testbench.

    """

    def __init__(self, root, resource, terminal):
    #Constructor for the Single class
        Sequence.__init__(self, root, resource, terminal)
        self.state = "STABILITY"

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
        self.Graph = [Graph(self.frame, self.resource, "Resistance")]
       
        self.graph_TL = self.Graph[0]
        self.graph_TL.modifyFigure(Graph_size=100)
        self.graph_TL.frame.grid(column=3, row=0, rowspan=8)

    def __initLabelFrames(self):
    #This method instanciates all the LabelFrames used in the Cycling test bench GUI
        self.labelFrame_MeasurementSetup = LabelFrame(self.frame, text="Measurement Setup")
        self.labelFrame_MeasurementSetup.configure(bg=self.resource.bgColor)
        self.labelFrame_MeasurementSetup.grid(column=0, columnspan=3, row=3, padx=self.resource.padx, pady=self.resource.pady)
        
    def __initButtons(self):
    #This method instanciates all the buttons used by the Cycling test bench GUI
        self.button_actualizeSequence.grid(column=0, columnspan=2, row=4, padx=10, pady=5)
        self.button_startSequence.grid(column=1, columnspan=2, row=4, padx=10, pady=5)

        self.button_measureResistance_pos.grid(column=0, row=5, rowspan=1, padx=10, pady=5)
        self.button_measureResistance_neg.grid(column=1, row=5, rowspan=1, padx=10, pady=5)
        self.button_measureImpedance.grid(column=2, row=5, rowspan=1, padx=10, pady=5)

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.stringVar_CBRAM_ident = StringVar()
        self.stringVar_CBRAM_ident.set("35u:1000n:600n:ddmmyyss:00x00")

        self.doubleVar_CBRAM_resistance = DoubleVar()
        self.doubleVar_CBRAM_resistance.set(1e6)

        self.doubleVar_nb_measurement = DoubleVar()
        self.doubleVar_nb_measurement.set(25)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench provides resistance measurement configuration for\nstability study of a CBRAM cell", padx=10, pady=20)
        self.label_description.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_description.grid(column=0, columnspan=3, row=0)

        self.label_CBRAM_ident = Label(self.frame, text="CBRAM cell's identifier : ")
        self.label_CBRAM_ident.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_ident.grid(column=0, row=1)

        self.label_CBRAM_resistance = Label(self.frame, text = "CBRAM cell's resistance : ")
        self.label_CBRAM_resistance.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_CBRAM_resistance.grid(column=0, row=2)

        self.label_measurement_type = Label(self.labelFrame_MeasurementSetup, text = "Measurement type : ")
        self.label_measurement_type.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_measurement_type.grid(column=0, row=0)

        self.label_measurement_method = Label(self.labelFrame_MeasurementSetup, text = "Measurement method : ")
        self.label_measurement_method.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_measurement_method.grid(column=0, row=1)

        self.label_nb_measurement = Label(self.labelFrame_MeasurementSetup, text = "Number of points : ")
        self.label_nb_measurement.configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_nb_measurement.grid(column=0, row=2)

        self.label_duration = Label(self.labelFrame_MeasurementSetup, text = "Duration : ")
        self.label_duration .configure(bg=self.resource.bgColor, fg=self.resource.textColor)
        self.label_duration .grid(column=0, row=3)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_measurementType = Combobox(self.labelFrame_MeasurementSetup, state="readonly", width=20, values=["Linear", "Geometric"])
        self.combo_measurementType.bind("<<ComboboxSelected>>", self.combo_measurementType_callback)
        self.combo_measurementType.configure(background=self.resource.bgColor)
        self.combo_measurementType.grid(column=1, row=0, padx=3*self.resource.padx, pady=self.resource.pady)
        self.combo_measurementType.current(0)
        
        self.combo_measurementMethod = Combobox(self.labelFrame_MeasurementSetup, state="readonly", width=20, values=["Positive", "Negative", "Impedance"])
        self.combo_measurementMethod.bind("<<ComboboxSelected>>", self.combo_measurementMethod_callback)
        self.combo_measurementMethod.configure(background=self.resource.bgColor)
        self.combo_measurementMethod.grid(column=1, row=1, padx=3*self.resource.padx, pady=self.resource.pady)
        self.combo_measurementMethod.current(0)
        
        self.combo_duration = Combobox(self.labelFrame_MeasurementSetup, state="readonly", width=20, values=["15mn", "30mn", "1h", "2h", "3h", "5h", "8h", "12h"])
        self.combo_duration.bind("<<ComboboxSelected>>", self.combo_duration_callback)
        self.combo_duration.configure(background=self.resource.bgColor)
        self.combo_duration.grid(column=1, row=3, padx=3*self.resource.padx, pady=self.resource.pady)
        self.combo_duration.current(0)

    def combo_measurementType_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        self.button_actualizeSequence_callBack()

    def combo_measurementMethod_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        self.button_actualizeSequence_callBack()

    def combo_duration_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        self.button_actualizeSequence_callBack()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_CBRAM_ident = Entry(self.frame, textvariable=self.stringVar_CBRAM_ident, width=30)
        self.entry_CBRAM_ident.grid(column=1, columnspan=2, row=1, padx=self.resource.padx)

        self.entry_CBRAM_resistance = Entry(self.frame, textvariable=self.doubleVar_CBRAM_resistance, width=12, state="readonly")
        self.entry_CBRAM_resistance.grid(column=1, columnspan=2, row=2, pady=self.resource.pady)

        self.entry_nb_measurement = Entry(self.labelFrame_MeasurementSetup, textvariable=self.doubleVar_nb_measurement, width=12)
        self.entry_nb_measurement.grid(column=1, row=2, pady=self.resource.pady)    

    def button_actualizeSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.results.cell_ident = self.stringVar_CBRAM_ident.get()

        if self.combo_duration.current() == 0:
            duration = 900
        elif self.combo_duration.current() == 1:
            duration = 1800
        elif self.combo_duration.current() == 2:
            duration = 3600
        elif self.combo_duration.current() == 3:
            duration = 7200
        elif self.combo_duration.current() == 4:
            duration = 10800
        elif self.combo_duration.current() == 5:
            duration = 18000
        elif self.combo_duration.current() == 6:
            duration = 28800
        elif self.combo_duration.current() == 7:
            duration = 43200

        self.time = linspace(0, self.doubleVar_nb_measurement.get(), self.doubleVar_nb_measurement.get())

        self.results.delay = self.controller.generateTimeBase(self.combo_measurementType.get(), duration, self.doubleVar_nb_measurement.get())
        self.results.duration = self.combo_duration.get()
        self.results.measurementMethod = self.combo_measurementMethod.get()
        self.results.measurementType = self.combo_measurementType.get()

        self.Graph[0].clearGraph()
        self.Graph[0].addStepGraph(x=self.time, xlabel="Iteration", y=self.results.delay, ylabel="Time (s)", grid=self.resource.Graph_grid)

    def button_startSequence_callBack(self):
    #This method is a callBack funtion for button_startSequence
        self.button_actualizeSequence_callBack()

        if self.combo_measurementMethod.get() == "Positive":
            negative = False
        elif self.combo_measurementMethod.get() == "Negative":
            negative = True
            
        [self.results.resistance, error] = self.service.measureStability(self.term_text, self.results.delay, negative=negative)

        self.results.cell_resistance = self.results.resistance[-1]     

        self.printResult()
        self.param2result()
        path=self.autoExport()

        if any(error) == True:
            messagebox.showinfo(title="Sequence ERROR", message=("An error occured during Measurement.\n Sequence was ended without export."))

            if self.resource.mailNotification == True :            
                message = "A Stability test was terminated with an error on your computer."
                self.service.sendEmailNotification(message)

        else :
            messagebox.showinfo(title="End of Sequence", message=("Stability Sequence ended succesfully.\n"))

            if self.resource.mailNotification == True :
                message = "A Stability test was succesfully terminated on your computer.\n\n Data were saved at :\n\n" + path 
                self.service.sendEmailNotification(message)

            if self.resource.autoExport == True:
                messagebox.showinfo(title="Auto Export", message=("Result files have been exported to the following PATH :\n" + path))
                
    def printResult(self):
    #This method add results to Graphs
        self.doubleVar_CBRAM_resistance.set(self.results.resistance[-1])

        self.Graph[0].clearGraph()

        resistance = asarray(self.results.resistance)

        self.Graph[0].addLinGraph(x=self.results.delay, xlabel="Time (s)", y=resistance/self.resource.resistanceCoeff, ylabel="Resistance",
                                  yscale="log", color="orange", grid=self.resource.Graph_grid)

    def loadResults(self):
    #This methods load results in the different widgets  
        self.stringVar_CBRAM_ident.set(self.results.cell_ident)
        self.doubleVar_CBRAM_resistance.set(self.results.cell_resistance)

        if self.results.duration == "15mn":
            self.combo_duration.current(0)
        elif self.results.duration == "30mn":
            self.combo_duration.current(1)
        elif self.results.duration == "1h":
            self.combo_duration.current(2)
        elif self.results.duration == "2h":
            self.combo_duration.current(3)
        elif self.results.duration == "3h":
            self.combo_duration.current(4)
        elif self.results.duration == "5h":
            self.combo_duration.current(5)
        elif self.results.duration == "8h":
            self.combo_duration.current(6)
        elif self.results.duration == "12h":
            self.combo_duration.current(7)

        if self.results.measurementType == "Linear":
            self.combo_measurementType.current(0)
        elif self.results.measurementType == "Geometric":
            self.combo_measurementType.current(1)

        if self.results.measurementMethod == "positive":
            self.combo_measurementMethod.current(0)
        elif self.results.measurementMethod == "negative":
            self.combo_measurementMethod.current(1)

        self.doubleVar_nb_measurement.set(len(self.results.resistance))

        self.printResult()
