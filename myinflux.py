#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Client to communicate with an Influx database.

Original python influxdb client could not be used since it did not support:
 - custom paths in the server (e.g. https://domain.com/influxdb)
 - SSL keys for client authentication

@author: Tuomo Kohtamäki
"""
import requests
import urllib.parse


class MyInfluxClient():
    """Client to communicate with Influx database."""

    def __init__(self, url, crt, key):
        """Build client object."""
        # TODO check if cert and key exists
        self.url = url
        self.certpath = crt
        self.keypath = key

    def get_path(self, subpath):
        """Get the path to the method."""
        return urllib.parse.urljoin(self.url, subpath)

    def ping(self):
        """Send a ping request."""
        request_url = self.get_path('ping')
        ret = requests.get(request_url, cert=(self.certpath, self.keypath))
        return ret.status_code == 204

    def create_db(self, dbname):
        """Create a database."""
        request_url = self.get_path('query')
        ret = requests.post(request_url, data={'q': 'CREATE DATABASE '+dbname}, cert=(
            self.certpath, self.keypath))
        return ret.status_code == 200

    def add_measurement(self, dbname, measurement, data, tags=None, timestamp=None):
        """Add a row to the database."""
        # Construct the url and necessary GET arguments
        request_url = self.get_path('write') + '?db=' + dbname
        # Construct the POST data query:
        # "measurement,tag1=tagvalue1 data1=value1,data2=value2 timestamp"
        dataline = measurement + "," +\
            ",".join(["=".join([key, str(val)]) for key, val in tags.items()]) + " "
        dataline += ",".join(["=".join([key, str(val)]) for key, val in data.items()])
        if timestamp is not None:
            dataline += " " + str(timestamp)
        # print dataline
        ret = requests.post(request_url, data=dataline,
                            cert=(self.certpath, self.keypath),
                            headers={'Content-Type': 'application/octet-stream'})
        return ret.status_code == 204
