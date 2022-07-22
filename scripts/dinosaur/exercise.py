# Importamos las librerías requeridas para el script
import argparse
import time
import numpy as np
import collections
import pyautogui
import pandas as pd
import matplotlib.pyplot as plt

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions

def main():
    parser = argparse.ArgumentParser()

    # Configuramos los parámetros para conectar con la Cyton Board
    parser.add_argument('--timeout', type = int, help  = 'timeout for device discovery or connection', required = False, default = 0)
    parser.add_argument('--ip-port', type = int, help  = 'ip port', required = False, default = 0)
    parser.add_argument('--ip-protocol', type = int, help  = 'ip protocol, check IpProtocolType enum', required = False, default = 0)
    parser.add_argument('--ip-address', type = str, help  = 'ip address', required = False, default = '')
    parser.add_argument('--serial-port', type = str, help  = 'serial port', required = False, default = '')
    parser.add_argument('--mac-address', type = str, help  = 'mac address', required = False, default = '')
    parser.add_argument('--other-info', type = str, help  = 'other info', required = False, default = '')
    parser.add_argument('--streamer-params', type = str, help  = 'streamer params', required = False, default = '')
    parser.add_argument('--serial-number', type = str, help  = 'serial number', required = False, default = '')
    parser.add_argument('--board-id', type = int, help  = 'board id, check docs to get a list of supported boards', required = True)
    parser.add_argument('--log', action = 'store_true')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout

    # Se inicializan las variables y se realiza la calibración
    time_thres = 100
    sampling_rate = BoardShim.get_sampling_rate(args.board_id)
    window = sampling_rate*5 # 5 second window
    flex_thres = 0.8

    # Configuraciones necesarias para la placa
    if (args.log):
        BoardShim.enable_dev_board_logger()
    else:
        BoardShim.disable_board_logger()

    board = BoardShim(args.board_id, params)
    board.prepare_session()

    if args.board_id == brainflow.board_shim.BoardIds.CYTON_BOARD.value:
        board.config_board('x1060000X')

    board.start_stream(45000, args.streamer_params)
    time.sleep(10) # Delay para estabilizar la conexión

    # A partir de aqui se puede jugar

    print("Start!")
    prev_time = int(round(time.time() * 1000))

    while True:
        data = board.get_current_board_data(window) # Obtenemos la información de la placa
        DataFilter.perform_rolling_filter (data[1], 2, AggOperations.MEAN.value) # Eliminamos el ruido de la señal
        maximum = max(data[1])
        minimum = min(data[1])
        norm_data = (data[1,(window-(int)(sampling_rate/2)):(window-1)] - minimum) / (maximum - minimum) # Normalizamos la señal recibida

        if((int(round(time.time() * 1000)) - time_thres) > prev_time): # Validamos que haya pasado cierto tiempo desde la última flexión
            prev_time = int(round(time.time() * 1000)) # Actualizamos el tiempo de la última flexión
            for element in norm_data:
                if(element >= flex_thres):
                    pyautogui.click()
                    break

    board.stop_stream()
    board.release_session()

if __name__ == "__main__":
    main()
