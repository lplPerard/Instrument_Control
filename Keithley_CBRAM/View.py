"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for the application's view

"""
from Sequence import Sequence_view
from Parameters import Parameters

from tkinter import Tk   
from tkinter import Menu 

class View(Tk, Parameters):
    """Class containing the GUI for the CBRAM software according to the MCV model.

    """

    def __init__(self):
    #Constructor for the View class
        Tk.__init__(self)
        Parameters.__init__(self)

        self.__initView()
        self.__initMenu()
        
        self.configure(bg=self.bgColor)

    def __initView(self):
    #This method permits to create/actualize the view parameters
        
        self.configure(bg=self.bgColor)


    def __initMenu(self):
    #Barre de menu
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="General", menu=self.menu1)
        self.menu1.add_command(label="Save config", command=self.__saveConfig)
        self.menu1.add_command(label="Load config", command=self.__loadConfig)
        self.menu1.add_command(label="Parameters", command=self.__parameters)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quit", command=quit)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sequence", menu=self.menu2)        
        self.menu2.add_command(label="Single", command=self.__initSingle)
        self.menu2.add_command(label="Cycling", command=self.__initCycling)
        self.menu2.add_command(label="Stability", command=self.__initStability)        
        self.menu2.add_command(label="I/V Curve", command=self.__initIV)
        self.menu2.add_command(label="Intermediate Value", command=self.__initIntermediate)        

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Export", menu=self.menu3)
        self.menu3.add_command(label="Format .CSV", command=self.__exportCSV)
        self.menu3.add_command(label="Format .txt", command=self.__exportTXT)

        self.config(menu=self.menubar)

    def __saveConfig(self):
    #Callback function for save config menu1 option
        print('bla')

    def __loadConfig(self):
    #Callback function for load config menu1 option
        print('bla')

    def __parameters(self):
    #Callback function for parameters menu1 option
        print('bla')

    def __initSingle(self):
    #Callback function for Single menu2 option
        print('bla')

    def __initCycling(self):
    #Callback function for Cycling menu2 option
        print('bla')

    def __initStability(self):
    #Callback function for Stability menu2 option
        print('bla')

    def __initIV(self):
    #Callback function for I/V menu2 option
        print('bla')

    def __initIntermediate(self):
    #Callback function for Intermediate menu2 option
        print('bla')

    def __exportCSV(self):
    #Callback function for Format .CSV menu3 option
        print('bla')

    def __exportTXT(self):
    #Callback function for Format .txt menu3 option
        print('bla')