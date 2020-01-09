"""This code contains the controlling commands for the CBRAM programming software

"""

import pyvisa
from numpy import linspace
from numpy import ones

def findInstruments():
    rm = pyvisa.ResourceManager()
    return(rm.list_resources())

def resistanceMeasurement(ident):

    voltage = 1
    current = 1e-6

    if ident == "":
        return(-1)
    else:
        rm = pyvisa.ResourceManager()
        my_instrument = rm.open_resource(ident)

        my_instrument.write('*RST')
        my_instrument.write('TRAC:CLE "defbuffer1"')

        my_instrument.write('SOUR:FUNC CURR')
        my_instrument.write('SOUR:CURR:VLIM ' + str(voltage))

        my_instrument.write('SENS:FUNC "VOLT"')
        my_instrument.write('SOUR:CURR ' + str(current))
        my_instrument.write('OUTP ON')

        my_instrument.write('MEAS:VOLT?')
        volt = float(my_instrument.read())

        my_instrument.write('MEAS:CURR?')
        amp = float(my_instrument.read())

        if amp != 0:
            R = volt/amp
        else:
            R = -1

        my_instrument.write('OUTP OFF')
        my_instrument.close()

        return(R)

def generateSingleVoltageWaveform(ident, Us, Ilim):
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource(ident)

    my_instrument.write('*RST')
    my_instrument.write('TRAC:CLE "defbuffer1"')

    my_instrument.write('SOUR:FUNC VOLT')
    my_instrument.write('SOUR:VOLT ' + str(0))
    my_instrument.write('SOUR:VOLT:ILIM ' + str(Ilim))
    my_instrument.write('SOUR:VOLT:READ:BACK OFF')

    my_instrument.write('SENS:FUNC "VOLT"')
    my_instrument.write('SENS:VOLT:AZER OFF')
    my_instrument.write('SENS:VOLT:NPLC 0.01')

    my_instrument.write('SENS:CURR:RANG ' + str(Ilim))
    my_instrument.write('SENS:CURR:AZER OFF')
    my_instrument.write('SENS:CURR:NPLC 0.01')
    my_instrument.write('OUTP ON')

    i = 0
    Um = 0*Us
    Im = 0*Us
    while i < len(Us):
        my_instrument.write('SOUR:VOLT ' + str(Us[i]))
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)

        my_instrument.write('MEAS:VOLT?')
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)
        Um[i] = float(my_instrument.read())

        my_instrument.write('MEAS:CURR?')
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)
        Im[i] = float(my_instrument.read())

        i+=1
    
    my_instrument.write('OUTP OFF')
    my_instrument.close()

    return(Um, Im)
    
def generateSingleCurrentWaveform(ident, Is, Vlim):  
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource(ident)

    my_instrument.write('*RST')
    my_instrument.write('TRAC:CLE "defbuffer1"')

    my_instrument.write('SOUR:FUNC VOLT')
    my_instrument.write('SOUR:VOLT ' + str(0))
    my_instrument.write('SOUR:VOLT:ILIM ' + str(Ilim))
    my_instrument.write('SOUR:VOLT:READ:BACK OFF')

    my_instrument.write('SENS:FUNC "VOLT"')
    my_instrument.write('SENS:VOLT:AZER OFF')
    my_instrument.write('SENS:VOLT:NPLC 0.01')

    my_instrument.write('SENS:CURR:RANG ' + str(Ilim))
    my_instrument.write('SENS:CURR:AZER OFF')
    my_instrument.write('SENS:CURR:NPLC 0.01')
    my_instrument.write('OUTP ON')

    i = 0
    Um = 0*Us
    Im = 0*Us
    while i < len(Us):
        my_instrument.write('SOUR:VOLT ' + str(Us[i]))
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)

        my_instrument.write('MEAS:VOLT?')
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)
        Um[i] = float(my_instrument.read())

        my_instrument.write('MEAS:CURR?')
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)
        Im[i] = float(my_instrument.read())

        i+=1
    
    my_instrument.write('OUTP OFF')
    my_instrument.close()

    return(Um, Im)

def generateCyclingVoltageWaveform(ident, signal1, lim1, signal2, lim2):
    iteration = 0
    j = 0
    Rm = []
    Um = []
    Im = []
    nbTry = 0

    R = resistanceMeasurement(ident)
    if R > 1e4:
        state = "HIGH"
    else:
        state = "LOW"

    while nbTry < 5:
        iteration+=1
        j+=1

        if state == "HIGH":
            [U, I] = generateSingleVoltageWaveform(ident, signal1, lim1)
            Um.append(U)
            Im.append(I)
            Rm.append(resistanceMeasurement(ident))

            if R > 100:
                nbTry += 1
                iteration -=1
                state = "HIGH"

            else:
                state = "LOW"
                nbTry = 0

        elif state == "LOW":
            [U, I] = generateSingleVoltageWaveform(ident, signal2, lim2)            
            Um.append(U)
            Im.append(I)
            Rm.append(resistanceMeasurement(ident))

            if R < 1e4:
                nbTry += 1
                iteration-=1
                state = "LOW"

            else:
                state = "HIGH"
                nbTry = 0
                

    return(iteration, Rm, Um, Im)
        
def generateCyclingCurrentWaveform(ident, signal1, lim1, signal2, lim2):
    iteration = 0
    j = 0
    R = ones(1)
    Um = ones(1)
    Im = ones(1)
    nbTry = 0

    R = resistanceMeasurement(ident)
    if R > 1e4:
        state = "HIGH"
    else:
        state = "LOW"

    while nbTry < 5:
        iteration+=1
        j+=1

        if state == "HIGH":
            [U, I] = generateSingleVoltageWaveform(ident, signal1, lim1)
            Um[j] = U
            Im[j] = I
            R[j] = resistanceMeasurement(ident)

            if R > 100:
                nbTry += 1
                iteration -=1
                state = "HIGH"

            else:
                state = "LOW"
                nbTry = 0

        elif state == "LOW":
            [U, I] = generateSingleVoltageWaveform(ident, signal2, lim2)            
            Um[j] = U
            Im[j] = I
            R[j] = resistanceMeasurement(ident)

            if R < 1e4:
                nbTry += 1
                iteration-=1
                state = "LOW"

            else:
                state = "HIGH"
                nbTry = 0
                

    return(iteration, R, Um, Im)

def generateStabilityVoltageWaveform(ident, signal1, lim1, signal2, lim2, cycles):
    nbTry = 0
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource(ident)

    my_instrument.write('*RST')
    my_instrument.write('TRAC:CLE "defbuffer1"')

    my_instrument.close()

def generateStabilityCurrentWaveform(ident, signal1, lim1, signal2, lim2, cycles):
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource(ident)

    my_instrument.write('*RST')
    my_instrument.write('TRAC:CLE "defbuffer1"')

    my_instrument.close()
