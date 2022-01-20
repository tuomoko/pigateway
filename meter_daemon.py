#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Upload measurement data to the cloud every 10 seconds.

@author: Tuomo Kohtamäki
"""
from myinflux import MyInfluxClient
from ORNOMeters import MeterORNO504, MeterORNO516
import config
from timeloop import Timeloop
from datetime import timedelta

# Create an Influx client
influx = MyInfluxClient(url=config.influxSettings['url'], crt=config.influxSettings['crt'], key=config.influxSettings['key'])

# Create the energy meter client
if config.generalSettings['meter_type'] == 'OR-WE-504':
    meter = MeterORNO504(config.serialSettings['port'],config.serialSettings['address'])
elif config.generalSettings['meter_type'] == 'OR-WE-516':
    meter = MeterORNO516(config.serialSettings['port'],config.serialSettings['address'])
else:
    raise ValueError('Unknown power meter type')

# The tag is used to separate different devices
tag = dict()
tag['device'] = config.generalSettings['device']

tl = Timeloop()
@tl.job(interval=timedelta(seconds=10))
def sample_data_10s():
    # Read the data
    data = meter.read_registers()
    # Add the data to the database
    if data:
        influx.add_measurement(config.influxSettings['database'], config.influxSettings['measurement'], data, tag)

if __name__ == "__main__":
    tl.start(block=True)