"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for Service.

"""
import pyvisa

import numpy as np

from tkinter import Toplevel
from tkinter import Label
from tkinter import END

class Service():
    """Class containing the Service for the CBRAM software

    """

    def __init__(self, frame, resource):
    #Constructor for the Model class
        self.frame = frame
        self.resource = resource
        self.instrList = ["null"]

        try:
            self.resourceManager = pyvisa.ResourceManager()
            self.findInstruments()

        except:
            pass

    def findInstruments(self):
    #This method actualize le list of instruments connected to the computer
        try:
            self.instrList = self.resourceManager.list_resources()
        except:
            self.instrList = []

    def measureResistance(self, output, negative = False):
    #This method measure the resistance using a 4 wire resistance measurement set-up.
        error = 0
        self.instr = self.resourceManager.open_resource(self.resource.deviceAdress)

        self.instr.write('*RST')
        self.instr.write('TRAC:CLE "defbuffer1"')

        self.instr.write('SENS:FUNC "VOLT"')
        self.instr.write('SENS:VOLT:RSEN ON')
        
        self.instr.write('SENS:CURR:RSEN ON')
        self.instr.write('SENS:CURR:AZER ON')
        
        self.instr.write('SOUR:FUNC CURR')

        if negative == True:
            self.instr.write('SOUR:CURR ' + str(-1e-3))   
            output.insert(END, "Negative Resistance Measurement...\n")
            output.see(END)
            output.update_idletasks()
        else:
            self.instr.write('SOUR:CURR ' + str(1e-3)) 
            output.insert(END, "Positive Resistance Measurement...\n")
            output.see(END)
            output.update_idletasks()

        self.instr.write('SOUR:CURR:VLIM ' + str(2))     
        self.instr.write('SOUR:CURR:READ:BACK ON')
        
        self.instr.write('OUTP ON')
        
        self.instr.write('MEAS:CURR?')
        Im = float(self.instr.read())

        self.instr.write('MEAS:VOLT?')
        Um = float(self.instr.read())

        R = Um/Im

        if abs(R) > 1e20 :
            error = 1

        self.instr.write('OUTP OFF')
        self.instr.close()
        
        output.insert(END, "Measured Resistance is : " + str(abs(R)) + " Ohm\n\n")
        output.see(END)
        output.update_idletasks()

        return(abs(R), error)

    def generateSingleVoltageWaveform(self, output, Us, Ilim1, Ilim2=-1, index_Ilim2=-1):
    #This method generates a voltage waveform according to given parameter Us, using a 4 wire method

        self.instr = self.resourceManager.open_resource(self.resource.deviceAdress)

        if max(Us) > 0:            
            output.insert(END, "Positive Waveform is generated...\n")
            output.see(END)
            output.update_idletasks()

        else:      
            output.insert(END, "Negative Waveform is generated...\n")
            output.see(END)
            output.update_idletasks()


        self.instr.write('*RST')
        self.instr.write('TRAC:CLE "defbuffer1"')

        self.instr.write('SOUR:FUNC VOLT')
        self.instr.write('SOUR:VOLT ' + str(0))
        self.instr.write('SOUR:VOLT:ILIM ' + str(Ilim1))
        self.instr.write('SOUR:VOLT:READ:BACK ON')

        self.instr.write('SENS:FUNC "VOLT"')
        #self.instr.write('SENS:VOLT:RSEN ON')
        self.instr.write('SENS:VOLT:AZER OFF')
        self.instr.write('SENS:VOLT:NPLC 0.01')

        self.instr.write('SENS:CURR:RANG ' + str(Ilim1))
        #self.instr.write('SENS:CURR:RSEN ON')
        self.instr.write('SENS:CURR:AZER OFF')
        self.instr.write('SENS:CURR:NPLC 0.01')
        
        self.instr.write('OUTP ON')

        i = 0
        Um = 0*Us
        Im = 0*Us
        error = 0
        while i < len(Us):

            if i == index_Ilim2:                
                self.instr.write('SOUR:VOLT:ILIM ' + str(Ilim2))
                self.instr.write('SENS:CURR:RANG ' + str(Ilim2))

            self.instr.write('SOUR:VOLT ' + str(Us[i]))

            self.instr.write('MEAS:CURR?')
            Im[i] = float(self.instr.read())

            if abs(Im[i]) > 1e10:
                error = 1

            self.instr.write('MEAS:VOLT?')
            Um[i] = float(self.instr.read())

            if abs(Um[i]) > 1e10:
                error = 1

            i+=1
        
        self.instr.write('OUTP OFF')
        self.instr.close()

        output.insert(END, "DONE\n")
        output.see(END)
        output.update_idletasks()

        return(Um.tolist(), Im.tolist(), error)

    def generateCyclingVoltageWaveform(self, output, signal1, lim1, signal2, lim2):
        
        output.insert(END, "Starting a new CYCLING sequence\n")
        output.see(END)
        output.update_idletasks()
        
        cycles = 0
        iteration = 1
        nbTry = 1
        nbTry_return = [1]
        Rm = []
        Um = []
        Im = []

        [R, error] = self.measureResistance(output)
        if R > self.resource.R_high_lim:
            state = "HIGH"
            state_tpm = "HIGH"
        else:
            state = "LOW"
            state_tpm = "LOW"

        while nbTry <= self.resource.nbTry:
            if state_tpm != state:
                state_tpm = state
                cycles += 1

            output.insert(END, "Current State : " + state + " \n")
            output.insert(END, "Cycles : " + str(cycles) + " \n")
            output.insert(END, "iteration : " + str(nbTry) + "/" + str(self.resource.nbTry) + "\n")
            output.see(END)
            output.update_idletasks()

            if state == "HIGH":
                if (nbTry % 5) == 0:
                    output.insert(END, "Trying to Reset Cell\n")
                    output.see(END)
                    [U, I, error] = self.generateSingleVoltageWaveform(output, signal2, lim2/10)            
                    Um.append(U)
                    Im.append(I)
                    [R, error] = self.measureResistance(output, negative=True)
                    Rm.append(R)

                else:
                    [U, I, error] = self.generateSingleVoltageWaveform(output, signal1, lim1)
                    Um.append(U)
                    Im.append(I)
                    [R, error] = self.measureResistance(output)
                    Rm.append(R)

                if error != 0:                    
                     return(iteration, cycles, Rm, Um, Im, error)

                if R > self.resource.R_low_lim:
                    state = "HIGH"
                    nbTry += 1
                    nbTry_return.append(nbTry)

                else:
                    state = "LOW"
                    nbTry = 1
                    nbTry_return.append(nbTry)

            elif state == "LOW":
                [U, I, error] = self.generateSingleVoltageWaveform(output, signal2, lim2 + ((nbTry%5))*lim2/3)            
                Um.append(U)
                Im.append(I)
                [R, error] = self.measureResistance(output, negative=True)
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

        return(iteration, cycles, Rm, Um, Im, error)

    def simulateVoltageWaveform(self, signal, lim, lim2, CBRAM):
    #This method simulate the behavior of a CBRAM cell based on parameters extracted from CBRAM param, upon the signal voltage.
        Ea = 0.5
        k = 1.3e-23
        q = 1.6e-19

        T = 0*signal
        dh = 0
        h = 0
        r = 0
        dr = 0
        R = 0*signal
        I = 0*signal
        state = "off"

        Rmax = CBRAM.resistivity_off * CBRAM.nafion_th / (np.pi * (CBRAM.ext_radius)**2)

        R[0] = Rmax


        i=1
        j=0
        problem = 0

        while (i < len(signal)) and j < 100:
            T[i] = CBRAM.temperature + signal[i]**2 * CBRAM.thermal_resistance / R[i-1]
            E = signal[i] * CBRAM.resistivity_off * (CBRAM.nafion_th - h) / (CBRAM.resistivity_on * h  + CBRAM.resistivity_off  * (CBRAM.nafion_th - h))
            
            if E == 0:
                E = signal[i]
            
            if state == 'off' :
            
                dh = CBRAM.velocity_h * np.exp(-Ea*q / (k*T[i])) * np.sinh(CBRAM.alpha * q * E / (2*k*T[i]))
                h = h + dh * self.resource.stepDelay
                
                if signal[i] < 0:

                    if (R[i-1] > 0.8*Rmax) & ((signal[i] - signal[i-1]) < 0):
                        dh = -1*CBRAM.velocity_r * np.exp(-Ea*q / (k*T[i])) *  np.sinh(4*CBRAM.beta*q*signal[i]/(k*T[i]))


                    else:                
                        dh = CBRAM.velocity_r * np.exp(-Ea*q / (k*T[i])) *  np.sinh(2*CBRAM.beta*q*signal[i]/(k*T[i]))
                        
                    h = h + dh * self.resource.stepDelay

                if h >= CBRAM.nafion_th:
                    h = CBRAM.nafion_th      
                    state = 'on'

                elif h <= 0 : 
                    h = 0
                
                R[i] = abs(CBRAM.resistivity_on * h / (np.pi * ((CBRAM.CF_radius+r)**2)) + CBRAM.resistivity_off * (CBRAM.nafion_th - h) / (np.pi * (CBRAM.ext_radius**2)))
                I[i] = signal[i]/R[i]

                if signal[i] >= 0:

                    if abs(I[i]) > lim:
                        signal[i] = np.sign(signal[i]) * R[i] * lim/1.01
                        i = i-1
                        j = j+1

                    else:
                        j = 0

                else :

                    if abs(I[i]) > lim2:
                        signal[i] = np.sign(signal[i]) * R[i] * lim2/1.01
                        i = i-1
                        j = j+1

                    else:
                        j = 0

            elif state == 'on':
            
                dr = CBRAM.velocity_r * np.exp(-Ea*q/(k*T[i])) * np.sinh(CBRAM.beta*q*signal[i]/(k*T[i]))
                r = r + dr * self.resource.stepDelay   

                if CBRAM.CF_radius + r <= CBRAM.CF_radius: 
                    r = 0                
                    state = 'off'       

                if r > 6*CBRAM.CF_radius: 
                    r = 6*CBRAM.CF_radius

                R[i] = abs(CBRAM.resistivity_on * h / (np.pi * ((CBRAM.CF_radius+r)**2)) + CBRAM.resistivity_off * (CBRAM.nafion_th - h) / (np.pi * (CBRAM.ext_radius**2)))
                I[i] = signal[i]/R[i]
                
                if signal[i] >= 0:

                    if abs(I[i]) > lim:
                        signal[i] = np.sign(signal[i]) * R[i] * lim/1.01
                        i = i-1
                        j = j+1

                    else:
                        j = 0

                else :

                    if abs(I[i]) > lim2:
                        signal[i] = np.sign(signal[i]) * R[i] * lim2/1.01
                        i = i-1
                        j = j+1

                    else:
                        j = 0
            
            i = i+1

        if j == 100:
            problem = 1
        else:
            problem = 0

        return(signal, I, R, h, dh, r, dr, T, problem)