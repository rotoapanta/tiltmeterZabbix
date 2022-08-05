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
import configparser
from pyzabbix import ZabbixMetric, ZabbixSender
import logging
import os
import sys


def connect2zabbix(zx_ip, zx_port):
    """
    Try to connect to a ZX server, return
    """
    try:
        return ZabbixSender(zx_ip, zx_port)
    except Exception as e:
        raise ("Error in connect2zabbix: %s" % str(e))


def read_parameters(file_path):
    """
    Read a configuration text file
    :param file_path: path to configuration text file
    :return: dict: dict of a parser object
    """
    parameter_file = check_file(file_path)
    config = configparser.ConfigParser()
    config.read(parameter_file)  # Leer el archivo de configuración
    return config._sections


def check_file(file_path):
    """
    Check if the file exists

    :param file_path: path to file to check
    :return: file_path
    :raises Exception e: General exception if file doesn't exist.
    """
    try:
        with open(file_path):
            return file_path
    except Exception as e:
        logging.error("Error in check_file(%s). Error: %s " % (file_path, str(e)))
        raise Exception("Error in check_file(%s). Error: %s " % (file_path, str(e)))


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


def get_data_acquisition():
    serial_port_connected = serial_port_detected()  # Puerto de lectura o escritura.
    BAUD_RATE = 9600  # Velocidad de transmisión
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
            return list_values

        except KeyboardInterrupt:
            print("Comunicación Serial Interrumpida")
            break
    serial_port.close()  # cierre el puerto inmediatamente.


def send2Zabbix(zx_server, x):
    """
    Receive soh_data array and send it to a ZX trigger item only  if ping ok
    """
    print(x)
    axis_x = x[0]
    try:
        hostname = "CAYA_FW_1"
        metrics = [
            ZabbixMetric(hostname, 'axis.x.data', axis_x[1:]),
            ZabbixMetric(hostname, 'axis.y.data', x[1]),
            ZabbixMetric(hostname, 'temperature.data', x[2]),
            ZabbixMetric(hostname, 'serial.number.data', x[3])
        ]
        try:
            res = zx_server.send(metrics)
            logging.info("%s, %s" % (hostname, res))
        except Exception as e:
            logging.info("Error in send2Zabbix. Error was: %s" % str(e))

    except Exception as e:
        logging.info("Not station in dictionary: %s" % str(e))


# print(serial_port_detected.__doc__)
# help(serial_port_detected)
def main():
    exec_dir = os.path.realpath(os.path.dirname(__file__))
    logging.basicConfig(
        format='%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
        level=logging.INFO,  # Nivel de los eventos que se registran en el logger
        filename=os.path.join(exec_dir, "inclino_logs_info3.log"),  # Fichero en el que se escriben los logs
        filemode="a"  # a ("append"), en cada escritura, si el archivo de logs ya existe,
        # se abre y añaden nuevas lineas.
    )
    is_error = False

    if len(sys.argv) == 1:
        is_error = True
    else:
        try:
            run_param = read_parameters(sys.argv[1])
        except Exception as e:
            logging.error("Error reading configuration file: %s" % str(e))
            raise Exception("Error reading configuration file: %s" % str(e))

        try:
            zabbix_server = run_param['ZABBIX_INFO']['ip']
            zabbix_port = run_param['ZABBIX_INFO']['port']
        except Exception as e:
            logging.error("Error getting parameters: %s" % str(e))
            raise Exception("Error getting parameters: %s" % str(e))

        try:
            zx_server = connect2zabbix(zabbix_server, int(zabbix_port))

            x = get_data_acquisition()
            for n in range(3, len(x)):
                send2Zabbix(zx_server, x)

        except Exception as e:
            logging.error("Error in main(): %s " % str(e))

        if is_error:
            logging.info(f'Usage: python {sys.argv[0]} configuration_file.txt ')
            print(f'Usage: python {sys.argv[0]} CONFIGURATION_FILE.txt ')


if __name__ == '__main__':
    main()
