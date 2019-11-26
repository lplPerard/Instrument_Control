"""This code contains the view for the CBRAM cell programming software

"""

from tkinter import Tk #Import Tkinter library
from tkinter import Label 
from tkinter import Menu
from tkinter import Button
from tkinter import LabelFrame

from tkinter.ttk import Combobox

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def callbackFunc(event):
    print("New element selected")

#Window
main_window = Tk() #Generates the main window for the UI
main_window.title("CBRAM cells programmer")
main_window.configure(background="gainsboro")
main_window.resizable(True, True)

#Barre de menu
menubar = Menu(main_window)

menu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=menu1)
menu1.add_command(label="Save config")
menu1.add_command(label="Load config")
menu1.add_separator()
menu1.add_command(label="Quit", command=quit)


menu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Export", menu=menu2)
menu2.add_command(label="Format .CSV")
menu2.add_command(label="Format .txt")

menu3 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Calibrate", menu=menu3)
menu3.add_command(label="Perform new Calibration")
menu3.add_command(label="Reset Calibration")

main_window.config(menu=menubar)

#LabelFrame
labelframe1 = LabelFrame(main_window, text="General Configuration", padx=25, pady=15, bg="gainsboro")
labelframe1.grid(column=0, columnspan=2, row=0)

labelframe2 = LabelFrame(main_window, text="Signal Configuration", padx=25, pady=15, bg="gainsboro")
labelframe2.grid(column=0, columnspan=2, row=1)

#Labels
label1 = Label(main_window, text="Copyright Grenoble-inp LCIS") #Create a display section
label1.grid(column=2, row=3)   #Attach the display section to the main window
label1.configure(bg="gainsboro")

#Listes déroulantes
liste1 = Combobox(labelframe1, state="readonly", width=60, values=["ligne1", "ligne2", "ligne3"])
liste1.grid(column=0, row=0)
liste1.configure(background="gainsboro")
liste1.bind("<<ComboboxSelected>>", callbackFunc)

liste2 = Combobox(labelframe1, state="readonly", width=60, values=["SET cell in HIGH state", "SET cell in LOW state"])
liste2.grid(column=0, row=1)
liste2.configure(background="gainsboro")

liste3 = Combobox(labelframe1, state="readonly", width=60, values=["Voltage source", "Current Source"])
liste3.grid(column=0, row=2)
liste3.configure(background="gainsboro")

if liste2.current() == 1 :
    liste4 = Combobox(labelframe2, state="readonly", width=60, values=["ligne1", "ligne2", "ligne3"])
    liste4.grid(column=0, row=0)
    liste4.configure(background="gainsboro")

    liste5 = Combobox(labelframe2, state="readonly", width=60, values=["SET cell in HIGH state", "SET cell in LOW state"])
    liste5.grid(column=0, row=1)
    liste5.configure(background="gainsboro")

    liste6 = Combobox(labelframe2, state="readonly", width=60, values=["Voltage source", "Current Source"])
    liste6.grid(column=0, row=2)
    liste6.configure(background="gainsboro")

#Boutons
button1 = Button(main_window, text="Generate Command Script", padx=15, command=callbackFunc)
button1.grid(column=0, row=2)
button1.configure(bg="gainsboro")

button2 = Button(main_window, text="Start Sequence", padx=15, command=main_window.quit)
button2.grid(column=1, row=2)
button2.configure(bg="gainsboro")

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

graph = FigureCanvasTkAgg(fig, master=main_window)
canva2 = graph.get_tk_widget()
canva2.grid(column=2, row=0, rowspan=3)
canva2.configure(bg="gainsboro")

main_window.mainloop() #The main window can only be closed by manual action