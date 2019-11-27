"""This code contains the controlling commands for the CBRAM programming software

"""

from pyvisa import ResourceManager

rm = ResourceManager()
rm.list_resources() #Returns all visa ressources connected. Linked to combobox1.

#instrument = rm.open_resource("") #Open the selected instrument and create a handler
#print(instrument.query("*IDN?"))
