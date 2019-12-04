"""This code contains the controlling commands for the CBRAM programming software

"""

import pyvisa

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

def generateVoltageWaveform(ident):
    print('bla')

def generateCurrentWaveform(ident):
    print('bla')

#'USB0::0x05E6::0x2450::04100639::INSTR'