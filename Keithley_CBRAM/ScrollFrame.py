"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for a Scrollable Frame. This widget is used to encapsulate the Parameter_view.


"""
from Resource import Resource

import tkinter as tk
from tkinter import LabelFrame
from tkinter import Canvas
from tkinter import Frame
from tkinter import Label

class ScrollFrame(Parameters):

    def __init__(self, root):
    #Constructor for the ScrollFrame class.
        Resource.__init__(self)

        self.frame = LabelFrame(root)        
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)        
        self.canva = tk.Canvas(self.frame, yscrollcommand=self.scrollbar.set)
        self.lateral = Frame(self.canva)
        self.lateralFrame = self.canva.create_window(0, 0, anchor=tk.NW, window=self.lateral)

    def initFrame(self, name):
    #This method is called to create/actualize the frame
        self.scrollbar.configure(activebackground="grey", bg="white")

        self.frame.configure(text=name, bg=self.bgColor)
        self.lateral.configure(bg=self.bgColor)
        self.canva.configure(bg=self.bgColor)

        self.scrollbar.config(command=self.canva.yview)
        self.scrollbar.pack(side='right')
        self.canva.pack()

    def grid(self, column=0, row=0, columnspan=1, rowspan=1):
    #This method creates a grid method for the ScrollFrame class
        self.frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

    def update(self):
    #This method is used to update the view of the scrolable frame
        self.canva.update()