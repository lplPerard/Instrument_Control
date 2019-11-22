"""This code contains the view for the CBRAM cell programming software"""

from tkinter import * #Import Tkinter library

main_window = Tk() #Generates the main window for the UI

label1 = Label(main_window, text="Hello World") #Create a display section
label1.grid()   #Attach the display section to the main window

main_window.mainloop() #The main window can only be closed by manual action
