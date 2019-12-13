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
    current = 0.0001

    if ident == "":
        return(-1)
    else:
        rm = pyvisa.ResourceManager()
        my_instrument = rm.open_resource(ident)

        my_instrument.write('*RST')
        my_instrument.write('TRAC:CLE "defbuffer1"')

        my_instrument.write('SOUR:FUNC VOLT')
        my_instrument.write('SOUR:VOLT:ILIM ' + str(current))

        my_instrument.write('SENS:FUNC "CURR"')
        my_instrument.write('SOUR:VOLT ' + str(voltage))
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

def generateVoltageWaveform(ident, Us, Ilim):
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource(ident)

    my_instrument.write('*RST')
    my_instrument.write('TRAC:CLE "defbuffer1"')

    my_instrument.write('SOUR:FUNC VOLT')
    my_instrument.write('SOUR:VOLT ' + str(0))
    my_instrument.write('SOUR:VOLT:ILIM ' + str(Ilim))
    my_instrument.write('SOUR:VOLT:READ:BACK ON')

    my_instrument.write('SENS:FUNC "CURR"')
    my_instrument.write('SENS:CURR:RANG:AUTO ON')
    my_instrument.write('SENS:CURR:AZER OFF')
    my_instrument.write('OUTP ON')

    i = 0
    Um = 0*Us
    Im = 0*Us
    while i < len(Us):
        my_instrument.write('SOUR:VOLT ' + str(Us[i]))
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)

        my_instrument.write('MEAS:CURR?')
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)
        Im[i] = float(my_instrument.read())

        my_instrument.write('MEAS:VOLT?')
        my_instrument.flush(mask=pyvisa.constants.VI_WRITE_BUF)
        Um[i] = float(my_instrument.read())

        i+=1
    
    my_instrument.write('OUTP OFF')
    
def generateCurrentWaveform(ident, Is, Vlim):
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource(ident)

    my_instrument.write('*RST')
    my_instrument.write('TRAC:CLE "defbuffer1"')

    my_instrument.write('SOUR:FUNC CURR')
    my_instrument.write('SOUR:CURR:ILIM ' + str(Vlim))
    my_instrument.write('SOUR:CURR:READ:BACK ON')

    my_instrument.write('SENS:FUNC "VOLT"')
    my_instrument.write('SENS:VOLT:RANG:AUTO ON')
    my_instrument.write('SENS:VOLT:AZER OFF')
    my_instrument.write('OUTP ON')

    i = 0
    Um = 0*Us
    Im = 0*Us
    while i < len(Us):
        my_instrument.write('SOUR:CURR ' + str(Is[i]))
        my_instrument.write(':TRAC:TRIG')
        '''my_instrument.write('MEAS:CURR?')
        my_instrument.write('MEAS:VOLT?')'''
        i+=1
    
    result = float(my_instrument.read())
    print(result)
    my_instrument.write('OUTP OFF')
