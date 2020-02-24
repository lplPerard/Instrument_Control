"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for the application's view

"""
from Sequence.Single import Single
from Sequence.Cycling import Cycling
from Sequence.IV import IV
from Parameters import Parameters

from Resources import Resource
from Controller import Controller

from tkinter import Tk   
from tkinter import Label
from tkinter import Menu 

class View(Tk):
    """Class containing the GUI for the CBRAM software according to the MCV model.

    """

    def __init__(self):
    #Constructor for the View class
        Tk.__init__(self)

        self.resource = Resource()
        self.controller = Controller(self.resource)
        
        self.parameters = Parameters(self, self.resource)
        self.parameters.frame.grid(column=1, row=0)

        self.sequence = Single(self, self.resource)
        self.sequence.initFrame(text="Single Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

        self.__initWidgets()
        self.__actualizeView()

    def __initWidgets(self):
    #This method is used to encapsulate the creation of sequences and menues
        self.__initMenu()

        self.copyright = Label(self, text="Copyright grenoble-inp LCIS", bg=self.resource.bgColor)
        self.copyright.grid(column=0, row=11)

    def __initMenu(self):
    #This method generates a Menu bar which give access to the diffent software's tools
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Configuration", menu=self.menu1)
        self.menu1.add_command(label="Save", command=self.menu1_save_callBack)
        self.menu1.add_command(label="Load", command=self.menu1_load_callBack)
        self.menu1.add_command(label="Parameters", command=self.menu1_parameters_callBack)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sequence", menu=self.menu2)        
        self.menu2.add_command(label="Single", command=self.menu2_Single_callBack)
        self.menu2.add_command(label="Cycling", command=self.menu2_Cycling_callBack)     
        self.menu2.add_command(label="I/V Curve", command=self.menu2_IV_callBack)
        self.menu2.add_command(label="Intermediate Value", command=self.menu2_Intermediate_callBack)        

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Results", menu=self.menu3)
        self.menu3.add_command(label="Export", command=self.menu3_export_callBack)
        self.menu3.add_command(label="Import", command=self.menu3_import_callBack)

        self.config(menu=self.menubar)

    def menu1_save_callBack(self):
    #Callback function for save config menu1 option
        print('save')

    def menu1_load_callBack(self):
    #Callback function for load config menu1 option
        print('load')

    def menu1_parameters_callBack(self):
    #Callback function for load config menu1 option
        if self.parameters.show == True:
            self.parameters.frame.grid_forget()
            self.parameters.show = False

        elif self.parameters.show == False:
            self.parameters.frame.grid(column=1, row=0)
            self.parameters.show = True

    def menu2_Single_callBack(self):
    #Callback function for Single menu2 option
        self.sequence.clearFrame()
        self.sequence = Single(self, self.resource)
        self.sequence.initFrame(text="Single Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_Cycling_callBack(self):
    #Callback function for Cycling menu2 option
        self.sequence.clearFrame()
        self.sequence = Cycling(self, self.resource)
        self.sequence.initFrame(text="Cycling Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_IV_callBack(self):
    #Callback function for I/V menu2 option
        self.sequence.clearFrame()
        self.sequence = IV(self, self.resource)
        self.sequence.initFrame(text="IV Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_Intermediate_callBack(self):
    #Callback function for Intermediate menu2 option
        print('Intermediate')

    def menu3_export_callBack(self):
    #Callback function for Format .CSV menu3 option
        self.controller.serialize(self.sequence.results)

    def menu3_import_callBack(self):
    #Callback function for Format .txt menu3 option
        [state, results] = self.controller.load()

        if state == 'SINGLE':
            self.menu2_Single_callBack()
        elif state == 'CYCLING':
            self.menu2_Cycling_callBack()
        elif state == 'IV':
            self.menu2_IV_callBack()

        self.sequence.results = results
        self.parameters.update(results)
        self.sequence.loadResults()
        
    def __actualizeView(self):
    #This method permits to create/actualize the view parameters        
        self.configure(bg=self.resource.bgColor)