"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Class container for Service.

"""
import pyvisa

import numpy as np

class Service():
    """Class containing the Service for the CBRAM software

    """

    def __init__(self, resource):
    #Constructor for the Model class
        self.resource = resource

        self.resourceManager = pyvisa.ResourceManager()
        self.findInstruments()

    def findInstruments(self):
    #This method actualize le list of instruments connected to the computer
        self.instrList = self.resourceManager.list_resources()

    def measureResistance(self):
    #This method measure the resistance using a 2 wire resistance measurement set-up. It shouldn't be used to precisely measure low-resistance states

        voltage = 2.1
        current = 10e-6

        self.instr = self.resourceManager.open_resource(self.resource.deviceAdress)

        self.instr.write('*RST')
        self.instr.write('TRAC:CLE "defbuffer1"')

        self.instr.write('SOUR:FUNC CURR')
        self.instr.write('SOUR:CURR:VLIM ' + str(voltage))
        self.instr.write('SOUR:VOLT:READ:BACK ON')

        self.instr.write('SENS:FUNC "VOLT"')
        self.instr.write('SENS:VOLT:AZER ON')
        self.instr.write('SENS:VOLT:NPLC 0.01')

        self.instr.write('SOUR:CURR ' + str(current))
        self.instr.write('OUTP ON')

        self.instr.write('MEAS:CURR?')
        curr = float(self.instr.read())

        self.instr.write('MEAS:VOLT?')
        volt = float(self.instr.read())

        if curr != 0:
            R = volt/curr
        else:
            R = -1

        self.instr.write('OUTP OFF')
        self.instr.close()

        return(R)

    def generateSingleVoltageWaveform(self, Us, Ilim):
    #This method generates a voltage waveform according to given parameter Us
        self.instr = self.resourceManager.open_resource(self.resource.deviceAdress)

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

        return(Um.tolist(), Im.tolist())

    def generateCyclingVoltageWaveform(self, signal1, lim1, signal2, lim2):
        iteration = 1
        nbTry = 1
        nbTry_return = [1]
        Rm = []
        Um = []
        Im = []

        R = self.measureResistance()
        if R > self.resource.R_high_lim:
            state = "HIGH"
        else:
            state = "LOW"

        while nbTry <= self.resource.nbTry:
            print(state)

            if state == "HIGH":
                [U, I] = self.generateSingleVoltageWaveform(signal1, lim1)
                Um.append(U)
                Im.append(I)
                R = self.measureResistance()
                Rm.append(R)

                if R > self.resource.R_low_lim:
                    state = "HIGH"
                    nbTry += 1
                    nbTry_return.append(nbTry)

                else:
                    state = "LOW"
                    nbTry = 1
                    nbTry_return.append(nbTry)

            elif state == "LOW":
                [U, I] = self.generateSingleVoltageWaveform(signal2, lim2)            
                Um.append(U)
                Im.append(I)
                R = self.measureResistance()
                Rm.append(R)

                if R < self.resource.R_high_lim:
                    state = "LOW"
                    nbTry += 1
                    nbTry_return.append(nbTry)

                else:
                    state = "HIGH"
                    nbTry = 1
                    nbTry_return.append(nbTry)
                    
            iteration+=1
            print(R)

        return(iteration, nbTry_return[:-1], Rm, Um, Im)