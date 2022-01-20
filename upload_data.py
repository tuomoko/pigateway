#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Upload single measurement data to the cloud.

@author: Tuomo Kohtamäki
"""
from myinflux import MyInfluxClient
from ORNOMeters import MeterORNO504
import config

# Create an Influx client
influx = MyInfluxClient(url=config.influxSettings['url'], crt=config.influxSettings['crt'], key=config.influxSettings['key'])

# Create the energy meter client
meter = MeterORNO504(config.serialSettings['port'],config.serialSettings['address'])

# Read the data
data = meter.read_registers()

# The tag is used to separate different devices
tag = dict()
tag['device'] = config.generalSettings['device']

# Add the data to the database
if data:
    influx.add_measurement(config.influxSettings['database'], config.influxSettings['measurement'], data, tag)

