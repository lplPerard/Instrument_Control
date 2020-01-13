"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for the application's view

"""
from Single import Single_view

from Parameters import Parameters
from Parameters_view import Parameters_view

from tkinter import Tk   
from tkinter import Label
from tkinter import Menu 

class View(Tk, Parameters):
    """Class containing the GUI for the CBRAM software according to the MCV model.

    """

    def __init__(self):
    #Constructor for the View class
        Tk.__init__(self)
        Parameters.__init__(self)
        
        self.parameters_view = Parameters_view(self)
        self.parameters_view.frame.grid(column=1, row=0)
        self.singleSequence = Single_view(self)
        self.singleSequence.initFrame(text="Single Sequence", column=0,row=0, rowspan=10, bg=self.bgColor)

        self.__initWidgets()
        self.__actualizeView()

    def __initWidgets(self):
    #This method is used to encapsulate the creation of sequences and menues
        self.__initMenu()

        self.copyright = Label(self, text="Copyright grenoble-inp LCIS", bg=self.bgColor)
        self.copyright.grid(column=0, row=11)

    def __initMenu(self):
    #This method generates a Menu bar which give access to the diffent software's tools
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Configuration", menu=self.menu1)
        self.menu1.add_command(label="Save", command=self.menu1_save_callBack)
        self.menu1.add_command(label="Load", command=self.menu1_load_callBack)
        self.menu1.add_command(label="Parameters", command=self.menu1_parameters_callBack)        
        self.menu1.add_separator()
        self.menu1.add_command(label="Quit", command=quit)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sequence", menu=self.menu2)        
        self.menu2.add_command(label="Single", command=self.menu2_Single_callBack)
        self.menu2.add_command(label="Cycling", command=self.menu2_Cycling_callBack)
        self.menu2.add_command(label="Stability", command=self.menu2_Stability_callBack)        
        self.menu2.add_command(label="I/V Curve", command=self.menu2_IV_callBack)
        self.menu2.add_command(label="Intermediate Value", command=self.menu2_Intermediate_callBack)        

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Export", menu=self.menu3)
        self.menu3.add_command(label="Format .CSV", command=self.menu3_exportCSV_callBack)
        self.menu3.add_command(label="Format .txt", command=self.menu3_exportTxt_callBack)

        self.config(menu=self.menubar)

    def menu1_save_callBack(self):
    #Callback function for save config menu1 option
        print('save')

    def menu1_load_callBack(self):
    #Callback function for load config menu1 option
        print('load')

    def menu1_parameters_callBack(self):
    #Callback function for load config menu1 option
        print(self.parameters_view.frame.grid_size())
        self.parameters_view.frame.grid_forget()

    def menu2_Single_callBack(self):
    #Callback function for Single menu2 option
        print('Single')

    def menu2_Cycling_callBack(self):
    #Callback function for Cycling menu2 option
        print('Cycling')

    def menu2_Stability_callBack(self):
    #Callback function for Stability menu2 option
        print('Stability')

    def menu2_IV_callBack(self):
    #Callback function for I/V menu2 option
        print('IV')

    def menu2_Intermediate_callBack(self):
    #Callback function for Intermediate menu2 option
        print('Intermediate')

    def menu3_exportCSV_callBack(self):
    #Callback function for Format .CSV menu3 option
        print('bla')

    def menu3_exportTxt_callBack(self):
    #Callback function for Format .txt menu3 option
        print('bla')
        
    def __actualizeView(self):
    #This method permits to create/actualize the view parameters        
        self.configure(bg=self.bgColor)