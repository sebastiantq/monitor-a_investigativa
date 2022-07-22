"""Code modified from the example program to show how to read a multi-channel time series from LSL at
https://github.com/OpenBCI/OpenBCI_GUI/blob/master/Networking-Test-Kit/LSL/lslStreamTest.py."""

# Importamos las librerías requeridas para el script
from pylsl import StreamInlet, resolve_stream
import pyautogui
import time

# Se encuentra el stream EMG y se le notifica al usuario
print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

# Inicializamos las variables
time_thres = 2000 # Tiempo entre contracciones musculares
prev_time = 0 # Tiempo de la última contracción
blink_thres = 0.95 # Umbral para detectar un pico

while True:
	sample, timestamp = inlet.pull_sample() # Obtenemos la data EMG

	curr_time = int(round(time.time() * 1000)) # Obtenemos el tiempo actual en milisegundos

	if(curr_time - time_thres > prev_time): # Verificamos que haya pasado el tiempo requerido entre contracciones
		if (sample[0] >= blink_thres): # Continuamos solo si la contracción supera el umbral
			prev_time = int(round(time.time() * 1000)) # Actualizamos el tiempo de la última contracción
			pyautogui.press('space')
