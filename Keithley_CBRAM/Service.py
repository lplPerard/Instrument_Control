"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Service.

"""
import pyvisa

from Resource import Resource

import numpy as np

class Service(Resource):
    """Class containing the Service for the CBRAM software

    """

    def __init__(self):
    #Constructor for the Model class
        Resource.__init__(self)

        self.resourceManager = pyvisa.ResourceManager()
        self.findInstruments()
        self.instr = ""

    def findInstruments(self):
    #This method actualize le list of instruments connected to the computer
        self.instrList = self.resourceManager.list_resources()

    def generateSingleVoltageWaveform(self, Us, Ilim):
    #This method generates a voltage waveform according to given parameter Us
        print(self.deviceAdress)
        self.instr = self.resourceManager.open_resource(self.deviceAdress)

        self.instr.write('*RST')
        self.instr.write('TRAC:CLE "defbuffer1"')

        self.instr.write('SOUR:FUNC VOLT')
        self.instr.write('SOUR:VOLT ' + str(0))
        self.instr.write('SOUR:VOLT:ILIM ' + str(Ilim))
        self.instr.write('SOUR:VOLT:READ:BACK OFF')

        self.instr.write('SENS:FUNC "VOLT"')
        self.instr.write('SENS:VOLT:AZER OFF')
        self.instr.write('SENS:VOLT:NPLC 0.01')

        self.instr.write('SENS:CURR:RANG ' + str(Ilim))
        self.instr.write('SENS:CURR:AZER OFF')
        self.instr.write('SENS:CURR:NPLC 0.01')
        self.instr.write('OUTP ON')

        i = 0
        Um = 0*Us
        Im = 0*Us
        while i < len(Us):
            self.instr.write('SOUR:VOLT ' + str(Us[i]))
            self.instr.flush(mask=pyvisa.constants.VI_WRITE_BUF)

            self.instr.write('MEAS:VOLT?')
            self.instr.flush(mask=pyvisa.constants.VI_WRITE_BUF)
            Um[i] = float(self.instr.read())

            self.instr.write('MEAS:CURR?')
            self.instr.flush(mask=pyvisa.constants.VI_WRITE_BUF)
            Im[i] = float(self.instr.read())

            i+=1
        
        self.instr.write('OUTP OFF')
        self.instr.close()

        return(Um, Im)