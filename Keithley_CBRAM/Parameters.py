"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for Parameters_view. This class creates a frame to give access to a GUI of all parameters.


"""

from tkinter import LabelFrame
from tkinter import Label
from tkinter import DoubleVar
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter.ttk import Combobox

from Controller import Controller
from Service import Service

class Parameters():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root, resource):
    #Constructor for the CBRAM class
        self.resource = resource

        self.frame = LabelFrame(root, text="Parameters")
        self.frame.configure(bg=self.resource.bgColor)
        self.controller = Controller(resource)
        self.service = Service(root, resource)
        self.show = True
        #self.frame.initFrame(name="Parameters")

        self.__initWidgets()
        self.combo_SMUParam_adress_callback()  

    def __initWidgets(self):
    #This method creates/actualize all the Widgets displayed in the Parameters_view frame
        self.__initLabelFrames()
        self.__initLabels()
        self.__initButtons()
        self.__initVars()
        self.__initCombobox()
        self.__initEntries()

    def __initLabelFrames(self):
    #This methods instanciates all the LabelFrames displayed in the Parameters_view GUI
        self.labelFrame_generalParams = LabelFrame(self.frame, text="General Parameters", bg=self.resource.bgColor)
        self.labelFrame_generalParams.grid(column=0, row=0)

        self.labelFrame_SMUParams = LabelFrame(self.frame, text="SMU Parameters", bg=self.resource.bgColor)
        self.labelFrame_SMUParams.grid(column=0, row=2)

        self.labelFrame_graphParams = LabelFrame(self.frame, text="Graphs Parameters", bg=self.resource.bgColor)
        self.labelFrame_graphParams.grid(column=0, row=4)

        self.labelFrame_sequenceParams = LabelFrame(self.frame, text="Sequence Parameters", bg=self.resource.bgColor)
        self.labelFrame_sequenceParams.grid(column=0, row=6)

    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Parameters_view GUI
        self.label_generalParam_timeUnit = Label(self.labelFrame_generalParams, text="Time unit : ", bg=self.resource.bgColor)
        self.label_generalParam_timeUnit.grid(column=0, row=0)

        self.label_generalParam_voltUnit = Label(self.labelFrame_generalParams, text="Voltage unit : ", bg=self.resource.bgColor)
        self.label_generalParam_voltUnit.grid(column=0, row=1)

        self.label_generalParam_currUnit = Label(self.labelFrame_generalParams, text="Current unit : ", bg=self.resource.bgColor)
        self.label_generalParam_currUnit.grid(column=0, row=2)

        self.label_generalParam_resistanceUnit = Label(self.labelFrame_generalParams, text="Resistance unit : ", bg=self.resource.bgColor)
        self.label_generalParam_resistanceUnit.grid(column=0, row=3)

        self.label_generalParam_powerUnit = Label(self.labelFrame_generalParams, text="Power unit : ", bg=self.resource.bgColor)
        self.label_generalParam_powerUnit.grid(column=0, row=4)

        self.label_generalParam_autoExport = Label(self.labelFrame_generalParams, text="Auto export : ", bg=self.resource.bgColor)
        self.label_generalParam_autoExport.grid(column=0, row=5)

        self.label_generalParam_exportPath = Label(self.labelFrame_generalParams, text="Export Path : ", bg=self.resource.bgColor)
        self.label_generalParam_exportPath.grid(column=0, row=6)

        self.label_SMUParam_connectionMode = Label(self.labelFrame_SMUParams, text="Connection Mode : ", bg=self.resource.bgColor)
        self.label_SMUParam_connectionMode.grid(column=0, row=0)

        self.label_SMUParam_adress = Label(self.labelFrame_SMUParams, text="Device's Adress : ", bg=self.resource.bgColor)
        self.label_SMUParam_adress.grid(column=0, row=1)

        self.label_SMUParam_source = Label(self.labelFrame_SMUParams, text="Source : ", bg=self.resource.bgColor)
        self.label_SMUParam_source.grid(column=0, row=3)

        self.label_SMUParam_sense = Label(self.labelFrame_SMUParams, text="Sense : ", bg=self.resource.bgColor)
        self.label_SMUParam_sense.grid(column=0, row=4)

        self.label_SMUParam_NPLC = Label(self.labelFrame_SMUParams, text="NPLC : ", bg=self.resource.bgColor)
        self.label_SMUParam_NPLC.grid(column=0, row=5)

        self.label_SMUParam_stepDelay = Label(self.labelFrame_SMUParams, text="Step Delay : ", bg=self.resource.bgColor)
        self.label_SMUParam_stepDelay.grid(column=0, row=6)

        self.label_graphParam_grid = Label(self.labelFrame_graphParams, text="Display Grid : ", bg=self.resource.bgColor)
        self.label_graphParam_grid.grid(column=0, row=0)

        self.label_graphParam_compliance = Label(self.labelFrame_graphParams, text="Display Compliance : ", bg=self.resource.bgColor)
        self.label_graphParam_compliance.grid(column=0, row=1)

        self.label_graphParam_backgroundColor = Label(self.labelFrame_graphParams, text="Background Color : ", bg=self.resource.bgColor)
        self.label_graphParam_backgroundColor.grid(column=0, row=2)

        self.label_sequenceParam_R_low_lim = Label(self.labelFrame_sequenceParams, text="Rlow limit : ", bg=self.resource.bgColor)
        self.label_sequenceParam_R_low_lim .grid(column=0, row=0)

        self.label_sequenceParam_R_high_lim  = Label(self.labelFrame_sequenceParams, text="Rhigh limit : ", bg=self.resource.bgColor)
        self.label_sequenceParam_R_high_lim .grid(column=0, row=1)

        self.label_sequenceParam_nbTry = Label(self.labelFrame_sequenceParams, text="nbTry : ", bg=self.resource.bgColor)
        self.label_sequenceParam_nbTry.grid(column=0, row=2)

    def __initButtons(self):
    #This method instanciates all the Buttons displayed in the Parameters_view GUI
        self.button_SMUParam_adress = Button(self.labelFrame_SMUParams, text="Actualize", command=self.button_SMUParam_adress_callBack, padx=5, pady=10, bg=self.resource.bgColor)
        self.button_SMUParam_adress.grid(column=1, row=2)

    def button_SMUParam_adress_callBack(self):
    #Callback method for button_SMUParam_adress
        self.service.findInstruments()
        self.combo_SMUParam_adress.configure(values=self.service.instrList)

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Parameters_view GUI
        self.stringVar_generalParam_exportPath = StringVar()
        self.stringVar_generalParam_exportPath.set(self.resource.exportPath)

        self.doubleVar_SMUParam_NPLC = DoubleVar()
        self.doubleVar_SMUParam_NPLC.set(0.01)

        self.doubleVar_SMUParam_stepDelay = DoubleVar()
        self.doubleVar_SMUParam_stepDelay.set(0.0093)

        self.doubleVar_sequenceParam_R_low_lim = DoubleVar()
        self.doubleVar_sequenceParam_R_low_lim.set(self.resource.R_low_lim)

        self.doubleVar_sequenceParam_R_high_lim = DoubleVar()
        self.doubleVar_sequenceParam_R_high_lim.set(self.resource.R_high_lim)

        self.doubleVar_sequenceParam_nbTry= DoubleVar()
        self.doubleVar_sequenceParam_nbTry.set(self.resource.nbTry)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Parameters_view GUI
        self.combo_generalParam_timeUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["hour", "mn", "s", "ms"],width=5)
        self.combo_generalParam_timeUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_timeUnit_callback)
        self.combo_generalParam_timeUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_timeUnit.grid(column=1, row=0, pady=self.resource.pady)
        self.combo_generalParam_timeUnit.current(2)

        self.combo_generalParam_voltUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["V", "mV", "uV"],width=5)
        self.combo_generalParam_voltUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_voltUnit_callback)
        self.combo_generalParam_voltUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_voltUnit.grid(column=1, row=1, pady=self.resource.pady)
        self.combo_generalParam_voltUnit.current(0)

        self.combo_generalParam_currUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["A", "mA", "uA", "nA"],width=5)
        self.combo_generalParam_currUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_currUnit_callback)
        self.combo_generalParam_currUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_currUnit.grid(column=1, row=2, pady=self.resource.pady)
        self.combo_generalParam_currUnit.current(1)

        self.combo_generalParam_resistanceUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["MOhm", "KOhm", "Ohm", "mOhm"],width=5)
        self.combo_generalParam_resistanceUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_resistanceUnit_callback)
        self.combo_generalParam_resistanceUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_resistanceUnit.grid(column=1, row=3, pady=self.resource.pady)
        self.combo_generalParam_resistanceUnit.current(2)

        self.combo_generalParam_powerUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["W", "mW", "uW", "nW"],width=5)
        self.combo_generalParam_powerUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_powerUnit_callback)
        self.combo_generalParam_powerUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_powerUnit.grid(column=1, row=4, pady=self.resource.pady)
        self.combo_generalParam_powerUnit.current(1)

        self.combo_generalParam_autoExport = Combobox(self.labelFrame_generalParams, state="readonly", values=["Yes", "No"],width=12)
        self.combo_generalParam_autoExport.bind("<<ComboboxSelected>>", self.combo_generalParam_autoExport_callback)
        self.combo_generalParam_autoExport.configure(background=self.resource.bgColor)
        self.combo_generalParam_autoExport.grid(column=1, row=5, pady=self.resource.pady)
        self.combo_generalParam_autoExport.current(1)

        self.combo_SMUParam_connectionMode = Combobox(self.labelFrame_SMUParams, state="readonly", values=["USB", "Ethernet", "GPIB"],width=12)
        self.combo_SMUParam_connectionMode.bind("<<ComboboxSelected>>", self.combo_SMUParam_connectionMode_callback)
        self.combo_SMUParam_connectionMode.configure(background=self.resource.bgColor)
        self.combo_SMUParam_connectionMode.grid(column=1, row=0, pady=self.resource.pady)
        self.combo_SMUParam_connectionMode.current(0)

        self.combo_SMUParam_adress = Combobox(self.labelFrame_SMUParams, state="readonly", values=self.service.instrList,width=25)
        self.combo_SMUParam_adress.bind("<<ComboboxSelected>>", self.combo_SMUParam_adress_callback)
        self.combo_SMUParam_adress.configure(background=self.resource.bgColor)
        self.combo_SMUParam_adress.grid(column=1, row=1, pady=self.resource.pady)
        self.combo_SMUParam_adress.current(0)

        self.combo_SMUParam_source = Combobox(self.labelFrame_SMUParams, state="readonly", values=["VOLT", "CURR"],width=12)
        self.combo_SMUParam_source.bind("<<ComboboxSelected>>", self.combo_SMUParam_source_callback)
        self.combo_SMUParam_source.configure(background=self.resource.bgColor)
        self.combo_SMUParam_source.grid(column=1, row=3, pady=self.resource.pady)
        self.combo_SMUParam_source.current(0)

        self.combo_SMUParam_sense = Combobox(self.labelFrame_SMUParams, state="readonly", values=["VOLT", "CURR"],width=12)
        self.combo_SMUParam_sense.bind("<<ComboboxSelected>>", self.combo_SMUParam_sense_callback)
        self.combo_SMUParam_sense.configure(background=self.resource.bgColor)
        self.combo_SMUParam_sense.grid(column=1, row=4, pady=self.resource.pady)
        self.combo_SMUParam_sense.current(1)

        self.combo_graphParam_grid = Combobox(self.labelFrame_graphParams, state="readonly", values=["Yes", "No"],width=12)
        self.combo_graphParam_grid.bind("<<ComboboxSelected>>", self.combo_graphParam_grid_callback)
        self.combo_graphParam_grid.configure(background=self.resource.bgColor)
        self.combo_graphParam_grid.grid(column=1, row=0, pady=self.resource.pady)
        self.combo_graphParam_grid.current(0)

        self.combo_graphParam_compliance = Combobox(self.labelFrame_graphParams, state="readonly", values=["Yes", "No"],width=12)
        self.combo_graphParam_compliance.bind("<<ComboboxSelected>>", self.combo_graphParam_compliance_callback)
        self.combo_graphParam_compliance.configure(background=self.resource.bgColor)
        self.combo_graphParam_compliance.grid(column=1, row=1, pady=self.resource.pady)
        self.combo_graphParam_compliance.current(0)

        self.combo_graphParam_backgroundColor = Combobox(self.labelFrame_graphParams, state="readonly", values=["gainsboro", "white", "black", "grey", "blue", "yellow", "green"],width=12)
        self.combo_graphParam_backgroundColor.bind("<<ComboboxSelected>>", self.combo_graphParam_backgroundColor_callback)
        self.combo_graphParam_backgroundColor.configure(background=self.resource.bgColor)
        self.combo_graphParam_backgroundColor.grid(column=1, row=2, pady=self.resource.pady)
        self.combo_graphParam_backgroundColor.current(1)

    def combo_generalParam_timeUnit_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        self.resource.timeUnit = self.combo_generalParam_timeUnit.get()

    def combo_generalParam_voltUnit_callback(self, args=""):
    #Callback method for combo_generalParam_voltUnit
        if self.combo_generalParam_voltUnit.get() == "V":
            self.resource.voltCoeff = 1

        elif self.combo_generalParam_voltUnit.get() == "mV":
            self.resource.voltCoeff = 1e-3

        elif self.combo_generalParam_voltUnit.get() == "uV":
            self.resource.voltCoeff = 1e-6

    def combo_generalParam_currUnit_callback(self, args=""):
    #Callback method for combo_generalParam_currUnit
        if self.combo_generalParam_currUnit.get() == "A":
            self.resource.currCoeff = 1

        elif self.combo_generalParam_currUnit.get() == "mA":
            self.resource.currCoeff = 1e-3

        elif self.combo_generalParam_currUnit.get() == "uA":
            self.resource.currCoeff = 1e-6

        elif self.combo_generalParam_currUnit.get() == "nA":
            self.resource.currCoeff = 1e-9

    def combo_generalParam_resistanceUnit_callback(self, args=""):
    #Callback method for combo_generalParam_resistanceUnit
        if self.combo_generalParam_resistanceUnit.get() == "MOhm":
            self.resource.resistanceCoeff = 1e6

        elif self.combo_generalParam_resistanceUnit.get() == "KOhm":
            self.resource.resistanceCoeff = 1e3

        elif self.combo_generalParam_resistanceUnit.get() == "Ohm":
            self.resource.resistanceCoeff = 1

        elif self.combo_generalParam_resistanceUnit.get() == "mOhm":
            self.resource.resistanceCoeff = 1e-3

    def combo_generalParam_powerUnit_callback(self, args=""):
    #Callback method for combo_generalParam_powerUnit
        if self.combo_generalParam_powerUnit.get() == "W":
            self.resource.powerCoeff = 1

        elif self.combo_generalParam_powerUnit.get() == "mW":
            self.resource.powerCoeff = 1e-3

        elif self.combo_generalParam_powerUnit.get() == "uW":
            self.resource.powerCoeff = 1e-6

        elif self.combo_generalParam_powerUnit.get() == "nW":
            self.resource.powerCoeff = 1e-9

    def combo_generalParam_autoExport_callback(self, args=""):
    #Callback method for combo_generalParam_powerUnit
        if self.combo_generalParam_autoExport.get() == "Yes":
            self.resource.autoExport = True

        elif self.combo_generalParam_autoExport.get() == "No":
            self.resource.autoExport = False

    def combo_SMUParam_connectionMode_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        print("SMUParam_connectionMode")

    def combo_SMUParam_adress_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        self.resource.deviceAdress = self.combo_SMUParam_adress.get()

    def combo_SMUParam_source_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        print("SMUParam_source")

    def combo_SMUParam_sense_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        print("SMUParam_sense")

    def combo_graphParam_grid_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        if self.combo_graphParam_grid.get() == "Yes":
            self.resource.Graph_grid = True
        else:
            self.resource.Graph_grid = False

    def combo_graphParam_compliance_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        if self.combo_graphParam_compliance.get() == "Yes":
            self.resource.Graph_compliance = True
        else:
            self.resource.Graph_compliance = False

    def combo_graphParam_backgroundColor_callback(self, args=""):
    #Callback method for combo_generalParam_backgroundColor
        self.resource.Graph_bgColor = self.combo_graphParam_backgroundColor.get()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the parameters_view GUI
        self.entry_generalParam_exportPath = Entry(self.labelFrame_generalParams, textvariable=self.stringVar_generalParam_exportPath, width=30)
        self.entry_generalParam_exportPath.bind("<Return>", self.entry_generalParam_exportPath_callback)
        self.entry_generalParam_exportPath.grid(column=1, row=6, padx=self.resource.padx, pady=self.resource.pady)

        self.entry_SMUParam_NPLC = Entry(self.labelFrame_SMUParams, textvariable=self.doubleVar_SMUParam_NPLC, width=12)
        self.entry_SMUParam_NPLC.bind("<Return>", self.entry_SMUParam_NPLC_callback)
        self.entry_SMUParam_NPLC.grid(column=1, row=5, pady=self.resource.pady)

        self.entry_SMUParam_stepDelay = Entry(self.labelFrame_SMUParams, textvariable=self.doubleVar_SMUParam_stepDelay, width=12)
        self.entry_SMUParam_stepDelay.bind("<Return>", self.entry_SMUParam_stepDelay_callback)
        self.entry_SMUParam_stepDelay.grid(column=1, row=6, pady=self.resource.pady)

        self.entry_sequenceParam_R_low_lim = Entry(self.labelFrame_sequenceParams, textvariable=self.doubleVar_sequenceParam_R_low_lim, width=12)
        self.entry_sequenceParam_R_low_lim.bind("<Return>", self.entry_sequenceParam_R_low_lim_callback)
        self.entry_sequenceParam_R_low_lim.grid(column=1, row=0, pady=self.resource.pady)

        self.entry_sequenceParam_R_high_lim = Entry(self.labelFrame_sequenceParams, textvariable=self.doubleVar_sequenceParam_R_high_lim, width=12)
        self.entry_sequenceParam_R_high_lim.bind("<Return>", self.entry_sequenceParam_R_high_lim_callback)
        self.entry_sequenceParam_R_high_lim.grid(column=1, row=1, pady=self.resource.pady)

        self.entry_sequenceParam_nbTry = Entry(self.labelFrame_sequenceParams, textvariable=self.doubleVar_sequenceParam_nbTry, width=12)
        self.entry_sequenceParam_nbTry.bind("<Return>", self.entry_sequenceParam_nbTry_callback)
        self.entry_sequenceParam_nbTry.grid(column=1, row=2, pady=self.resource.pady)

    def entry_SMUParam_NPLC_callback(self, args=""):
    #Callback method for entry_SMUParam_NPLC
        self.resource.NPLC = self.doubleVar_SMUParam_NPLC.get()

    def entry_SMUParam_stepDelay_callback(self, args=""):
    #Callback method for entry_SMUParam_NPLC
        self.resource.stepDelay = self.doubleVar_SMUParam_stepDelay.get()

    def entry_sequenceParam_R_low_lim_callback(self, args=""):
    #Callback method for entry_SMUParam_NPLC
        self.resource.R_low_lim = self.doubleVar_sequenceParam_R_low_lim.get()

    def entry_sequenceParam_R_high_lim_callback(self, args=""):
    #Callback method for entry_SMUParam_NPLC
        self.resource.R_high_lim = self.doubleVar_sequenceParam_R_high_lim.get()

    def entry_sequenceParam_nbTry_callback(self, args=""):
    #Callback method for entry_SMUParam_NPLC
        self.resource.nbTry = self.doubleVar_sequenceParam_nbTry.get()
        self.resource.R_high_lim = self.doubleVar_sequenceParam_R_high_lim.get()

    def entry_generalParam_exportPath_callback(self, args=""):
    #Callback method for entry_SMUParam_NPLC
        self.resource.exportPath = self.stringVar_generalParam_exportPath.get()

    def update(self, result=0):
    #This methods updates the parameters with the result argument

        if result != 0:
            try :
                self.doubleVar_sequenceParam_nbTry.set(result.nbTry_max)
            except AttributeError:
                pass

            self.doubleVar_sequenceParam_R_high_lim.set(result.R_high_lim)
            self.doubleVar_sequenceParam_R_low_lim.set(result.R_low_lim)

            self.doubleVar_SMUParam_NPLC.set(result.stepDelay)
            self.doubleVar_SMUParam_stepDelay.set(result.NPLC)

            if result.voltCoeff == 1:
                self.combo_generalParam_voltUnit.current(0)
            elif result.voltCoeff == 1e-3:
                self.combo_generalParam_voltUnit.current(1)
            elif result.voltCoeff == 1e-6:
                self.combo_generalParam_voltUnit.current(2)
                
            if result.currCoeff == 1:
                self.combo_generalParam_currUnit.current(0)
            elif result.currCoeff == 1e-3:
                self.combo_generalParam_currUnit.current(1)
            elif result.currCoeff == 1e-6:
                self.combo_generalParam_currUnit.current(2)
            elif result.currCoeff == 1e-9:
                self.combo_generalParam_currUnit.current(3)
                
            if result.resistanceCoeff == 1e6:
                self.combo_generalParam_resistanceUnit.current(0)
            elif result.resistanceCoeff == 1e3:
                self.combo_generalParam_resistanceUnit.current(1)
            elif result.resistanceCoeff == 1:
                self.combo_generalParam_resistanceUnit.current(2)
            elif result.resistanceCoeff == 1e-2:
                self.combo_generalParam_resistanceUnit.current(3)
                
            if result.powerCoeff == 1:
                self.combo_generalParam_powerUnit.current(0)
            elif result.powerCoeff == 1e-3:
                self.combo_generalParam_powerUnit.current(1)
            elif result.powerCoeff == 1e-6:
                self.combo_generalParam_powerUnit.current(2)
            elif result.powerCoeff == 1e-9:
                self.combo_generalParam_powerUnit.current(3)

            if result.source == "VOLT":
                self.combo_SMUParam_source.current(0)
            elif result.source == "CURR":
                self.combo_SMUParam_source.current(1)

            if result.sense == "VOLT":
                self.combo_SMUParam_sense.current(0)
            elif result.sense == "CURR":
                self.combo_SMUParam_sense.current(1)
