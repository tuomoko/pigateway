#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Upload measurement data to the cloud every 10 seconds.

@author: Tuomo Kohtamäki
"""
from myinflux import MyInfluxClient
from MeterORNO504 import MeterORNO504
import config
import time
from timeloop import Timeloop
from datetime import timedelta

# Create an Influx client
influx = MyInfluxClient(url=config.influxSettings['url'], crt=config.influxSettings['crt'], key=config.influxSettings['key'])

# Create the energy meter client
meter = MeterORNO504(config.serialSettings['port'],config.serialSettings['address'])

# The tag is used to separate different devices
tag = dict()
tag['device'] = config.generalSettings['device']

tl = Timeloop()
@tl.job(interval=timedelta(seconds=10))
def sample_data_10s():
    # Read the data
    data = meter.read_registers()
    # Add the data to the database
    influx.add_measurement(config.influxSettings['database'], config.influxSettings['measurement'], data, tag)

if __name__ == "__main__":
    tl.start(block=True)