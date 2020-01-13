"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Parameters_view. This class creates a frame to give access to a GUI of all parameters.


"""

from tkinter import LabelFrame
from tkinter import Label
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Button
from tkinter.ttk import Combobox

from Controller import Controller

class Parameters():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root, resource):
    #Constructor for the CBRAM class
        self.resource = resource

        self.frame = LabelFrame(root, text="Parameters")
        self.frame.configure(bg=self.resource.bgColor)
        self.controller = Controller()
        self.show = True
        #self.frame.initFrame(name="Parameters")

        self.__initWidgets()  

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
        self.labelFrame_SMUParams.grid(column=0, row=1)

        self.labelFrame_graphParams = LabelFrame(self.frame, text="Graphs Parameters", bg=self.resource.bgColor)
        self.labelFrame_graphParams.grid(column=0, row=2)

        self.labelFrame_singleParams = LabelFrame(self.frame, text="Single Sequence Parameters", bg=self.resource.bgColor)
        self.labelFrame_singleParams.grid(column=0, row=3)

    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Parameters_view GUI
        self.label_generalParam_backgroundColor = Label(self.labelFrame_generalParams, text="Background Color", bg=self.resource.bgColor)
        self.label_generalParam_backgroundColor.grid(column=0, row=0)

        self.label_generalParam_textColor = Label(self.labelFrame_generalParams, text="Text Color", bg=self.resource.bgColor)
        self.label_generalParam_textColor.grid(column=0, row=1)

        self.label_generalParam_timeUnit = Label(self.labelFrame_generalParams, text="Time unit", bg=self.resource.bgColor)
        self.label_generalParam_timeUnit.grid(column=0, row=2)

        self.label_generalParam_voltUnit = Label(self.labelFrame_generalParams, text="Voltage unit", bg=self.resource.bgColor)
        self.label_generalParam_voltUnit.grid(column=0, row=3)

        self.label_generalParam_currUnit = Label(self.labelFrame_generalParams, text="Current unit", bg=self.resource.bgColor)
        self.label_generalParam_currUnit.grid(column=0, row=4)

        self.label_generalParam_powerUnit = Label(self.labelFrame_generalParams, text="Power unit", bg=self.resource.bgColor)
        self.label_generalParam_powerUnit.grid(column=0, row=5)

        self.label_SMUParam_connectionMode = Label(self.labelFrame_SMUParams, text="Connection Mode", bg=self.resource.bgColor)
        self.label_SMUParam_connectionMode.grid(column=0, row=0)

        self.label_SMUParam_adress = Label(self.labelFrame_SMUParams, text="Device's Adress", bg=self.resource.bgColor)
        self.label_SMUParam_adress.grid(column=0, row=1)

        self.label_SMUParam_source = Label(self.labelFrame_SMUParams, text="Source", bg=self.resource.bgColor)
        self.label_SMUParam_source.grid(column=0, row=3)

        self.label_SMUParam_sense = Label(self.labelFrame_SMUParams, text="Sense", bg=self.resource.bgColor)
        self.label_SMUParam_sense.grid(column=0, row=4)

        self.label_SMUParam_NPLC = Label(self.labelFrame_SMUParams, text="NPLC", bg=self.resource.bgColor)
        self.label_SMUParam_NPLC.grid(column=0, row=5)

        self.label_SMUParam_stepDelay = Label(self.labelFrame_SMUParams, text="Step Delay", bg=self.resource.bgColor)
        self.label_SMUParam_stepDelay.grid(column=0, row=6)

        self.label_graphParam_grid = Label(self.labelFrame_graphParams, text="Display Grid", bg=self.resource.bgColor)
        self.label_graphParam_grid.grid(column=0, row=0)

        self.label_graphParam_compliance = Label(self.labelFrame_graphParams, text="Display Compliance", bg=self.resource.bgColor)
        self.label_graphParam_compliance.grid(column=0, row=1)

        self.label_graphParam_backgroundColor = Label(self.labelFrame_graphParams, text="Background Color", bg=self.resource.bgColor)
        self.label_graphParam_backgroundColor.grid(column=0, row=2)

    def __initButtons(self):
    #This method instanciates all the Buttons displayed in the Parameters_view GUI
        self.button_SMUParam_adress = Button(self.labelFrame_SMUParams, text="Actualize", command=self.button_SMUParam_adress_callBack, padx=5, pady=10, bg=self.resource.bgColor)
        self.button_SMUParam_adress.grid(column=1, row=2)

    def button_SMUParam_adress_callBack(self):
    #Callback method for button_SMUParam_adress
        self.controller.service.findInstruments()
        self.combo_SMUParam_adress.configure(values=self.controller.service.instrList)

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Parameters_view GUI
        self.doubleVar_SMUParam_NPLC = DoubleVar()
        self.doubleVar_SMUParam_NPLC.set(0.01)

        self.doubleVar_SMUParam_stepDelay = DoubleVar()
        self.doubleVar_SMUParam_stepDelay.set(0.011)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Parameters_view GUI
        self.combo_generalParam_backgroundColor = Combobox(self.labelFrame_generalParams, state="readonly", values=["gainsboro", "white", "black", "grey", "blue", "yellow", "green"])
        self.combo_generalParam_backgroundColor.bind("<<ComboboxSelected>>", self.combo_generalParam_backgroundColor_callback)
        self.combo_generalParam_backgroundColor.configure(background=self.resource.bgColor)
        self.combo_generalParam_backgroundColor.grid(column=1, row=0, pady=self.resource.pady)
        self.combo_generalParam_backgroundColor.current(0)

        self.combo_generalParam_textColor = Combobox(self.labelFrame_generalParams, state="readonly", values=["gainsboro", "white", "black", "grey", "blue", "yellow", "green"])
        self.combo_generalParam_textColor.bind("<<ComboboxSelected>>", self.combo_generalParam_textColor_callback)
        self.combo_generalParam_textColor.configure(background=self.resource.bgColor)
        self.combo_generalParam_textColor.grid(column=1, row=1, pady=self.resource.pady)
        self.combo_generalParam_textColor.current(0)

        self.combo_generalParam_timeUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["hour", "mn", "s", "ms"])
        self.combo_generalParam_timeUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_textColor_callback)
        self.combo_generalParam_timeUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_timeUnit.grid(column=1, row=2, pady=self.resource.pady)
        self.combo_generalParam_timeUnit.current(2)

        self.combo_generalParam_voltUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["V", "mV", "uV"])
        self.combo_generalParam_voltUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_backgroundColor_callback)
        self.combo_generalParam_voltUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_voltUnit.grid(column=1, row=3, pady=self.resource.pady)
        self.combo_generalParam_voltUnit.current(0)

        self.combo_generalParam_currUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["A", "mA", "uA", "nA"])
        self.combo_generalParam_currUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_textColor_callback)
        self.combo_generalParam_currUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_currUnit.grid(column=1, row=4, pady=self.resource.pady)
        self.combo_generalParam_currUnit.current(1)

        self.combo_generalParam_powerUnit = Combobox(self.labelFrame_generalParams, state="readonly", values=["W", "mW", "uW", "nW"])
        self.combo_generalParam_powerUnit.bind("<<ComboboxSelected>>", self.combo_generalParam_textColor_callback)
        self.combo_generalParam_powerUnit.configure(background=self.resource.bgColor)
        self.combo_generalParam_powerUnit.grid(column=1, row=5, pady=self.resource.pady)
        self.combo_generalParam_powerUnit.current(1)

        self.combo_SMUParam_adress = Combobox(self.labelFrame_SMUParams, state="readonly", values=self.controller.service.instrList)
        self.combo_SMUParam_adress.bind("<<ComboboxSelected>>", self.combo_SMUParam_adress_callback)
        self.combo_SMUParam_adress.configure(background=self.resource.bgColor)
        self.combo_SMUParam_adress.grid(column=1, row=1, pady=self.resource.pady)
        self.combo_SMUParam_adress.current(0)

        self.combo_SMUParam_source = Combobox(self.labelFrame_SMUParams, state="readonly", values=["VOLT", "CURR"])
        self.combo_SMUParam_source.bind("<<ComboboxSelected>>", self.combo_SMUParam_source_callback)
        self.combo_SMUParam_source.configure(background=self.resource.bgColor)
        self.combo_SMUParam_source.grid(column=1, row=3, pady=self.resource.pady)
        self.combo_SMUParam_source.current(0)

        self.combo_SMUParam_sense = Combobox(self.labelFrame_SMUParams, state="readonly", values=["VOLT", "CURR"])
        self.combo_SMUParam_sense.bind("<<ComboboxSelected>>", self.combo_SMUParam_sense_callback)
        self.combo_SMUParam_sense.configure(background=self.resource.bgColor)
        self.combo_SMUParam_sense.grid(column=1, row=4, pady=self.resource.pady)
        self.combo_SMUParam_sense.current(1)

        self.combo_graphParam_grid = Combobox(self.labelFrame_graphParams, state="readonly", values=["Yes", "No"])
        self.combo_graphParam_grid.bind("<<ComboboxSelected>>", self.combo_graphParam_grid_callback)
        self.combo_graphParam_grid.configure(background=self.resource.bgColor)
        self.combo_graphParam_grid.grid(column=1, row=0, pady=self.resource.pady)
        self.combo_graphParam_grid.current(0)

        self.combo_graphParam_compliance = Combobox(self.labelFrame_graphParams, state="readonly", values=["Yes", "No"])
        self.combo_graphParam_compliance.bind("<<ComboboxSelected>>", self.combo_graphParam_compliance_callback)
        self.combo_graphParam_compliance.configure(background=self.resource.bgColor)
        self.combo_graphParam_compliance.grid(column=1, row=1, pady=self.resource.pady)
        self.combo_graphParam_compliance.current(0)

        self.combo_graphParam_backgroundColor = Combobox(self.labelFrame_graphParams, state="readonly", values=["gainsboro", "white", "black", "grey", "blue", "yellow", "green"])
        self.combo_graphParam_backgroundColor.bind("<<ComboboxSelected>>", self.combo_graphParam_backgroundColor_callback)
        self.combo_graphParam_backgroundColor.configure(background=self.resource.bgColor)
        self.combo_graphParam_backgroundColor.grid(column=1, row=2, pady=self.resource.pady)
        self.combo_graphParam_backgroundColor.current(2)

    def combo_generalParam_backgroundColor_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        self.resource.bgColor = self.combo_generalParam_backgroundColor.get()

    def combo_generalParam_textColor_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        self.textColor = self.combo_generalParam_textColor.get()

    def combo_SMUParam_connectionMode_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        print("SMUParam_connectionMode")

    def combo_SMUParam_adress_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        print(self.combo_SMUParam_adress.get())
        self.deviceAdress = self.combo_SMUParam_adress.get()
        print(self.deviceAdress)

    def combo_SMUParam_source_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        print("SMUParam_source")

    def combo_SMUParam_sense_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        print("SMUParam_sense")

    def combo_graphParam_grid_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        if self.combo_graphParam_grid.get() == "Yes":
            self.resource.Graph_grid = True
        else:
            self.resource.Graph_grid = False

    def combo_graphParam_compliance_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        if self.combo_graphParam_compliance.get() == "Yes":
            self.resource.Graph_compliance = True
        else:
            self.resource.Graph_compliance = False

    def combo_graphParam_backgroundColor_callback(self, args):
    #Callback method for combo_generalParam_backgroundColor
        self.resource.Graph_bgColor = self.combo_graphParam_backgroundColor.get()

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the parameters_view GUI
        self.entry_SMUParam_NPLC = Entry(self.labelFrame_SMUParams, textvariable=self.doubleVar_SMUParam_NPLC)
        self.entry_SMUParam_NPLC.grid(column=1, row=5, pady=self.resource.pady)

        self.entry_SMUParam_stepDelay = Entry(self.labelFrame_SMUParams, textvariable=self.doubleVar_SMUParam_stepDelay)
        self.entry_SMUParam_stepDelay.grid(column=1, row=6, pady=self.resource.pady)
