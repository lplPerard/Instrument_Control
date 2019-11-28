"""This code contains the controlling commands for the CBRAM programming software

"""

from pyvisa import ResourceManager

class Instrument(ResourceManager):

    def __init__(self):
        ResourceManager.__init__(self)


    def initInstrument(self):
    #Create a ResourceManager object linked to the selected instrument
        self.open_resource("") #Open the selected instrument and create a handler
        self.list_resources() #Returns all visa ressources connected. Linked to combobox1.
        #print(instrument.query("*IDN?"))

    def searchInstruments(self):
    #Search for compatible instruments
        print("bla")

    def generateScript(self):
    #Generate from View.py arguments
        print("bla")
        
