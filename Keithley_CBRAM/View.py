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
        self.generatePlotParam()

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
        self.labelframe1 = LabelFrame(self, text="General Configuration", padx=15, pady=5, bg="gainsboro")
        self.labelframe1.grid(column=0, columnspan=2, row=0)

        self.labelframe2 = LabelFrame(self, text="Signal Configuration", padx=15, pady=5, bg="gainsboro")
        self.labelframe2.grid(column=0, columnspan=2, row=1)

        self.labelframe3 = LabelFrame(self, text="Cell configuration", padx=15, pady=5, bg="gainsboro")
        self.labelframe3.grid(column=0, columnspan=2, row=2)
        
    def __initCombobox(self):
    #Listes déroulantes
        self.liste1 = Combobox(self.labelframe1, state="readonly", width=30, values=findInstruments())
        self.liste1.grid(column=0, row=0)
        self.liste1.configure(background="gainsboro")
        self.liste1.current(0)

        self.liste2 = Combobox(self.labelframe1, state="readonly", width=30, values=["SET cell in HIGH state", "SET cell in LOW state"])
        self.liste2.grid(column=0, row=2)
        self.liste2.configure(background="gainsboro")
        self.liste2.bind("<<ComboboxSelected>>", self.listeCallBack)
        self.liste2.current(0)

        self.liste3 = Combobox(self.labelframe1, state="readonly", width=30, values=["Voltage source", "Current Source"])
        self.liste3.grid(column=0, row=3)
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

        self.label5_String = StringVar()
        self.label5_String.set("Compensation resistance (Ohm)")

        self.label6_String = StringVar()
        self.label6_String.set("Current resistance State (Ohm): ")

        self.entry1_String = DoubleVar()

        self.entry2_String = DoubleVar()
        self.entry2_String.set(1)

        self.entry3_String = DoubleVar()
        self.entry3_String.set(1)

        self.entry4_String = DoubleVar()
        self.entry4_String.set(1e-3)

        self.entry5_String = DoubleVar()
        self.entry6_String = DoubleVar()

    def __initEntries(self):
    #Entries
        self.entry1 = Entry(self.labelframe2, textvariable=self.entry1_String , width=15)
        self.entry1.grid(column=1, row=0)

        self.entry2 = Entry(self.labelframe2, textvariable=self.entry2_String , width=15)
        self.entry2.grid(column=1, row=1)

        self.entry3 = Entry(self.labelframe2, textvariable=self.entry3_String , width=15)
        self.entry3.grid(column=1, row=2)

        self.entry4 = Entry(self.labelframe2, textvariable=self.entry4_String , width=15)
        self.entry4.grid(column=1, row=3)

        self.entry5 = Entry(self.labelframe3, textvariable=self.entry5_String , width=15)
        self.entry5.grid(column=1, row=0)

        self.entry6 = Entry(self.labelframe3, textvariable=self.entry6_String , width=15)
        self.entry6.grid(column=1, row=1)

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

        self.label4 = Label(self.labelframe2, textvariable=self.label4_String) #Create a display section
        self.label4.grid(column=0, row=3)   #Attach the display section to the main window
        self.label4.configure(bg="gainsboro")

        self.label5 = Label(self.labelframe3, textvariable=self.label5_String) #Create a display section
        self.label5.grid(column=0, row=0)   #Attach the display section to the main window
        self.label5.configure(bg="gainsboro")

        self.label6 = Label(self.labelframe3, textvariable=self.label6_String) #Create a display section
        self.label6.grid(column=0, row=1)   #Attach the display section to the main window
        self.label6.configure(bg="gainsboro")

        self.copyright = Label(self, text="Copyright Grenoble-inp LCIS") #Create a display section
        self.copyright.grid(column=2, row=4)   #Attach the display section to the main window
        self.copyright.configure(bg="gainsboro")

    def __initButtons(self):
    #Boutons
        self.button0 = Button(self.labelframe1, text="Actualize", padx=11, command=self.button0CallBack)
        self.button0.grid(column=0, row=1)
        self.button0.configure(bg="gainsboro")

        self.button1 = Button(self.labelframe3, text="Acquire Cell's resistance state", padx=11, command=self.button1CallBack)
        self.button1.grid(column=1, row=2)
        self.button1.configure(bg="gainsboro")

        self.button2 = Button(self, text="Actualize Sequence", padx=15, command=self.button2CallBack)
        self.button2.grid(column=0, row=3)
        self.button2.configure(bg="gainsboro")

        self.button3 = Button(self, text="Start Sequence", padx=15, command=self.button3CallBack)
        self.button3.grid(column=1, row=3)
        self.button3.configure(bg="gainsboro")

    def setFigures(self, t, Us, Is, Rs, Ps, Um=0, Im=0, Rm=0, Pm=0):
    #Figures to Canvas
        if Um==0 or Im==0 or Rm == 0 or Pm==0:
            Um = Um * np.ones(len(t))
            Im = Im * np.ones(len(t))
            Rm = Rm * np.ones(len(t))
            Pm = Pm * np.ones(len(t))

        self.fig = Figure(figsize=(15, 8), dpi=80, facecolor="gainsboro")

        self.axU = self.fig.add_subplot(221)
        self.axU.set_xlabel("Time (s)")
        self.axU.set_ylabel("Tension (V)")
        self.axU.grid(True)
        self.axU.step(t,Us)
        self.axU.step(t,Um)

        self.axI = self.fig.add_subplot(222, sharex=self.axU)
        self.axI.set_xlabel("Time (s)")
        self.axI.set_ylabel("Current (A)")
        self.axI.grid(True)
        self.axI.step(t,Is)
        self.axI.step(t,Im)

        self.axR = self.fig.add_subplot(223, sharex=self.axU)
        self.axR.set_xlabel("Time (s)")
        self.axR.set_ylabel("Resistance (Ohm)")
        self.axR.set_yscale('log')
        self.axR.grid(True)
        self.axR.step(t,Rs)
        self.axR.step(t,Rm)

        self.axP = self.fig.add_subplot(224, sharex=self.axU)
        self.axP.set_xlabel("Time (s)")
        self.axP.set_ylabel("Power (W)")
        self.axP.set_yscale('log')
        self.axP.grid(True)
        self.axP.step(t,Ps)
        self.axP.step(t,Pm)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=2, row=0, rowspan=3)
        self.canvas.get_tk_widget().configure(bg="gainsboro")

    def generatePlotParam(self, Um=0, Im=0):
    #Function to generate values to plot
        if Um!=0 or Im!=0:
            print("bla")
            #Bien penser à soustraire la résistance de compensation !

        else:
            if self.liste2.current()==1 and self.liste3.current()==0:
                span = self.entry2_String.get() - self.entry1_String.get()
                T_max = span / self.entry3_String.get()
                t = np.linspace(0, T_max, T_max/0.01)
                ramp = span/T_max

                Us = ramp * t - self.entry1_String.get()
                Rs = 1e6 - 990e3*t/T_max
                Is = Us/Rs        
                Ps = Us*Is

            elif self.liste2.current()==0 and self.liste3.current()==0:
                span = - abs(self.entry2_String.get() - self.entry1_String.get())
                T_max = self.entry3_String.get()
                t = np.linspace(0, T_max, T_max/0.01)

                Us = span * np.ones(int(T_max/0.01))
                Rs = 10 + 990e3*t/T_max
                Is = Us/Rs        
                Ps = Us*Is

            elif self.liste2.current()==1 and self.liste3.current()==1:
                span = self.entry2_String.get() - self.entry1_String.get()
                T_max = span / self.entry3_String.get()
                t = np.linspace(0, T_max, T_max/0.01)
                ramp = span/T_max

                Is = ramp * t - self.entry1_String.get()
                Rs = 1e6 - 990e3*t/T_max
                Us = Is*Rs        
                Ps = Us*Is

            elif self.liste2.current()==0 and self.liste3.current()==1:
                span = - abs(self.entry2_String.get() - self.entry1_String.get())
                T_max = self.entry3_String.get()
                t = np.linspace(0, T_max, T_max/0.01)

                Is = span * np.ones(int(T_max/0.01))
                Rs = 10 + 990e3*t/T_max
                Us = Is*Rs        
                Ps = Us*Is

            self.setFigures(t,Us,Is,Rs,Ps)
            
    def listeCallBack(self, event=None):
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

        self.update_idletasks()

    def button0CallBack(self):
    #Callback function for button0 event
        self.liste1.config(values=findInstruments())
        self.update_idletasks()
    
    def button1CallBack(self):
    #Callback function for button1 event
        R = resistanceMeasurement(self.liste1.get())
        if R >= 1e6:
            self.entry6_String.set(R/1e6)
            self.label6_String.set("Current resistance State (MOhm): ")
        elif R >= 1e3:
            self.entry6_String.set(R/1e3)
            self.label6_String.set("Current resistance State (kOhm): ")
        else:
            self.entry6_String.set(R)
            self.label6_String.set("Current resistance State (Ohm): ")
        self.update_idletasks()

    def button2CallBack(self):
    #Callback function for button2 event
        self.update_idletasks()
        self.generatePlotParam()

    def button3CallBack(self):
    #Callback function for button3 event
        R = resistanceMeasurement(self.liste1.get())

        if R >= 1e6 and self.liste2.current()==0:            
            showwarning(title="Start Sequence", message="Cell already in High resistance state")
            self.entry6_String.set(R/1e6)
            self.label6_String.set("Current resistance State (MOhm): ")

        elif R >= 1e3  and self.liste2.current()==0: 
            answer = askokcancel(title="Start Sequence", message="Cell currently in middle state R = " + str('%.2E' %R/1e3) + "kOhm\n Do you want to try to increase this resistance ?")
            self.entry6_String.set(R/1e3)
            self.label6_String.set("Current resistance State (kOhm): ")

            if self.liste3.current()==0 and answer==True:
                generateVoltageWaveform
            elif answer==True:
                generateCurrentWaveform

        elif self.liste2.current()==0: 
            self.entry6_String.set(R)
            self.label6_String.set("Current resistance State (Ohm): ")

            if self.liste3.current()==0:
                generateVoltageWaveform
            else:
                generateCurrentWaveform

        elif R >= 1e3  and self.liste2.current()==1: 
            if R >= 1e6:
                self.entry6_String.set(R/1e6)
                self.label6_String.set("Current resistance State (MOhm): ")
            elif R >= 1e3:
                self.entry6_String.set(R/1e3)
                self.label6_String.set("Current resistance State (kOhm): ")

            if self.liste3.current()==1:
                generateVoltageWaveform
            else:
                generateCurrentWaveform
                
        elif self.liste2.current()==1: 
            answer = askokcancel(title="Start Sequence", message="Cell currently in middle state R = " + str('%.2E'%R) + "Ohm\n Do you want to try to lower this resistance ?")
            if self.liste3.current()==0 and answer==True:
                generateVoltageWaveform
            elif answer==True:
                generateCurrentWaveform

    def saveConfig(self):
    #Callback function for menu1.saveConfig
        self.configFile.path = filedialog.asksaveasfilename(title = "Select file",filetypes = (("Config files","*.ini"),("all files","*.*")))
        if self.configFile.path != "":
            self.configFile.file = open(self.configFile.path, 'w')

            self.configFile.file.write(self.liste1.get() + "\n")
            self.configFile.file.write(self.liste2.get() + "\n")
            self.configFile.file.write(self.liste3.get() + "\n")
            self.configFile.file.write(str(self.entry1_String.get()) + "\n")
            self.configFile.file.write(str(self.entry2_String.get()) + "\n")
            self.configFile.file.write(str(self.entry3_String.get()) + "\n")
            self.configFile.file.write(str(self.entry4_String.get()) + "\n")
            self.configFile.file.write(str(self.entry5_String.get()) + "\n")

            self.configFile.file.close()

    def loadConfig(self):
    #Callback function for menu1.loadConfig
        self.configFile.path =  filedialog.askopenfilename(title = "Select file",filetypes = (("Config files","*.ini"),("all files","*.*")))
        print(self.configFile.path )
        if self.configFile.path != "":
            self.configFile.file = open(self.configFile.path, 'r')

            line = self.configFile.file.readline()[:-1]
            self.liste1.current(0)
            if line == self.liste1.get():
                pass    
            else:
                self.liste1.current(1)
                if line == self.liste1.get():
                    pass
                else:
                    self.liste1.current(2)
                    if line == self.liste1.get():
                        pass
                    else:
                        self.liste1.current(3)
                        if line == self.liste1.get():
                            pass
                        else:
                            self.liste1.current(4)
                            if line == self.liste1.get():
                                pass
                            else:
                                self.liste1.current(4)
                                if line == self.liste1.get():
                                    pass
                        
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

            self.entry1_String.set(float(self.configFile.file.readline()[:-1]))
            self.entry2_String.set(float(self.configFile.file.readline()[:-1]))
            self.entry3_String.set(float(self.configFile.file.readline()[:-1]))
            self.entry4_String.set(float(self.configFile.file.readline()[:-1]))
            self.entry5_String.set(float(self.configFile.file.readline()[:-1]))

        self.update_idletasks()
        self.listeCallBack()
        self.configFile.file.close()

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
            self.entry5_String.set(R/1000000)
            self.label5_String.set("Compensation resistance (MOhm)")
        elif R >= 1000:
            self.entry5_String.set(R/1000)
            self.label5_String.set("Compensation resistance (kOhm)")
        else:
            self.entry5_String.set(R)
            self.label5_String.set("Compensation resistance (Ohm)")
        self.update_idletasks()

    def resetCalibration(self):
    #Callback function for menu3.resetCalibration
        answer = askokcancel(title="Reset Calibration", message="Are you sure you want to reset calibration ?\nThis could impact future measurement")
        if answer:
            self.entry5_String.set(0)
            self.update_idletasks()

"""This code contains the view for the CBRAM cell programming software

"""

if __name__ == "__main__":
    app = Application()
    app.title("CBRAM cells programmer")
    app.mainloop()