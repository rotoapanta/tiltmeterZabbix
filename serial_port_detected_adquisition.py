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
    """
    Detect serial port
    :return: serial port connected
    """
    com_list = serial.tools.list_ports.comports()
    connected = []
    for element in com_list:
        connected.append(element.device)
    # print("Connected COM ports: " + str(connected))
    # print(connected[5])
    return connected[5]


def main():
    serial_port_connected = serial_port_detected()  # Puerto de lectura o escritura.
    BAUD_RATE = 9600  # Velocidad de transmisión
    HOST = "CAYA_FW_1"
    serial_port = serial.Serial(serial_port_connected,
                                BAUD_RATE,
                                timeout=1.0)  # Abrir el puerto serial, se establece un tiempo de espera de 1 seg
    print("Conectado a: " + serial_port.portstr)

    while True:
        try:
            raw_data = serial_port.readline()  # leer una línea terminada '\n'
            # print(raw_data)
            if not raw_data:
                print("Desconectado Interfaz Serial")
                continue  # si quiere acabar el proceso poner break
            values = str(raw_data[0:len(raw_data)].decode("utf-8"))
            list_values = values.split(',')
            axis_x_data = (list_values[0])
            axis_y_data = (list_values[1])
            temperature_data = (list_values[2])
            serial_number = (list_values[3])
            print(axis_x_data[1:])  # 1er dato eje X
            print(axis_y_data)  # 2do dato eje Y
            print(temperature_data)  # 3er dato temperatura
            print(serial_number)  # 4to dato numero serial
        except KeyboardInterrupt:
            print("Comunicación Serial Interrumpida")
            break
    serial_port.close()  # cierre el puerto inmediatamente.


# print(serial_port_detected.__doc__)
# help(serial_port_detected)
main()
