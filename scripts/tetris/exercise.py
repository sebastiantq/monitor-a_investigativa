# Importamos las librerías requeridas para el script
import socket
import sys
import time
import argparse
import signal
import json
import pyautogui

"""Code modified from the example program to show how to read a multi-channel time series from UDP at https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/UDP/udp_receive.py."""

""" These variables can be changed if needed for changed controls on different Tetris websites. Refer to pyautogui documentation for
more information on what keywords map to specific keys. https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys """

MOVE_PIECE_LEFT = "left"
MOVE_PIECE_RIGHT = "right"
DROP_PIECE = "space"
ROTATE_PIECE = "up"

# Función para cerrar la conexión
def exit_print(signal, frame):
    print("Closing listener")
    sys.exit(0)

if __name__ == "__main__":
    # Recibimos los argumentos de la instrucción para ejecutar el script
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=12345, help="The port to listen on")
    parser.add_argument("--address", default="/openbci", help="address to listen to")
    parser.add_argument("--option", default="print", help="Debugger option")
    parser.add_argument("--len", default=8, help="Debugger option")
    args = parser.parse_args()

    # Asignamos los argumentos anteriormente recibidos
    length = args.len
    if args.option == "print":
        signal.signal(signal.SIGINT, exit_print)

    # Conectamos con el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (args.ip, args.port)
    sock.bind(server_address)

    # Imprimimos la información del socket
    print('--------------------')
    print("-- UDP LISTENER -- ")
    print('--------------------')
    print("IP:", args.ip)
    print("PORT:", args.port)
    print('--------------------')

    # Comenzamos a calibrar el dispositivo y a recibir mensajes
    print("Calibration period, remain neutral...")
    start = time.time()
    numSamples = 0
    duration = 10
    rotated = False
    space_pressed = False
    left_once = False
    right_once = False
    x_prev = 0
    z_prev = 0

    x_start_sum = 0
    x_start_samples = 0
    for y in range(150):
        data, addr = sock.recvfrom(20000) # Definimos un buffer de 20000 bytes
        obj = json.loads(data.decode())
        if obj.get('type') == 'accelerometer':
            aux_data = obj.get('data')
            x_start_sum += aux_data[0]
            x_start_samples += 1

    print("Calibration done. You may now begin Tetris!")

    x_start = x_start_sum / x_start_samples

    while True:
        data, addr = sock.recvfrom(20000) # Definimos de nuevo el buffer por cada iteración
        if args.option == "print":
            obj = json.loads(data.decode())
            if obj.get('type') == 'accelerometer':
                aux_data = obj.get('data')
                x = aux_data[0]
                z = aux_data[2]

                # Comenzamos a identificar los movimientos de la cabeza
                if 0.075 + x_start < x < 0.2 + x_start and not left_once: # Movimiento hacia la izquierda
                    pyautogui.press('left')
                    left_once = True
                elif -0.075 + x_start > x > -0.2 + x_start and not right_once: # Movimiento hacia la derecha
                    pyautogui.press('right')
                    right_once = True
                elif x > 0.2 + x_start and x_prev < x: # Movimiento hacia la izquierda
                    pyautogui.press('left')
                    left_once = False
                elif x < -0.2 + x_start and x_prev > x: # Movimiento hacia la derecha
                    pyautogui.press('right')
                    right_once = False
                elif -0.075 + x_start < x < 0.075 + x_start: # No hay movimiento
                    left_once = False
                    right_once = False

                x_prev = x
                z_prev = z

            numSamples += 1
