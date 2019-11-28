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

from tkinter.ttk import Combobox

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(Tk):

    def __init__(self):
    #Constructor for  the main window
        Tk.__init__(self)
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
        self.__initFigures()

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
        self.menubar.add_cascade(label="Export", menu=self.menu2)
        self.menu2.add_command(label="Format .CSV", command=self.exportCSV)
        self.menu2.add_command(label="Format .txt", command=self.exportTXT)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Calibrate", menu=self.menu3)
        self.menu3.add_command(label="Perform new Calibration", command=self.newCalibration)
        self.menu3.add_command(label="Reset Calibration", command=self.resetCalibration)

        self.config(menu=self.menubar)

    def __initFrames(self):
    #LabelFrames
        self.labelframe1 = LabelFrame(self, text="General Configuration", padx=25, pady=15, bg="gainsboro")
        self.labelframe1.grid(column=0, columnspan=2, row=0)

        self.labelframe2 = LabelFrame(self, text="Signal Configuration", padx=25, pady=15, bg="gainsboro")
        self.labelframe2.grid(column=0, columnspan=2, row=1)
        
    def __initCombobox(self):
    #Listes déroulantes
        self.liste1 = Combobox(self.labelframe1, state="readonly", width=60, values=["ligne1", "ligne2", "ligne3"])
        self.liste1.grid(column=0, row=0)
        self.liste1.configure(background="gainsboro")
        self.liste1.current(0)

        self.liste2 = Combobox(self.labelframe1, state="readonly", width=60, values=["SET cell in HIGH state", "SET cell in LOW state"])
        self.liste2.grid(column=0, row=1)
        self.liste2.configure(background="gainsboro")
        self.liste2.bind("<<ComboboxSelected>>", self.listeCallBack)
        self.liste2.current(0)

        self.liste3 = Combobox(self.labelframe1, state="readonly", width=60, values=["Voltage source", "Current Source"])
        self.liste3.grid(column=0, row=2)
        self.liste3.configure(background="gainsboro")
        self.liste3.bind("<<ComboboxSelected>>", self.listeCallBack)
        self.liste3.current(0)

    def __initStringVars(self):
    #StringVars
        self.label1_String = StringVar()
        self.label1_String.set("Start value (V) : ")
        
        self.label2_String = StringVar()
        self.label2_String.set("Stop value (V) : ")

        self.label3_String = StringVar()
        self.label3_String.set("Pulse Width (s) : ")

        self.label4_String = StringVar()
        self.label4_String.set("Current compliance (A) : ")

        self.entry1_String = DoubleVar()
        self.entry2_String = DoubleVar()
        self.entry3_String = DoubleVar()
        self.entry4_String = DoubleVar()

    def __initEntries(self):
    #Entries
        self.entry1 = Entry(self.labelframe2, textvariable=self.entry1_String , width=30)
        self.entry1.grid(column=1, row=0)

        self.entry2 = Entry(self.labelframe2, textvariable=self.entry2_String , width=30)
        self.entry2.grid(column=1, row=1)

        self.entry3 = Entry(self.labelframe2, textvariable=self.entry3_String , width=30)
        self.entry3.grid(column=1, row=2)

        self.entry4 = Entry(self.labelframe2, textvariable=self.entry4_String , width=30)
        self.entry4.grid(column=1, row=3)

    def __initLabels(self):
    #Labels
        self.label1 = Label(self.labelframe2, textvariable=self.label1_String) #Create a display section
        self.label1.grid(column=0, row=0)   #Attach the display section to the main window
        self.label1.configure(bg="gainsboro")

        self.label2 = Label(self.labelframe2, textvariable=self.label2_String) #Create a display section
        self.label2.grid(column=0, row=1)   #Attach the display section to the main window
        self.label2.configure(bg="gainsboro")

        self.label3 = Label(self.labelframe2, textvariable=self.label3_String) #Create a display section
        self.label3.grid(column=0, row=2)   #Attach the display section to the main window
        self.label3.configure(bg="gainsboro")

        self.label3 = Label(self.labelframe2, textvariable=self.label4_String) #Create a display section
        self.label3.grid(column=0, row=3)   #Attach the display section to the main window
        self.label3.configure(bg="gainsboro")

        self.copyright = Label(self, text="Copyright Grenoble-inp LCIS") #Create a display section
        self.copyright.grid(column=2, row=3)   #Attach the display section to the main window
        self.copyright.configure(bg="gainsboro")

    def __initButtons(self):
    #Boutons
        self.button1 = Button(self, text="Generate Command Script", padx=15, command=self.button1CallBack)
        self.button1.grid(column=0, row=2)
        self.button1.configure(bg="gainsboro")

        self.button2 = Button(self, text="Start Sequence", padx=15, command=self.button2CallBack)
        self.button2.grid(column=1, row=2)
        self.button2.configure(bg="gainsboro")

    def __initFigures(self):
    #Figures to Canvas
        x = np.linspace(0, 2 * np.pi, 50)
        y = np.sin(x)
        fig = Figure(figsize=(10, 12), dpi=80, facecolor="gainsboro")

        ax1 = fig.add_subplot(311)
        ax1.plot(x,y)
        ax1.set_xlabel("angle (radian)")
        ax1.set_ylabel("sin(x)")
        ax1.grid(True)

        ax2 = fig.add_subplot(312, sharex=ax1)
        ax2.plot(y,x)
        ax2.set_xlabel("angle (radian)")
        ax2.set_ylabel("sin(x)")
        ax2.grid(True)

        ax3 = fig.add_subplot(313, sharex=ax1)
        ax3.plot(x,y)
        ax3.set_xlabel("angle (radian)")
        ax3.set_ylabel("sin(x)")
        ax3.grid(True)

        graph = FigureCanvasTkAgg(fig, master=self)
        canva2 = graph.get_tk_widget()
        canva2.grid(column=2, row=0, rowspan=3)
        canva2.configure(bg="gainsboro")

    def listeCallBack(self, event):
    #Callback function for Combobox event
        if (self.liste2.current() == 1) and (self.liste3.current() == 1):
            self.label1_String.set("Start value (A) : ")
            self.label2_String.set("Stop value (A) : ")
            self.label3_String.set("Ramp (A/s) : ")
            self.label4_String.set("Compliance Voltage (V) : ")

        elif (self.liste2.current() == 1) and (self.liste3.current() == 0):
            self.label1_String.set("Start value (V) : ")
            self.label2_String.set("Stop value (V) : ")
            self.label3_String.set("Ramp (V/s) : ")
            self.label4_String.set("Compliance Current (A) : ")

        elif (self.liste2.current() == 0) and (self.liste3.current() == 0):
            self.label1_String.set("Start value (V) : ")
            self.label2_String.set("Stop value (V) : ")
            self.label3_String.set("Pulse Width (s) : ")
            self.label4_String.set("Compliance Curent (A) : ")

        elif (self.liste2.current() == 0) and (self.liste3.current() == 1):
            self.label1_String.set("Start value (A) : ")
            self.label2_String.set("Stop value (A) : ")
            self.label3_String.set("Pulse Width (s) : ")
            self.label4_String.set("Compliance Voltage (V) : ")

        else:
            pass

        self.label1.update_idletasks()
        print(self.label4_String.get())

    def button1CallBack(self):
    #Callback function for button1 event
        print("bla")

    def button2CallBack(self):
    #Callback function for button2 event
        print("bla")

    def saveConfig(self):
    #Callback function for menu1.saveConfig
        print("bla")

    def loadConfig(self):
    #Callback function for menu1.loadConfig
        print("bla")

    def exportCSV(self):
    #Callback function for menu2.exportCSV
        print("bla")

    def exportTXT(self):
    #Callback function for menu2.exportTXT
        print("bla")

    def newCalibration(self):
    #Callback function for menu3.newCalibration
        print("bla")

    def resetCalibration(self):
    #Callback function for menu3.resetCalibration
        print("bla")


"""This code contains the view for the CBRAM cell programming software

"""

if __name__ == "__main__":
    app = Application()
    app.title("CBRAM cells programmer")
    app.mainloop()