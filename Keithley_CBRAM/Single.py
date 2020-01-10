"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for the Single test bench. Single Sequence allow to modify the state of a CBRAM cell once.

"""

from Sequence import Sequence_view

from tkinter import Label
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter.ttk import Combobox

class Single_view(Sequence_view):
    """Class containing the Single_view testbench.

    """

    def __init__(self, root):
    #Constructor for the Single_view class
        Sequence_view.__init__(self, root)
        self.state = "SINGLE"
        self.model = Single_Model()
        self.initFrame(text="Single Sequence", bg=self.bgColor)

        self.__initWidgets()

    def __initWidgets(self):
    #The method creates/actualize all the Widgets displayed in the Single sequence frame
        self.__initVars()
        self.__initLabels()
        self.__initCombobox()
        self.__initEntries()

    def __initVars(self):
    #This methods instanciates all the Vars used by widgets in the Single test bench GUI
        self.stringVar_startValue = StringVar()
        self.stringVar_startValue.set("Start value : ")
        
        self.stringVar_stopValue = StringVar()
        self.stringVar_stopValue.set("Stop value : ")

        self.stringVar_time = StringVar()
        self.stringVar_time.set("Ramp : ")

        self.stringVar_compliance = StringVar()
        self.stringVar_compliance.set(self.sense + " compliance : ")

        self.doubleVar_startValue = DoubleVar()
        self.doubleVar_startValue.set(0)

        self.doubleVar_stopValue = DoubleVar()
        self.doubleVar_stopValue.set(20)

        self.doubleVar_time = DoubleVar()
        self.doubleVar_time.set(50)

        self.doubleVar_compliance = DoubleVar()
        self.doubleVar_compliance.set(1e-4)
        
    def __initLabels(self):
    #This methods instanciates all the Labels displayed in the Single testbench GUI
        self.label_description = Label(self.frame, text="This test bench provides signal configuration to program a CBRAM cell", pady=20)
        self.label_description.configure(bg=self.bgColor, fg=self.textColor)
        self.label_description.grid(column=0, columnspan=2, row=0)

        self.label_startValue = Label(self.frame, textvariable=self.stringVar_startValue)
        self.label_startValue.configure(bg=self.bgColor, fg=self.textColor)
        self.label_startValue.grid(column=0, row=2)

        self.label_stopValue = Label(self.frame, textvariable=self.stringVar_stopValue)
        self.label_stopValue.configure(bg=self.bgColor, fg=self.textColor)
        self.label_stopValue.grid(column=0, row=3)

        self.label_time = Label(self.frame, textvariable=self.stringVar_time)
        self.label_time.configure(bg=self.bgColor, fg=self.textColor)
        self.label_time.grid(column=0, row=4)

        self.label_compliance = Label(self.frame, textvariable=self.stringVar_compliance)
        self.label_compliance.configure(bg=self.bgColor, fg=self.textColor)
        self.label_compliance.grid(column=0, row=5)

    def __initCombobox(self):
    #This methods instanciates all the combobox displayed in the Single testbench GUI
        self.combo_aimingState = Combobox(self.frame, state="readonly", width=30, values=["SET cell in LOW state", "SET cell in HIGH state"])
        self.combo_aimingState.bind("<<ComboboxSelected>>", self.combo_aimingState_callback)
        self.combo_aimingState.configure(background=self.bgColor)
        self.combo_aimingState.grid(column=0, columnspan=1, row=1)
        self.combo_aimingState.current(0)

    def combo_aimingState_callback(self, args=[]):
    #This method is called when an action is made on combo_aimingState
        if self.combo_aimingState.current() == 0:
            self.stringVar_time.set("Ramp : ")

        elif self.combo_aimingState.current() == 1:
            self.stringVar_time.set("Pulse width : ")

    def __initEntries(self):
    #This methods instanciates all the Entries displayed in the Single testbench GUI
        self.entry_startValue = Entry(self.frame, textvariable=self.doubleVar_startValue, width=15)
        self.entry_startValue.grid(column=1, row=2)

        self.entry_stopValue = Entry(self.frame, textvariable=self.doubleVar_stopValue, width=15)
        self.entry_stopValue.grid(column=1, row=3)

        self.entry_time = Entry(self.frame, textvariable=self.doubleVar_time, width=15)
        self.entry_time.grid(column=1, row=4)

        self.entry_compliance = Entry(self.frame, textvariable=self.doubleVar_compliance, width=15)
        self.entry_compliance.grid(column=1, row=5)

class Single_Model():
    """Class containing the Single_model testbench.

    """

    def __init__(self):
    #Constructor for the Single_model class
        print('bla')