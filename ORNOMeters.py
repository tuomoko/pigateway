#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Read data from ORNO energy meters through Modbus RTU.

@author: Tuomo Kohtamäki
"""
import minimalmodbus

# Set to true for debugging purposes
print_debug = True

class MeterORNO504():
    """Client to communicate with ORNO OR-WE-504 single phase energy meter."""

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


class MeterORNO516():
    """Client to communicate with ORNO OR-WE-516 three phase energy meter."""

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
                data['U1'] = self.instrument.read_float(0x000E)
                data['U2'] = self.instrument.read_float(0x0010)
                data['U3'] = self.instrument.read_float(0x0012)
                data['f'] = self.instrument.read_float(0x0014)
                data['I1'] = self.instrument.read_float(0x0016)
                data['I2'] = self.instrument.read_float(0x0018)
                data['I3'] = self.instrument.read_float(0x001A)
                data['P'] = self.instrument.read_float(0x001C)
                data['P1'] = self.instrument.read_float(0x001E)
                data['P2'] = self.instrument.read_float(0x0020)
                data['P3'] = self.instrument.read_float(0x0022)
                data['Q'] = self.instrument.read_float(0x0024)
                data['Q1'] = self.instrument.read_float(0x0026)
                data['Q2'] = self.instrument.read_float(0x0028)
                data['Q3'] = self.instrument.read_float(0x002A)
                data['S'] = self.instrument.read_float(0x002C)
                data['S1'] = self.instrument.read_float(0x002E)
                data['S2'] = self.instrument.read_float(0x0030)
                data['S3'] = self.instrument.read_float(0x0032)
                data['PF'] = self.instrument.read_float(0x0034)
                data['PF1'] = self.instrument.read_float(0x0036)
                data['PF2'] = self.instrument.read_float(0x0038)
                data['PF3'] = self.instrument.read_float(0x003A)
                data['E'] = self.instrument.read_float(0x0100)
                data['E1'] = self.instrument.read_float(0x0102)
                data['E2'] = self.instrument.read_float(0x0104)
                data['E3'] = self.instrument.read_float(0x0106)
                
                if print_debug:
                    print('Voltage L1 / L2 / L3: ' + str(data['U1']) + ' / ' + str(data['U2']) + ' / ' + str(data['U3']) + ' V')
                    print('Current L1 / L2 / L3: ' + str(data['I1']) + ' / ' + str(data['I2']) + ' / ' + str(data['I3']) + ' A')
                    print('Frequency: ' + str(data['f']) + ' Hz')
                    print('Active Power L1 / L2 / L3 / Total: ' + str(data['P1']) + ' / ' + str(data['P2']) + ' / ' + str(data['P3']) + ' / ' + str(data['P']) + ' W')
                    print('Reactive Power L1 / L2 / L3 / Total: ' + str(data['Q1']) + ' / ' + str(data['Q2']) + ' / ' + str(data['Q3']) + ' / ' + str(data['Q']) + ' VAr')
                    print('Apparent Power L1 / L2 / L3 / Total: ' + str(data['S1']) + ' / ' + str(data['S2']) + ' / ' + str(data['S3']) + ' / ' + str(data['S']) + ' VA')
                    print('PF L1 / L2 / L3 / Total: ' + str(data['PF1']) + ' / ' + str(data['PF2']) + ' / ' + str(data['PF3']) + ' / ' + str(data['PF']))
                    print('Active energy L1 / L2 / L3 / Total: ' + str(data['E1']) + ' / ' + str(data['E2']) + ' / ' + str(data['E3']) + ' / ' + str(data['E']) + ' Wh')
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

