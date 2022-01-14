#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Upload measurement data to the cloud.

@author: Tuomo Kohtamäki
"""
from myinflux import MyInfluxClient
import config

# Create a client
influx = MyInfluxClient(url=config.influxSettings['url'], crt=config.influxSettings['crt'], key=config.influxSettings['key'])

# TODO create this from measured data
data = dict()
data['P1'] = 100

# The tag is used to separate different devices
tag = dict()
tag['device'] = config.generalSettings['device']

# Add the data
influx.add_measurement(config.influxSettings['database'], config.influxSettings['measurement'], data, tag)
