"""This code contains the view for the CBRAM cell programming software

"""

from tkinter import Tk #Import Tkinter library
from tkinter import Label 
from tkinter import Menu
from tkinter import Button
from tkinter import Canvas

from tkinter.ttk import Combobox

import numpy as np

from matplotlib.figure import Figure
#from matplotlib.backends import tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Window
main_window = Tk() #Generates the main window for the UI
main_window.title("CBRAM cells programmer")
main_window.configure(background="gainsboro")

#Labels
label1 = Label(main_window, text="Hello World") #Create a display section
label1.grid(column=1, row=1)   #Attach the display section to the main window
label1.configure(bg="gainsboro")

label2 = Label(main_window, text="Hello World") #Create a display section
label2.grid(column=3, row=1)   #Attach the display section to the main window
label2.configure(bg="gainsboro")

label3 = Label(main_window, text="Hello World") #Create a display section
label3.grid(column=3, row=2)   #Attach the display section to the main window
label3.configure(bg="gainsboro")

#Listes déroulantes
liste1 = Combobox(main_window, values=["ligne1", "ligne2", "ligne3"])
liste1.grid(column=1, row=3)
liste1.configure(background="gainsboro")

#Barre de menu
menubar = Menu(main_window)

menu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=menu1)
menu1.add_command(label="Save config")
menu1.add_command(label="Load config")
menu1.add_separator()
menu1.add_command(label="Quit")


menu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Export", menu=menu2)
menu2.add_command(label="Format .CSV")
menu2.add_command(label="Format .txt")

main_window.config(menu=menubar)

#Boutons
button1 = Button(main_window, text="Quit", command=main_window.quit)
button1.grid(column=2, row=5)
button1.configure(bg="gainsboro")

#Canvas
canva1 = Canvas(main_window, width=300, height=200)
canva1.grid(column=2, row=8)
canva1.configure(bg="gainsboro")

#Figures to Canvas
x = np.linspace(0, 2 * np.pi, 50)
y = np.sin(x)
fig = Figure(figsize=(6,4))
ax = fig.add_subplot(111)
ax.plot(x,y)

graph = FigureCanvasTkAgg(fig, master=main_window)
canva2 = graph.get_tk_widget()
canva2.grid(column=2, row=9)
canva2.configure(bg="gainsboro")

main_window.mainloop() #The main window can only be closed by manual action
