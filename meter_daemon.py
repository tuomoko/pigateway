#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Upload measurement data to the cloud every 10 seconds.

@author: Tuomo Kohtamäki
"""
from myinflux import MyInfluxClient
from readmodbus import ReadModbus
import config
from timeloop import Timeloop
from datetime import timedelta

# Create an Influx client
influx = MyInfluxClient(url=config.influxSettings['url'], crt=config.influxSettings['crt'], key=config.influxSettings['key'])

# Create modbus readers for each device defined in the config.py
devices = dict()
for device in config.deviceSettings:
    devices[device['tag']] = ReadModbus(config.serialSettings,device['address'],device['map_file'])

tl = Timeloop()
@tl.job(interval=timedelta(seconds=10))
def sample_data_10s():
    # Measure all devices and store to database separately
    for device_tag, device in devices.items():
        # Read the data
        data = device.read_registers()
        tag = dict()
        tag['device'] = device_tag
        # Add the data to the database
        if data:
            influx.add_measurement(config.influxSettings['database'], config.influxSettings['measurement'], data, device_tag)

if __name__ == "__main__":
    tl.start(block=True)