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

	if (sample[0] >= flex_thres): # Verificamos si hay un pico en el brazo
		if(curr_time - 500 > prev_time): # Verificamos que haya un delay entre flexiones para que funcione correctamente
			if(curr_time - 1000 > prev_time): # Scroll hacia arriba o hacia abajo dependiendo de si se hacen o no flexiones seguidas
				print("Arriba")
				pyautogui.scroll(500)
			else:
				print("Abajo")
				pyautogui.scroll(-1000) # El desplazamiento hacia abajo debe de ser el doble del que se hace hacia arriba,
										# dado que primero subirá y luego bajará, si fuese igual quedaría en el mismo lugar

			prev_time = int(round(time.time() * 1000)) # Actualizamos el tiempo de la última flexión
