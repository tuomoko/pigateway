#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Read data from ORNO OR-WE-504 single phase energy meter.

@author: Tuomo Kohtamäki
"""
import minimalmodbus

# Set to true for debugging purposes
print_debug = True

class MeterORNO504():
    """Client to communicate with energy meter."""

    def __init__(self, port, address):
        self.instrument = minimalmodbus.Instrument(port, address)  # port name, device address (in decimal)
        self.instrument.serial.baudrate = 9600 # Default for ORNO meter
        self.instrument.serial.timeout = 0.5 # Longer timeout needed
        return

    def read_registers(self):
        data = dict()
        success = False
        retries = 0
        while success == False:
            try:
                data['U1'] = self.instrument.read_register(0, 1)  # Registernumber, number of decimals
                data['I1'] = self.instrument.read_register(1, 1)
                data['f'] = self.instrument.read_register(2, 1)
                data['P1'] = self.instrument.read_register(3, 0)
                data['Q1'] = self.instrument.read_register(4, 0)
                data['S1'] = self.instrument.read_register(5, 0)
                data['PF1'] = self.instrument.read_register(6, 3)
                data['E1'] = self.instrument.read_long(7)
                if print_debug:
                    print('Voltage: ' + str(data['U1']) + ' V')
                    print('Current: ' + str(data['I1']) + ' A')
                    print('Frequency: ' + str(data['f']) + ' Hz')
                    print('Active Power: ' + str(data['P1']) + ' W')
                    print('Reactive Power: ' + str(data['Q1']) + ' VAr')
                    print('Apparent Power: ' + str(data['S1']) + ' VA')
                    print('PF: ' + str(data['PF1']))
                    print('Active energy: ' + str(data['E1']) + ' Wh')
                success = True
            except IOError:
                if print_debug:
                    print("Failed to read from instrument")
                retries += 1
                if (retries >= 3):
                    if print_debug:
                        print("3 consecutive reads failed. Giving up.")
                    break
        return data

