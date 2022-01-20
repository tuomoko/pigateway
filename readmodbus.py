#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Read data with Modbus RTU devices using a Modbus map from YAML file.

@author: Tuomo Kohtamäki
"""
import minimalmodbus
import yaml

# Set to true for debugging purposes
print_debug = True

class ReadModbus():
    """Client to communicate with Modbus devices."""

    def __init__(self, serialSettings, address, map_file):
        self.instrument = minimalmodbus.Instrument(serialSettings['port'], address)  # port name, device address (in decimal)
        if 'baudrate' in serialSettings:
            self.instrument.serial.baudrate = serialSettings['baudrate']
        if 'timeout' in serialSettings:
            self.instrument.serial.timeout = serialSettings['timeout']
        #TODO add other serial settings
        
        # Load the modbus map
        with open(map_file, "r") as f:
            self.registers = yaml.safe_load(f)['registers']
        
        return

    # Read all the registers from the map and return as dictionary
    def read_registers(self):
        data = dict()
        success = False
        retries = 0
        while success == False:
            try:
                for register in self.registers:
                    variable, value = self.__read_register(register)
                    data[variable] = value
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

    # Internal method to read a single register
    def __read_register(self, register):
        if register['type'] == 'uint':
            value = self.instrument.read_register(register['address'], register['decimals'])
        elif register['type'] == 'int':
            value = self.instrument.read_register(register['address'], register['decimals'], signed=True)
        elif register['type'] == 'long':
            value = self.instrument.read_long(register['address'])
        elif register['type'] == 'longint':
            value = self.instrument.read_long(register['address'], signed=True)
        elif register['type'] == 'float':
            value = self.instrument.read_float(register['address'])
        else:
            raise ValueError("Incorrect register type for " + str(register))
        
        if print_debug:
            print("Address " + str(register['address']) + ' (' +register['variable'] + ') = ' + str(value) + ' : ' + register['description'])
        return register['variable'], value

