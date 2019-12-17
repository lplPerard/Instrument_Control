"""This code contains the view for the CBRAM cell programming software

"""

from tkinter import Tk
from tkinter import Label 
from tkinter import Menu
from tkinter import Button
from tkinter import Entry
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.ttk import Combobox

from Class import ConfigFile

from Controller import *

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(Tk):

    def __init__(self):
    #Constructor for  the main window
        Tk.__init__(self)

        self.state="SINGLE"
        self.timeStep = 0.4

        self.configFile = ConfigFile()
        self.__initWidget()
        self.configure(bg="gainsboro")
        
    def __initWidget(self):
    #Widget initialization
        self.__initMenu()
        self.__initFrames()
        self.__initCombobox()
        self.__initStringVars()
        self.__initEntries()
        self.__initLabels()
        self.__initButtons()
        self.actualizeFigure()

    def __initMenu(self):
    #Barre de menu
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu1)
        self.menu1.add_command(label="Save config", command=self.saveConfig)
        self.menu1.add_command(label="Load config", command=self.loadConfig)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quit", command=quit)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sequence", menu=self.menu2)        
        self.menu2.add_command(label="Single", command=self.initSingle)
        self.menu2.add_command(label="Cycling", command=self.initCycling)
        self.menu2.add_command(label="Stability", command=self.initStability)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Calibrate", menu=self.menu3)
        self.menu3.add_command(label="Perform new Calibration", command=self.newCalibration)
        self.menu3.add_command(label="Reset Calibration", command=self.resetCalibration)

        self.menu4 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Export", menu=self.menu4)
        self.menu4.add_command(label="Format .CSV", command=self.exportCSV)
        self.menu4.add_command(label="Format .txt", command=self.exportTXT)

        self.config(menu=self.menubar)

    def __initFrames(self):
    #LabelFrames
        self.labelframe_generalConfig = LabelFrame(self, text="General Configuration", padx=15, pady=5, bg="gainsboro")
        self.labelframe_generalConfig.grid(column=0, columnspan=2, row=0)

        self.labelframe_singleConfig = LabelFrame(self, text="Signal Configuration", padx=15, pady=5, bg="gainsboro")
        self.labelframe_singleConfig.grid(column=0, columnspan=2, row=1)

        self.labelframe_cyclingConfig = LabelFrame(self, text="Cycle Test configuration", padx=15, pady=5, bg="gainsboro")

        self.labelframe_stabilityConfig = LabelFrame(self, text="Cycle Test configuration", padx=15, pady=5, bg="gainsboro")

        self.labelframe_cellConfig = LabelFrame(self, text="Cell configuration", padx=15, pady=5, bg="gainsboro")
        self.labelframe_cellConfig.grid(column=0, columnspan=2, row=2, padx=50)
        
    def __initCombobox(self):
    #Listes déroulantes
        self.liste1 = Combobox(self.labelframe_generalConfig, state="readonly", width=30, values=findInstruments())
        self.liste1.grid(column=0, row=0)
        self.liste1.configure(background="gainsboro")
        self.liste1.current(0)

        self.liste2 = Combobox(self.labelframe_generalConfig, state="readonly", width=30, values=["SET cell in HIGH state", "SET cell in LOW state"])
        self.liste2.grid(column=0, row=2)
        self.liste2.configure(background="gainsboro")
        self.liste2.bind("<<ComboboxSelected>>", self.listeCallBack)
        self.liste2.current(0)

        self.liste3 = Combobox(self.labelframe_generalConfig, state="readonly", width=30, values=["Voltage source", "Current Source"])
        self.liste3.grid(column=0, row=3)
        self.liste3.configure(background="gainsboro")
        self.liste3.bind("<<ComboboxSelected>>", self.listeCallBack)
        self.liste3.current(0)

    def __initStringVars(self):
    #StringVars
        self.label_String_1 = StringVar()
        self.label_String_1.set("Start value (V) : ")
        
        self.label_String_2 = StringVar()
        self.label_String_2.set("Stop value (V) : ")

        self.label_String_3 = StringVar()
        self.label_String_3.set("Pulse Width (s) : ")

        self.label_String_4 = StringVar()
        self.label_String_4.set("Current compliance (A) : ")

        self.label_String_5 = StringVar()
        self.label_String_5.set("Start value (V) : ")
        
        self.label_String_6 = StringVar()
        self.label_String_6.set("Stop value (V) : ")

        self.label_String_7 = StringVar()
        self.label_String_7.set("Pulse Width (s) : ")

        self.label_String_8 = StringVar()
        self.label_String_8.set("Current compliance (A) : ")

        self.label_String_9 = StringVar()
        self.label_String_9.set("Compensation resistance (Ohm)")

        self.label_String_10 = StringVar()
        self.label_String_10.set("Current resistance State (Ohm): ")

        self.entryS_frame1_1 = DoubleVar() #Start Value
        self.entryS_frame1_2 = DoubleVar() #Stop Value
        self.entryS_frame1_2.set(1)
        self.entryS_frame1_3 = DoubleVar() #Ramp/Width
        self.entryS_frame1_3.set(1)
        self.entryS_frame1_4 = DoubleVar()
        self.entryS_frame1_4.set(1e-3) #Compliance

        self.entryS_frame2_1 = DoubleVar() #Start Value
        self.entryS_frame2_2 = DoubleVar() #Stop Value
        self.entryS_frame2_2.set(1)
        self.entryS_frame2_3 = DoubleVar() #Ramp
        self.entryS_frame2_3.set(1)
        self.entryS_frame2_4 = DoubleVar()
        self.entryS_frame2_4.set(1e-3) #Compliance
        self.entryS_frame2_5 = DoubleVar() #Start Value
        self.entryS_frame2_6 = DoubleVar() #Stop Value
        self.entryS_frame2_6.set(1)
        self.entryS_frame2_7 = DoubleVar() #Width
        self.entryS_frame2_7.set(1)
        self.entryS_frame2_8 = DoubleVar()
        self.entryS_frame2_8.set(1e-3) #Compliance

        self.entryS_frame3_1 = DoubleVar() #Start Value
        self.entryS_frame3_2 = DoubleVar() #Stop Value
        self.entryS_frame3_2.set(1)
        self.entryS_frame3_3 = DoubleVar() #Ramp
        self.entryS_frame3_3.set(1)
        self.entryS_frame3_4 = DoubleVar()
        self.entryS_frame3_4.set(1e-3) #Compliance
        self.entryS_frame3_5 = DoubleVar() #Start Value
        self.entryS_frame3_6 = DoubleVar() #Stop Value
        self.entryS_frame3_6.set(1)
        self.entryS_frame3_7 = DoubleVar() #Width
        self.entryS_frame3_7.set(1)
        self.entryS_frame3_8 = DoubleVar()
        self.entryS_frame3_8.set(1e-3) #Compliance
        self.entryS_frame3_9 = DoubleVar()
        self.entryS_frame3_9.set(10) #Cycles

        self.entryS_frame4_1 = DoubleVar()
        self.entryS_frame4_2 = DoubleVar()

    def __initEntries(self):
    #Entries
        entry_frame1_1 = Entry(self.labelframe_singleConfig, textvariable=self.entryS_frame1_1, width=15)
        entry_frame1_1.grid(column=1, row=0)
        entry_frame1_2 = Entry(self.labelframe_singleConfig, textvariable=self.entryS_frame1_2, width=15)
        entry_frame1_2.grid(column=1, row=1)
        entry_frame1_3 = Entry(self.labelframe_singleConfig, textvariable=self.entryS_frame1_3, width=15)
        entry_frame1_3.grid(column=1, row=2)
        entry_frame1_4 = Entry(self.labelframe_singleConfig, textvariable=self.entryS_frame1_4, width=15)
        entry_frame1_4.grid(column=1, row=3)

        entry_frame2_1 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_1, width=15)
        entry_frame2_1.grid(column=1, row=0)
        entry_frame2_2 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_2, width=15)
        entry_frame2_2.grid(column=1, row=1)
        entry_frame2_3 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_3, width=15)
        entry_frame2_3.grid(column=1, row=2)
        entry_frame2_4 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_4, width=15)
        entry_frame2_4.grid(column=1, row=3)
        entry_frame2_5 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_5, width=15)
        entry_frame2_5.grid(column=1, row=5)
        entry_frame2_6 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_6, width=15)
        entry_frame2_6.grid(column=1, row=6)
        entry_frame2_7 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_7, width=15)
        entry_frame2_7.grid(column=1, row=7)
        entry_frame2_8 = Entry(self.labelframe_cyclingConfig, textvariable=self.entryS_frame2_8, width=15)
        entry_frame2_8.grid(column=1, row=8)

        entry_frame3_1 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_1, width=15)
        entry_frame3_1.grid(column=1, row=0)
        entry_frame3_2 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_2, width=15)
        entry_frame3_2.grid(column=1, row=1)
        entry_frame3_3 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_3, width=15)
        entry_frame3_3.grid(column=1, row=2)
        entry_frame3_4 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_4, width=15)
        entry_frame3_4.grid(column=1, row=3)
        entry_frame3_5 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_5, width=15)
        entry_frame3_5.grid(column=1, row=5)
        entry_frame3_6 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_6, width=15)
        entry_frame3_6.grid(column=1, row=6)
        entry_frame3_7 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_7, width=15)
        entry_frame3_7.grid(column=1, row=7)
        entry_frame3_8 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_8, width=15)
        entry_frame3_8.grid(column=1, row=8)
        entry_frame3_9 = Entry(self.labelframe_stabilityConfig, textvariable=self.entryS_frame3_9, width=15)
        entry_frame3_9.grid(column=1, row=10)

        entry_frame4_1 = Entry(self.labelframe_cellConfig, textvariable=self.entryS_frame4_1, state= "readonly", width=15)
        entry_frame4_1.grid(column=1, row=0)
        entry_frame4_2 = Entry(self.labelframe_cellConfig, textvariable=self.entryS_frame4_2, state= "readonly", width=15)
        entry_frame4_2.grid(column=1, row=1)

    def __initLabels(self):
    #Labels
        label_single_1 = Label(self.labelframe_singleConfig, textvariable=self.label_String_1) #Create a display section
        label_single_1.grid(column=0, row=0)   #Attach the display section to the main window
        label_single_1.configure(bg="gainsboro")

        label_single_2 = Label(self.labelframe_singleConfig, textvariable=self.label_String_2) #Create a display section
        label_single_2.grid(column=0, row=1)   #Attach the display section to the main window
        label_single_2.configure(bg="gainsboro")

        label_single_3 = Label(self.labelframe_singleConfig, textvariable=self.label_String_3) #Create a display section
        label_single_3.grid(column=0, row=2)   #Attach the display section to the main window
        label_single_3.configure(bg="gainsboro")

        label_single_4 = Label(self.labelframe_singleConfig, textvariable=self.label_String_4) #Create a display section
        label_single_4.grid(column=0, row=3)   #Attach the display section to the main window
        label_single_4.configure(bg="gainsboro")

        label_config_1 = Label(self.labelframe_cellConfig, textvariable=self.label_String_9) #Create a display section
        label_config_1.grid(column=0, row=0)   #Attach the display section to the main window
        label_config_1.configure(bg="gainsboro")

        label_config_2 = Label(self.labelframe_cellConfig, textvariable=self.label_String_10) #Create a display section
        label_config_2.grid(column=0, row=1)   #Attach the display section to the main window
        label_config_2.configure(bg="gainsboro")

        label_cycling_1 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_1) #Create a display section
        label_cycling_1.grid(column=0, row=0)   #Attach the display section to the main window
        label_cycling_1.configure(bg="gainsboro")

        label_cycling_2 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_2) #Create a display section
        label_cycling_2.grid(column=0, row=1)   #Attach the display section to the main window
        label_cycling_2.configure(bg="gainsboro")

        label_cycling_3 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_3) #Create a display section
        label_cycling_3.grid(column=0, row=2)   #Attach the display section to the main window
        label_cycling_3.configure(bg="gainsboro")

        label_cycling_4 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_4) #Create a display section
        label_cycling_4.grid(column=0, row=3)   #Attach the display section to the main window
        label_cycling_4.configure(bg="gainsboro")

        label0 = Label(self.labelframe_cyclingConfig, text="") #Create a display section
        label0.grid(column=0, row=4,)   #Attach the display section to the main window
        label0.configure(bg="gainsboro")

        label_cycling_5 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_5) #Create a display section
        label_cycling_5.grid(column=0, row=5,)   #Attach the display section to the main window
        label_cycling_5.configure(bg="gainsboro")

        label_cycling_6 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_6) #Create a display section
        label_cycling_6.grid(column=0, row=6)   #Attach the display section to the main window
        label_cycling_6.configure(bg="gainsboro")

        label_cycling_7 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_7) #Create a display section
        label_cycling_7.grid(column=0, row=7)   #Attach the display section to the main window
        label_cycling_7.configure(bg="gainsboro")

        label_cycling_8 = Label(self.labelframe_cyclingConfig, textvariable=self.label_String_8) #Create a display section
        label_cycling_8.grid(column=0, row=8)   #Attach the display section to the main window
        label_cycling_8.configure(bg="gainsboro")

        copyright = Label(self, text="Copyright Grenoble-inp LCIS") #Create a display section
        copyright.grid(column=2, row=4)   #Attach the display section to the main window
        copyright.configure(bg="gainsboro")
        
        label_stability_1 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_1) #Create a display section
        label_stability_1.grid(column=0, row=0)   #Attach the display section to the main window
        label_stability_1.configure(bg="gainsboro")

        label_stability_2 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_2) #Create a display section
        label_stability_2.grid(column=0, row=1)   #Attach the display section to the main window
        label_stability_2.configure(bg="gainsboro")

        label_stability_3 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_3) #Create a display section
        label_stability_3.grid(column=0, row=2)   #Attach the display section to the main window
        label_stability_3.configure(bg="gainsboro")

        label_stability_4 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_4) #Create a display section
        label_stability_4.grid(column=0, row=3)   #Attach the display section to the main window
        label_stability_4.configure(bg="gainsboro")

        label1 = Label(self.labelframe_stabilityConfig, text="") #Create a display section
        label1.grid(column=0, row=4,)   #Attach the display section to the main window
        label1.configure(bg="gainsboro")

        label_stability_5 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_5) #Create a display section
        label_stability_5.grid(column=0, row=5,)   #Attach the display section to the main window
        label_stability_5.configure(bg="gainsboro")

        label_stability_6 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_6) #Create a display section
        label_stability_6.grid(column=0, row=6)   #Attach the display section to the main window
        label_stability_6.configure(bg="gainsboro")

        label_stability_7 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_7) #Create a display section
        label_stability_7.grid(column=0, row=7)   #Attach the display section to the main window
        label_stability_7.configure(bg="gainsboro")

        label_stability_8 = Label(self.labelframe_stabilityConfig, textvariable=self.label_String_8) #Create a display section
        label_stability_8.grid(column=0, row=8)   #Attach the display section to the main window
        label_stability_8.configure(bg="gainsboro")

        label2 = Label(self.labelframe_stabilityConfig, text="") #Create a display section
        label2.grid(column=0, row=9,)   #Attach the display section to the main window
        label2.configure(bg="gainsboro")

        label_stability_9 = Label(self.labelframe_stabilityConfig, text="Number of cycles") #Create a display section
        label_stability_9.grid(column=0, row=10)   #Attach the display section to the main window
        label_stability_9.configure(bg="gainsboro")

    def __initButtons(self):
    #Boutons
        self.button0 = Button(self.labelframe_generalConfig, text="Actualize", padx=11, command=self.button0CallBack)
        self.button0.grid(column=0, row=1)
        self.button0.configure(bg="gainsboro")

        self.button1 = Button(self.labelframe_cellConfig, text="Acquire Cell's resistance state", padx=11, command=self.button1CallBack)
        self.button1.grid(column=1, row=2)
        self.button1.configure(bg="gainsboro")

        self.button2 = Button(self, text="Actualize Sequence", padx=15, command=self.button2CallBack)
        self.button2.grid(column=0, row=3)
        self.button2.configure(bg="gainsboro")

        self.button3 = Button(self, text="Start Sequence", padx=15, command=self.button3CallBack)
        self.button3.grid(column=1, row=3)
        self.button3.configure(bg="gainsboro")

    def setFigures(self, TL=0, TR=0, BL=0, BR=0):
    #Figures to Canvas
        if TL==0 or TR==0 or BL == 0 or BR==0:
            TL = TL * np.ones(len(self.t))
            TR = TR * np.ones(len(self.t))
            BL = BL * np.ones(len(self.t))
            BR = BR * np.ones(len(self.t))

        self.fig = Figure(figsize=(15, 9), dpi=70, facecolor="gainsboro")

        self.plotTL = self.fig.add_subplot(221)
        self.plotTL.set_xlabel("Time (s)")
        self.plotTL.set_ylabel("Tension (V)")
        self.plotTL.grid(True)
        self.plotTL.step(self.t,self.TL)
        self.plotTL.step(self.t,TL)

        self.plotTR = self.fig.add_subplot(222)
        self.plotTR.set_xlabel("Time (s)")
        self.plotTR.set_ylabel("Current (mA)")
        self.plotTR.grid(True)
        self.plotTR.step(self.t,self.TR*1000)
        self.plotTR.step(self.t,TR*1000)

        self.plotBL = self.fig.add_subplot(223)
        self.plotBL.set_xlabel("Time (s)")
        self.plotBL.set_ylabel("Resistance (Ohm)")
        self.plotBL.set_yscale('log')
        self.plotBL.grid(True)
        self.plotBL.step(self.t,self.BL)
        self.plotBL.step(self.t,BL)

        self.plotBR = self.fig.add_subplot(224)
        self.plotBR.set_xlabel("Time (s)")
        self.plotBR.set_ylabel("Power (W)")
        self.plotBR.set_yscale('log')
        self.plotBR.grid(True)
        self.plotBR.step(self.t,self.BR)
        self.plotBR.step(self.t,BR)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=2, row=0, rowspan=3)
        self.canvas.get_tk_widget().configure(bg="gainsboro")

    def actualizeFigure(self, Um=0, Im=0):
    #Function to generate values to plot
        if self.state == "SINGLE":
            self.plotSingleSequence()
            self.setFigures()

        elif self.state == "CYCLING":
            self.plotCyclingSequence()
            self.setFigures()

        elif self.state == "STABILITY":
            self.plotStabilitySequence()
            self.setFigures()
            self.plotBL.set_xlabel("Cycle")
            self.plotBL.set_ylabel("Resistance")
            
        if Um!=0 or Im!=0:
            print("bla")
            #Bien penser à soustraire la résistance de compensation !

    def plotSingleSequence(self):
    #Function to generate preview of the sequence as it should be performed by the instrument
        if self.liste2.current()==1 and self.liste3.current()==0:
            span = self.entryS_frame1_2.get() - self.entryS_frame1_1.get()
            T_max = span / self.entryS_frame1_3.get()
            self.t = np.linspace(0, T_max, T_max/self.timeStep)
            ramp = span/T_max

            self.TL = ramp * self.t + self.entryS_frame1_1.get()
            self.BL = 1e6 - 990e3*self.t/T_max
            self.TR = self.TL/self.BL        
            self.BR = self.TL*self.TR

        elif self.liste2.current()==0 and self.liste3.current()==0:
            span = - abs(self.entryS_frame1_2.get() - self.entryS_frame1_1.get())
            T_max = self.entryS_frame1_3.get()
            self.t = np.linspace(0, T_max, T_max/self.timeStep)

            self.TL = span * np.ones(len(self.t)) + self.entryS_frame1_1.get()
            self.BL = 10 + 990e3*self.t/T_max
            self.TR = self.TL/self.BL        
            self.BR = self.TL*self.TR

        elif self.liste2.current()==1 and self.liste3.current()==1:
            span = self.entryS_frame1_2.get() - self.entryS_frame1_1.get()
            T_max = span / self.entryS_frame1_3.get()
            self.t = np.linspace(0, T_max, T_max/self.timeStep)
            ramp = span/T_max

            self.TR = ramp * self.t + self.entryS_frame1_1.get()
            self.BL = 1e6 - 990e3*self.t/T_max
            self.TL = self.TR*self.BL        
            self.BR = self.TL*self.TR

        elif self.liste2.current()==0 and self.liste3.current()==1:
            span = - abs(self.entryS_frame1_2.get() - self.entryS_frame1_1.get())
            T_max = self.entryS_frame1_3.get()
            self.t = np.linspace(0, T_max, T_max/self.timeStep)

            self.TR = span * np.ones(len(self.t)) + self.entryS_frame1_1.get()
            self.BL = 10 + 990e3*self.t/T_max
            self.TL = self.TR*self.BL        
            self.BR = self.TL*self.TR
            
    def plotCyclingSequence(self):
    #Function to generate preview of the sequence as it should be performed by the instrument
        span1 = self.entryS_frame2_2.get() - self.entryS_frame2_1.get()
        span2 = -abs(self.entryS_frame2_6.get() - self.entryS_frame2_5.get())

        T1 = span1 / self.entryS_frame2_3.get()
        time1 = np.linspace(0, T1, T1/self.timeStep)

        T2 = self.entryS_frame2_7.get()
        time2 = np.linspace(0, T2, T2/self.timeStep)

        T_max = 2*(T1+T2)
        self.t = np.linspace(0, T_max, 2*(len(time1) + len(time2)))
        ramp = span1/T1
        
        if self.liste3.current()==0:
            self.TL = np.concatenate((ramp * time1 + self.entryS_frame2_1.get(), span2 * np.ones(len(time2)) + self.entryS_frame2_5.get(), ramp * time1 + self.entryS_frame2_1.get(), span2 * np.ones(len(time2)) + self.entryS_frame2_5.get()))
            self.BL = 10 + 990e3*self.t/T_max
            self.TR = self.TL/self.BL        
            self.BR = self.TL*self.TR

        elif self.liste3.current()==1:

            self.TR = np.concatenate((ramp * time1 - self.entryS_frame2_1.get(), span2 * np.ones(len(time2)), ramp * time1 - self.entryS_frame2_1.get(), span2 * np.ones(len(time2))))
            self.BL = 10 + 990e3*self.t/T_max
            self.TL = self.TR*self.BL        
            self.BR = self.TL*self.TR

    def plotStabilitySequence(self):
    #Function to generate preview of the sequence as it should be performed by the instrument
        cycles = self.entryS_frame3_9.get()
        span1 = self.entryS_frame3_2.get() - self.entryS_frame3_1.get()
        span2 = -abs(self.entryS_frame3_6.get() - self.entryS_frame3_5.get())

        T1 = span1 / self.entryS_frame3_3.get()
        time1 = np.linspace(0, T1, T1/self.timeStep)

        T2 = self.entryS_frame3_7.get()
        time2 = np.linspace(0, T2, T2/self.timeStep)

        T_max = cycles * (T1+T2)
        self.t = np.linspace(0, T_max, cycles*(len(time1) + len(time2)))
        ramp = span1/T1
        
        if self.liste3.current()==0:
            i=0
            self.TL = np.concatenate((ramp * time1 + self.entryS_frame2_1.get(), span2 * np.ones(len(time2)) + self.entryS_frame2_5.get()))
            while(i < cycles - 1):
                self.TL = np.concatenate((ramp * time1 + self.entryS_frame2_1.get(), span2 * np.ones(len(time2)) + self.entryS_frame2_5.get(), self.TL))
                i+=1
            
            self.BL = 10 + 990e3*self.t/T_max
            self.TR = self.TL/self.BL        
            self.BR = self.TL*self.TR

        elif self.liste3.current()==1:
            i=0
            self.TR = np.concatenate((ramp * time1 + self.entryS_frame2_1.get(), span2 * np.ones(len(time2)) + self.entryS_frame2_5.get()))
            while(i < cycles - 1):
                self.TR = np.concatenate((ramp * time1 + self.entryS_frame2_1.get(), span2 * np.ones(len(time2)) + self.entryS_frame2_5.get(), self.TR))
                i+=1
            
            self.BL = 10 + 990e3*self.t/T_max
            self.TL = self.TR*self.BL        
            self.BR = self.TL*self.TR

    def listeCallBack(self, event=None):
    #Callback function for Combobox event
        if (self.liste2.current() == 1) and (self.liste3.current() == 1):
            self.label_String_1.set("Start value (A) : ")
            self.label_String_2.set("Stop value (A) : ")
            self.label_String_3.set("Ramp (A/s) : ")
            self.label_String_4.set("Compliance Voltage (V) : ")

            self.label_String_5.set("Start value (A) : ")
            self.label_String_6.set("Stop value (A) : ")
            self.label_String_7.set("Pulse Width (s) : ")
            self.label_String_8.set("Compliance Voltage (V) : ")

        elif (self.liste2.current() == 1) and (self.liste3.current() == 0):
            self.label_String_1.set("Start value (V) : ")
            self.label_String_2.set("Stop value (V) : ")
            self.label_String_3.set("Ramp (V/s) : ")
            self.label_String_4.set("Compliance Current (A) : ")

            self.label_String_5.set("Start value (V) : ")
            self.label_String_6.set("Stop value (V) : ")
            self.label_String_7.set("Pulse Width (s) : ")
            self.label_String_8.set("Compliance Current (A) : ")

        elif (self.liste2.current() == 0) and (self.liste3.current() == 0):
            self.label_String_1.set("Start value (V) : ")
            self.label_String_2.set("Stop value (V) : ")
            self.label_String_3.set("Pulse Width (s) : ")
            self.label_String_4.set("Compliance Curent (A) : ")

            self.label_String_5.set("Start value (V) : ")
            self.label_String_6.set("Stop value (V) : ")
            self.label_String_7.set("Pulse Width (s) : ")
            self.label_String_8.set("Compliance Current (A) : ")

        elif (self.liste2.current() == 0) and (self.liste3.current() == 1):
            self.label_String_1.set("Start value (A) : ")
            self.label_String_2.set("Stop value (A) : ")
            self.label_String_3.set("Pulse Width (s) : ")
            self.label_String_4.set("Compliance Voltage (V) : ")

            self.label_String_5.set("Start value (A) : ")
            self.label_String_6.set("Stop value (A) : ")
            self.label_String_7.set("Pulse Width (s) : ")
            self.label_String_8.set("Compliance Voltage (V) : ")

        else:
            pass

        self.update_idletasks()

    def button0CallBack(self):
    #Callback function for button0 event
        self.liste1.config(values=findInstruments())
        self.update_idletasks()
    
    def button1CallBack(self):
    #Callback function for button1 event
        R = resistanceMeasurement(self.liste1.get())
        if R >= 1e6:
            self.entryS_frame4_2.set(R/1e6)
            self.label_String_10.set("Current resistance State (MOhm): ")
        elif R >= 1e3:
            self.entryS_frame4_2.set(R/1e3)
            self.label_String_10.set("Current resistance State (kOhm): ")
        else:
            self.entryS_frame4_2.set(R)
            self.label_String_10.set("Current resistance State (Ohm): ")
        self.update_idletasks()

    def button2CallBack(self):
    #Callback function for button2 event
        self.update_idletasks()
        self.actualizeFigure()

    def button3CallBack(self):
    #Callback function for button3 event
        self.button2CallBack()

        if self.state == "SINGLE":
            self.generateSingleSequence()

        elif self.state == "CYCLING":
            self.generateCyclingSequence()

        elif self.state == "STABILITY":
            self.generateStabilitySequence()       

    def generateSingleSequence(self):
    #Function to generate the waveform to send to the instrument for a Single sequence
        instr = self.liste1.get()
        R = resistanceMeasurement(instr)
        lim = self.entryS_frame1_4.get()

        if R >= 1e6 and self.liste2.current()==0:            
            showwarning(title="Start Sequence", message="Cell already in High resistance state")
            self.entryS_frame4_2.set(R/1e6)
            self.label_String_10.set("Current resistance State (MOhm): ")

        elif R >= 1e3  and self.liste2.current()==0: 
            answer = askokcancel(title="Start Sequence", message="Cell currently in middle state R = " + str('%.2E' %R/1e3) + "kOhm\n Do you want to try to increase this resistance ?")
            self.entryS_frame4_2.set(R/1e3)
            self.label_String_10.set("Current resistance State (kOhm): ")

            if self.liste3.current()==0 and answer==True:
                generateVoltageWaveform(instr, self.TL, lim)
            elif answer==True:
                generateCurrentWaveform(instr, self.TR, lim)

        elif self.liste2.current()==0: 
            self.entryS_frame4_2.set(R)
            self.label_String_10.set("Current resistance State (Ohm): ")

            if self.liste3.current()==0:
                generateVoltageWaveform(instr, self.TL, lim)
            else:
                generateCurrentWaveform(instr, self.TR, lim)

        elif R >= 1e3  and self.liste2.current()==1: 
            if R >= 1e6:
                self.entryS_frame4_2.set(R/1e6)
                self.label_String_10.set("Current resistance State (MOhm): ")
            elif R >= 1e3:
                self.entryS_frame4_2.set(R/1e3)
                self.label_String_10.set("Current resistance State (kOhm): ")

            if self.liste3.current()==0:
                generateVoltageWaveform(instr, self.TL, lim)
            else:
                generateCurrentWaveform(instr, self.TR, lim)
                
        elif self.liste2.current()==1: 
            answer = askokcancel(title="Start Sequence", message="Cell currently in middle state R = " + str('%.2E'%R) + "Ohm\n Do you want to try to lower this resistance ?")
            self.entryS_frame4_2.set(R)
            self.label_String_10.set("Current resistance State (Ohm): ")
            if self.liste3.current()==0 and answer==True:
                generateVoltageWaveform(instr, self.TL, lim)
            elif answer==True:
                generateCurrentWaveform(instr, self.TR, lim)

    def generateCyclingSequence(self):
    #Function to generate the waveform to send to the instrument for a Cycling sequence
        print("bla")

    def generateStabilitySequence(self):
    #Function to generate the waveform to send to the instrument for a Stability sequence
        print("bla")

    def saveConfig(self):
    #Callback function for menu1.saveConfig
            if self.state == "SINGLE":
                self.saveSingleConfig()

            elif self.state == "CYCLING":
                self.saveCyclingConfig()

            elif self.state == "STABILITY":
                self.saveStabilityConfig() 

    def saveSingleConfig(self):
    #Function to save Single sequence
        self.configFile.path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("Config files","*.ini"),("all files","*.*")))
        if self.configFile.path != "":
            self.configFile.file = open(self.configFile.path, 'w')

            self.configFile.file.write(self.state + "\n")  #Save state as line 1

            self.configFile.file.write(self.liste1.get() + "\n") #Save general config
            self.configFile.file.write(self.liste2.get() + "\n")
            self.configFile.file.write(self.liste3.get() + "\n")

            self.configFile.file.write(str(self.entryS_frame1_1.get()) + "\n") #Save signal parameters
            self.configFile.file.write(str(self.entryS_frame1_2.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame1_3.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame1_4.get()) + "\n")
            
            self.configFile.file.write(str(self.entryS_frame4_1.get()) + "\n") #Save Compensation resistance

            self.configFile.file.close()

    def saveCyclingConfig(self):
    #Function to save Cycling Sequence
        self.configFile.path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("Config files","*.ini"),("all files","*.*")))
        if self.configFile.path != "":
            self.configFile.file = open(self.configFile.path, 'w')

            self.configFile.file.write(self.state + "\n")  #Save state as line 1

            self.configFile.file.write(self.liste1.get() + "\n") #Save general config
            self.configFile.file.write(self.liste3.get() + "\n")

            self.configFile.file.write(str(self.entryS_frame2_1.get()) + "\n") #Save signals parameters
            self.configFile.file.write(str(self.entryS_frame2_2.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame2_3.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame2_4.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame2_5.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame2_6.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame2_7.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame2_8.get()) + "\n")
            
            self.configFile.file.write(str(self.entryS_frame4_1.get()) + "\n") #Save Compensation resistance

            self.configFile.file.close()

    def saveStabilityConfig(self):
    #Function to save Stability sequence
        self.configFile.path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("Config files","*.ini"),("all files","*.*")))
        if self.configFile.path != "":
            self.configFile.file = open(self.configFile.path, 'w')

            self.configFile.file.write(self.state + "\n")  #Save state as line 1

            self.configFile.file.write(self.liste1.get() + "\n") #Save general config
            self.configFile.file.write(self.liste3.get() + "\n")

            self.configFile.file.write(str(self.entryS_frame3_1.get()) + "\n") #Save signals parameters
            self.configFile.file.write(str(self.entryS_frame3_2.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_3.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_4.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_5.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_6.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_7.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_8.get()) + "\n")
            self.configFile.file.write(str(self.entryS_frame3_9.get()) + "\n") #Save Cycles
            
            self.configFile.file.write(str(self.entryS_frame4_1.get()) + "\n") #Save Compensation resistance

            self.configFile.file.close()

    def loadConfig(self):
    #Callback function for menu1.loadConfig
        self.configFile.path =  filedialog.askopenfilename(title = "Select file",filetypes = (("Config files","*.ini"),("all files","*.*")))
        print(self.configFile.path )
        if self.configFile.path != "":
            self.configFile.file = open(self.configFile.path, 'r')
            state = self.configFile.file.readline()[:-1]

            if state == "SINGLE":
                self.loadSingleConfig()
                self.initSingle()

            elif state == "CYCLING":
                self.loadCyclingConfig()
                self.initCycling

            elif state == "STABILITY":
                self.loadStabilityConfig()
                self.initStability  

            self.configFile.file.close()

    def loadSingleConfig(self):
    #Function to load a config for Single sequence
        i=0
        line = self.configFile.file.readline()[:-1]
        self.liste1.current(0)
        while self.liste1.current() != -1:
            if line == self.liste1.get():
                break
            else:
                i+=1
                self.liste1.current(i)

        if self.liste1.current() == -1:
            showerror(title="Load Config", message="Cannot find Desired instrument : " + line)

                    
        line = self.configFile.file.readline()[:-1]
        self.liste2.current(0)
        if line == self.liste2.get():
            pass
        else:
            self.liste2.current(1)
            if line == self.liste2.get():
                pass

        line = self.configFile.file.readline()[:-1]
        self.liste3.current(0)
        if line == self.liste3.get():
            pass
        else:
            self.liste3.current(1)
            if line == self.liste3.get():
                pass

        self.entryS_frame1_1.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame1_2.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame1_3.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame1_4.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame4_1.set(float(self.configFile.file.readline()[:-1]))

        self.update_idletasks()
        self.listeCallBack()
        self.configFile.file.close()
        self.actualizeFigure()

    def loadCyclingConfig(self):
    #Function to load a config for Single sequence
        i=0
        line = self.configFile.file.readline()[:-1]
        self.liste1.current(0)
        while self.liste1.current() != -1:
            if line == self.liste1.get():
                break
            else:
                i+=1
                self.liste1.current(i)

        if self.liste1.current() == -1:
            showerror(title="Load Config", message="Cannot find Desired instrument : " + line)
            self.liste2.current(1)
            if line == self.liste2.get():
                pass

        line = self.configFile.file.readline()[:-1]
        self.liste3.current(0)
        if line == self.liste3.get():
            pass
        else:
            self.liste3.current(1)
            if line == self.liste3.get():
                pass

        self.entryS_frame2_1.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_2.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_3.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_4.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_5.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_6.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_7.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame2_8.set(float(self.configFile.file.readline()[:-1]))

        self.entryS_frame4_1.set(float(self.configFile.file.readline()[:-1]))

        self.update_idletasks()
        self.listeCallBack()
        self.configFile.file.close()
        self.actualizeFigure()

    def loadStabilityConfig(self):
    #Function to load a config for Single sequence
        i=0
        line = self.configFile.file.readline()[:-1]
        self.liste1.current(0)
        while self.liste1.current() != -1:
            if line == self.liste1.get():
                break
            else:
                i+=1
                self.liste1.current(i)

        if self.liste1.current() == -1:
            showerror(title="Load Config", message="Cannot find Desired instrument : " + line)
            self.liste2.current(1)
            if line == self.liste2.get():
                pass

        line = self.configFile.file.readline()[:-1]
        self.liste3.current(0)
        if line == self.liste3.get():
            pass
        else:
            self.liste3.current(1)
            if line == self.liste3.get():
                pass

        self.entryS_frame3_1.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_2.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_3.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_4.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_5.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_6.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_7.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_8.set(float(self.configFile.file.readline()[:-1]))
        self.entryS_frame3_9.set(float(self.configFile.file.readline()[:-1]))

        self.entryS_frame4_1.set(float(self.configFile.file.readline()[:-1]))

        self.update_idletasks()
        self.listeCallBack()
        self.configFile.file.close()
        self.actualizeFigure()

    def exportCSV(self):
    #Callback function for menu2.exportCSV
        print("bla")

    def exportTXT(self):
    #Callback function for menu2.exportTXT
        print("bla")

    def newCalibration(self):
    #Callback function for menu3.newCalibration
        answer = showinfo(title="New Calibration", message="Short electrodes then press OK")
        if answer:
            R = resistanceMeasurement(self.liste1.get())
        if R >= 1000000:
            self.entryS_frame4_1.set(R/1000000)
            self.label_String_9.set("Compensation resistance (MOhm)")
        elif R >= 1000:
            self.entryS_frame4_1.set(R/1000)
            self.label_String_9.set("Compensation resistance (kOhm)")
        else:
            self.entryS_frame4_1.set(R)
            self.label_String_9.set("Compensation resistance (Ohm)")
        self.update_idletasks()

    def resetCalibration(self):
    #Callback function for menu3.resetCalibration
        answer = askokcancel(title="Reset Calibration", message="Are you sure you want to reset calibration ?\nThis could impact future measurement")
        if answer:
            self.entryS_frame4_1.set(0)
            self.update_idletasks()

    def initSingle(self):
        self.state="SINGLE"
        
        self.liste2.config(state='enable')
        self.listeCallBack()

        self.labelframe_cyclingConfig.grid_forget()
        self.labelframe_stabilityConfig.grid_forget()
        self.labelframe_singleConfig.grid(column=0, columnspan=2, row=1)

        self.actualizeFigure()

    def initCycling(self):
        self.state="CYCLING"

        self.liste2.current(1)
        self.liste2.config(state='disabled')
        self.listeCallBack()

        self.labelframe_singleConfig.grid_forget()
        self.labelframe_stabilityConfig.grid_forget()
        self.labelframe_cyclingConfig.grid(column=0, columnspan=2, row=1)

        self.actualizeFigure()

    def initStability(self):
        self.state="STABILITY"

        self.liste2.current(1)
        self.liste2.config(state='disabled')
        self.listeCallBack()

        self.labelframe_singleConfig.grid_forget()
        self.labelframe_cyclingConfig.grid_forget()
        self.labelframe_stabilityConfig.grid(column=0, columnspan=2, row=1)

        self.actualizeFigure()

"""This code contains the view for the CBRAM cell programming software

"""

if __name__ == "__main__":
    app = Application()
    app.title("CBRAM cells programmer")
    app.mainloop()