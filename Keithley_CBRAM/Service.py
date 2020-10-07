"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD

File description : Class container for Service.

"""
import pyvisa
import time

import numpy as np

from tkinter import Toplevel
from tkinter import Label
from tkinter import END

class Service():
    """Class containing the Service for the CBRAM software. The goal of service is to manage the connection and communication with external device.

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

    def measureResistance(self, output, current = 1e-3, v_lim = 2, negative = False):
    #This method measure the resistance using a 4 wire resistance measurement set-up.
        error = 0
        self.instr = self.resourceManager.open_resource(self.resource.SMUAdress)

        self.instr.write('*RST')
        self.instr.write('*CLS')
        self.instr.write('TRAC:CLE "defbuffer1"')

        self.instr.write('SENS:FUNC "VOLT"')
        self.instr.write('SENS:VOLT:RSEN ON')
        
        self.instr.write('SENS:CURR:RSEN ON')
        self.instr.write('SENS:CURR:AZER ON')
        
        self.instr.write('SOUR:FUNC CURR')

        if negative == True:
            self.instr.write('SOUR:CURR ' + str(-1*current))   
            output.insert(END, "Negative Resistance Measurement...\n")
            output.see(END)
            output.update_idletasks()
        else:
            self.instr.write('SOUR:CURR ' + str(current)) 
            output.insert(END, "Positive Resistance Measurement...\n")
            output.see(END)
            output.update_idletasks()

        self.instr.write('SOUR:CURR:VLIM ' + str(v_lim))     
        self.instr.write('SOUR:CURR:READ:BACK ON')
        
        self.instr.write('OUTP ON')
        
        self.instr.write('MEAS:CURR?')
        Im = float(self.instr.read())

        self.instr.write('MEAS:VOLT?')
        Um = float(self.instr.read())

        R = Um/Im

        if abs(R) > 1e20 :
            error = 1

        if abs(R) < 1e-10 :
            error = 1

        self.instr.write('OUTP OFF')
        self.instr.close()
        
        output.insert(END, "Measured Resistance is : " + str(abs(R)) + " Ohm\n\n")
        output.see(END)
        output.update_idletasks()

        return(abs(R), error)

    def measureImpedance(self, output, voltage = 2, frequency = 1e2, func1 = "Cp", func2="Rp"):
    #This method measure the resistance using a 4 wire resistance measurement set-up.  
        output.insert(END, "RLC Impedance Measurement...\n")
        output.see(END)
        output.update_idletasks()

        error = 0

        self.instr = self.resourceManager.open_resource(self.resource.RLCAdress)

        self.instr.write('*RST')
        self.instr.write('*CLS')
        self.instr.write(':MEM:CLE')
        self.instr.write(':FORM REAL')
        self.instr.write(':TRIG:SOUR BUS')
        self.instr.write(':FUNC:IMP ' + str(func1) + str(func2))
        
        self.instr.write(':VOLT ' + str(voltage))
        self.instr.write(':FREQ ' + str(frequency))

        self.instr.write(':TRIG:IMM')
        Z = self.instr.query_binary_values(':FETCH:IMP:FORM?')[:3]
        #Z = self.instr.read()

        self.instr.close()
        
        output.insert(END, "Measured Impedance is : " + str(Z) + "\n")
        output.see(END)
        output.update_idletasks()

        return(Z, error)
        
    def generateSingleVoltageWaveform(self, output, Us, Ilim1, Ilim2=-1, index_Ilim2=-1):
    #This method generates a voltage waveform according to given parameter Us, using a 4 wire method

        self.instr = self.resourceManager.open_resource(self.resource.SMUAdress)

        if max(Us) > 0:            
            output.insert(END, "Positive Waveform is generated...\n")
            output.see(END)
            output.update_idletasks()

        else:      
            output.insert(END, "Negative Waveform is generated...\n")
            output.see(END)
            output.update_idletasks()


        self.instr.write('*RST')
        self.instr.write('*CLS')
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

    def measureStability(self, output, delay, negative = False):
    #This method is used to automatically measure resistance at different time interval, using the measureResitance method.
        output.insert(END, "Starting a Stability measurement\n\n")
        output.see(END)
        output.update_idletasks()

        delay = np.asarray(delay)

        i = 0
        R = 0*delay
        error = 0*delay

        while i < len(delay) - 1:

            output.insert(END, "Current advancement : " + str((i+1)*100/len(delay)) + " %\n")
            output.see(END)
            output.update_idletasks()

            [R[i], error[i]] = self.measureResistance(output, negative=negative)
            time.sleep(delay[i+1] - delay[i])

            i = i+1

        output.insert(END, "Current advancement : " + str((i+1)*100/len(delay)) + " %\n")
        output.see(END)
        output.update_idletasks()

        [R[i], error[i]] = self.measureResistance(output, negative=negative)

        return(R.tolist(), error)

    def generateCyclingVoltageWaveform(self, output, signal1, lim1, signal2, lim2, R_low_lim, R_high_lim, nbTry_max):
        
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
        if R > R_high_lim:
            state = "HIGH"
            state_tpm = "HIGH"
        else:
            state = "LOW"
            state_tpm = "LOW"

        while nbTry <= nbTry_max:
            if state_tpm != state:
                state_tpm = state
                cycles += 1

            output.insert(END, "Current State : " + state + " \n")
            output.insert(END, "Cycles : " + str(cycles) + " \n")
            output.insert(END, "iteration : " + str(nbTry) + "/" + str(nbTry_max) + "\n")
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

                if R > R_low_lim:
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

                if R < R_high_lim:
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


        """
            A method to simulate the behaviour of a CBRAM cell and compare it to importe I/V result test

            Parameters
            ----------

            signal : double vector
                Voltage command signal that would be applied to the real cell

            lim : double
                Current compliance for positive part of the signal

            lim2 : double
                Current compliance for the negative part of the signal

            CBRAM : CBRAM
                CBRAM object that describes the simulated cell's caracteristics

    """

        Ea = 0.5                #Activation energy
        k = 1.3e-23             #Boltzmann
        q = 1.6e-19             #Charge energy
        eps0 = 8.85418782e-12   #Void permittivity
        epsR = 3                #Nafion's permittivity

        dh = 0          #Filament's length growth rate
        h = 0           #Filament's current length
        r = 0           #Filament's current radius
        dr = 0          #Filament's radial growth rate
        
        T = 0*signal    #Temperature vector initialized to zero
        R = 0*signal    #Resistance vector initialized to zero
        I = 0*signal    #Current vector initialized to zero
        IPF = 0         #Poole-Frenkel current initialized to zero
        F = 0
        state = "off"   #Current state initialized to off

        tampon = signal

        Rmax = CBRAM.resistivity_off_ohm * CBRAM.nafion_th / (np.pi * (CBRAM.ext_radius)**2)    #Maximum resistance calculation based on cell's caracteristics (Pristine State)

        R[0] = Rmax #First resistance point initialized to maximum resistance (Pristine State)


        i=1     #To calculate iterations on the signal
        j=0     #To calculate iterations on current limiting process, work as a watchdog
        done=False
        problem = 0

        while (i < len(signal)) and j < 100:
            T[i] = CBRAM.temperature + signal[i]**2 * CBRAM.thermal_resistance / R[i-1] #Temperature calculation
            
            if (signal[i] < CBRAM.negative_offset_threshold) and (tampon[i] -  tampon[i-1] > 0) and (done == False):  #A threshold is added to YU's model to fit our results in LRS to HRS part
                signal[i:] = signal[i:] + CBRAM.negative_offset
                done=True
            
            
            E = signal[i] * CBRAM.resistivity_off_ohm * (CBRAM.nafion_th - h) / (CBRAM.resistivity_on * h  + CBRAM.resistivity_off_ohm  * (CBRAM.nafion_th - h))    #Electric field calculation based upon signal
 
            if E == 0:
                E = signal[i]  #To avoid E always equals 0 since h is initialized to zero
            
            if state == 'off' :
            
                dh = CBRAM.velocity_h * np.exp(-Ea*q / (k*T[i])) * np.sinh(CBRAM.alpha * q * E / (2*k*T[i])) #dh calculation based upon Mott-Gurney's law
                h = h + dh * self.resource.stepDelay #h calculation as integration of dh

                if h >= CBRAM.nafion_th :
                    h = CBRAM.nafion_th     #Maximum filament length limited to electrolyte thickness      
                    state = 'on'            #State is on because filament is touching

                elif h <= 0 : 
                    h = 0       #Minimum filament length limited to zero
                
                R[i] = abs(CBRAM.resistivity_on * h / (np.pi * ((CBRAM.CF_radius+r)**2)) + CBRAM.resistivity_off_ohm * (CBRAM.nafion_th - h) / (np.pi * (CBRAM.ext_radius**2))) #Resistance calculation based upon cell's geometry using Ohmic conductivity

                if signal[i] < 0:                    
                    R[i] = abs(CBRAM.resistivity_on * h / (np.pi * ((CBRAM.CF_radius+r)**2)) + CBRAM.resistivity_off_PF * (CBRAM.nafion_th - h) / (np.pi * (CBRAM.ext_radius**2)))  #Resistance calculation based upon cell's geometry using Poole-Frenkel conductivity


                I[i] = signal[i]/R[i] #Current calculation based upon signal and calculated resistance

                if (signal[i] < 0) and (tampon[i] -  tampon[i-1] > 0):
                    F = E/(CBRAM.nafion_th - h)
                    IPF = (np.pi * ((CBRAM.CF_radius+r)**2))*CBRAM.sigmaPF*F*np.exp(-1./k/T[i]*(CBRAM.phiPF*q-(q**3/np.pi/eps0/epsR*abs(F))**0.5))
                    print(IPF)
                    I[i] = IPF
                    R[i] = signal[i]/I[i]

                ### The following section aimsa calculate the applied voltage signal according to current compliance. The signal is recalculated as the product of current compliance and calculated resistance.
                ### After recalculation, i is decremented and the iteration is recalculated based upon the new voltage.

                if signal[i] >= 0:

                    if abs(I[i]) > lim:
                        signal[i] = np.sign(signal[i]) * R[i] * lim/1.01    #1% overshoot is tolerated (the simulation fails otherwise in most cases)
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

            elif state == 'on':     #When reaching on state, we consider radial growth of the filament
            
                dr = CBRAM.velocity_r * np.exp(-Ea*q/(k*T[i])) * np.sinh(CBRAM.beta*q*signal[i]/(k*T[i]))   #dr calculation based upon Mott-Gurney's law
                r = r + dr * self.resource.stepDelay   #r calculation as integration of dr

                if CBRAM.CF_radius + r <= CBRAM.CF_radius:  #if the radius becomes thinner than the original radius, we go back to off state
                    r = 0                
                    state = 'off' 

                if r > 3*CBRAM.CF_radius: #Maximum radius size limitation. Arbitrary factor
                    r = 3*CBRAM.CF_radius

                R[i] = abs(CBRAM.resistivity_on * h / (np.pi * ((CBRAM.CF_radius+r)**2)) + CBRAM.resistivity_off_ohm * (CBRAM.nafion_th - h) / (np.pi * (CBRAM.ext_radius**2))) #Resistance calculation based upon cell's geometry using Ohmic conductivity

                if signal[i] < 0:                    
                    R[i] = abs(CBRAM.resistivity_on * h / (np.pi * ((CBRAM.CF_radius+r)**2)) + CBRAM.resistivity_off_PF * (CBRAM.nafion_th - h) / (np.pi * (CBRAM.ext_radius**2)))  #Resistance calculation based upon cell's geometry using Poole-Frenkel conductivity
                    
                I[i] = signal[i]/R[i]   #Current calculation
                
                ### The following section aims at calculate the applied voltage signal according to current compliance. The signal is recalculated as the product of current compliance and calculated resistance.
                ### After recalculation, i is decremented and the iteration is recalculated based upon the new voltage.

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
            problem = 1     #Cannot solve current limitation, add error to results
        else:
            problem = 0     #Current limitation solved, no problem

        return(signal, I, R, h, dh, r, dr, T, problem)
        
    def sendEmailNotification(self, tosend):
    #This method sends an automatic email with results information after a sequence was terminated

        Fromadd = "research.notification.lcis@gmail.com"
        Toadd = "luc.perard@lcis.grenoble-inp.fr"    ##  Spécification des destinataires

        message = MIMEMultipart()    ## Création de l'objet "message"
        message['From'] = Fromadd    ## Spécification de l'expéditeur
        message['To'] = Toadd    ## Attache du destinataire à l'objet "message"
        message['Subject'] = "A Cycling test was terminated !"    ## Spécification de l'objet de votre mail

        msg = tosend   ## Message à envoyer
        message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))    ## Attache du message à l'objet "message", et encodage en UTF-8
        
        serveur = smtplib.SMTP('smtp.gmail.com', 587)    ## Connexion au serveur sortant (en précisant son nom et son port)
        serveur.starttls()    ## Spécification de la sécurisation
        serveur.login(Fromadd, "13octobre1996")    ## Authentification
        texte= message.as_string().encode('utf-8')    ## Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
        serveur.sendmail(Fromadd, Toadd, texte)    ## Envoi du mail
        serveur.quit()    ## Déconnexion du serveur