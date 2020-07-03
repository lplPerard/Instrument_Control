"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for the application's view

"""
from Single import Single
from Cycling import Cycling
from IV import IV
from Modelling import Modelling
from Parameters import Parameters
from Stability import Stability

from Resources import Resource
from Controller import Controller

from tkinter import Tk   
from tkinter import Label
from tkinter import Menu 
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END

class View(Tk):
    """Class containing the GUI for the CBRAM software according to the MCV model.

    """

    def __init__(self):
    #Constructor for the View class
        """
            Constructor for the class View. The class inherits from Tk from GUI management.
            The following attributes are  created :

            - self.topLevel_param : Toplevel window used to display the parameters of the software. Hidden by default.
            - self.topLevel_term : Toplevel window used to display a terminal. Hidden by default
            - self.term_text : 



        """
        Tk.__init__(self)
        
        self.topLevel_param = Toplevel(self)
        self.topLevel_param.title("Parameters")
        self.topLevel_param.protocol('WM_DELETE_WINDOW', self.topLevel_param.withdraw)
        self.topLevel_param.withdraw()

        self.topLevel_term =Toplevel(self)
        self.topLevel_term.title("Terminal")
        self.topLevel_term.protocol('WM_DELETE_WINDOW', self.topLevel_term.withdraw)
        self.topLevel_term.transient()
        self.topLevel_term.withdraw()
        self.term_text = Text(self.topLevel_term, height=30, width=70, bg="black", fg="green")
        self.term_text.grid(column=0, row=0)
        self.term_text.insert(END, "You are running CBRAM software\n")

        self.resource = Resource()
        self.controller = Controller(self.resource)
        self.parameters = Parameters(self.topLevel_param, self.resource)
        self.parameters.frame.grid(column=0, row=0)

        self.sequence = Single(self, self.resource, self.term_text)
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
        self.menubar.add_cascade(label="Display", menu=self.menu1)
        self.menu1.add_command(label="Terminal", command=self.menu1_terminal_callBack)
        self.menu1.add_command(label="Parameters", command=self.menu1_parameters_callBack)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Sequence", menu=self.menu2)        
        self.menu2.add_command(label="Single", command=self.menu2_Single_callBack)
        self.menu2.add_command(label="Cycling", command=self.menu2_Cycling_callBack)     
        self.menu2.add_command(label="I/V Curve", command=self.menu2_IV_callBack)  
        self.menu2.add_command(label="Stability", command=self.menu2_Stability_callBack)
        self.menu2.add_command(label="Modelling", command=self.menu2_Modelling_callBack)        

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Results", menu=self.menu3)
        self.menu3.add_command(label="Export", command=self.menu3_export_callBack)
        self.menu3.add_command(label="Import", command=self.menu3_import_callBack)

        self.config(menu=self.menubar)

    def menu1_terminal_callBack(self):
    #Callback function for load config menu1 option
        if self.topLevel_term.state() == "withdrawn":
            self.topLevel_term.deiconify()

        elif self.topLevel_term.state() == "normal":
            self.topLevel_term.withdraw()

    def menu1_parameters_callBack(self):
    #Callback function for load config menu1 option
        if self.topLevel_param.state() == "withdrawn":
            self.topLevel_param.deiconify()

        elif self.topLevel_param.state() == "normal":
            self.topLevel_param.withdraw()

    def menu2_Single_callBack(self):
    #Callback function for Single menu2 option
        self.sequence.clearFrame()
        self.sequence = Single(self, self.resource, self.term_text)
        self.sequence.initFrame(text="Single Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_Cycling_callBack(self):
    #Callback function for Cycling menu2 option
        self.sequence.clearFrame()
        self.sequence = Cycling(self, self.resource, self.term_text)
        self.sequence.initFrame(text="Cycling Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_Stability_callBack(self):
    #Callback function for I/V menu2 option
        self.sequence.clearFrame()
        self.sequence = Stability(self, self.resource, self.term_text)
        self.sequence.initFrame(text="Stability Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_IV_callBack(self):
    #Callback function for I/V menu2 option
        self.sequence.clearFrame()
        self.sequence = IV(self, self.resource, self.term_text)
        self.sequence.initFrame(text="IV Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

    def menu2_Modelling_callBack(self):
    #Callback function for Modelling menu2 option
        self.sequence.clearFrame()
        self.sequence = Modelling(self, self.resource, self.term_text)
        self.sequence.initFrame(text="Modelling Sequence", column=0, row=0, rowspan=10, bg=self.resource.bgColor)

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
        elif state == 'STABILITY':
            self.menu2_Stability_callBack()

        self.sequence.results = results
        self.parameters.update(results)
        self.sequence.loadResults()
        
    def __actualizeView(self):
    #This method permits to create/actualize the view parameters        
        self.configure(bg=self.resource.bgColor)