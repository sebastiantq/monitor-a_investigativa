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
prev_time = 0 # Tiempo en que se realizó la última flexión
flex_thres = 1.0 # Umbral de flexión

while True:
	sample, timestamp = inlet.pull_sample() # Obtenemos la data EMG

	curr_time = int(round(time.time() * 1000)) # Obtenemos el tiempo actual en milisegundos

	if (((sample[1] >= flex_thres) or (sample[0] >= flex_thres))): # Verificamos si se detecto algun pico en uno de los brazos
		prev_time = int(round(time.time() * 1000)) # Atualizamos el tiempo de la última flexión

		if(sample[1] > sample[0]): # Scroll hacia arriba o abajo dependiendo de la intesidad de las señales
			pyautogui.scroll(50)
		else:
			pyautogui.scroll(-50)
