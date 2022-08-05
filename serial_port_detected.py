#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
__file__ = serial_port_detected.py
__author__ = rotoapanta "Roberto Toapanta"
__copyright__ = "Copyright 2021, BitTech"
__credits__ = ["Roberto Toapanta, Giovanny Toapanta"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Roberto Toapanta"
__email__ = "robertocarlos.toapanta@gmail.com"
__status__ = "Production"
__fecha__ = 4/2/22 22:25
__description__ = "Puertos seriales conectados y selección del puerto Prolific"
__information__ : https://qastack.mx/programming/12090503/listing-available-com-ports-with-python
"""

import serial.tools.list_ports


def serial_port_detected():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    #print("Connected COM ports: " + str(connected))
    #print(connected[5])
    return connected[5]


serial_port_detected()
