'''
MIT License

Copyright (c) [2023] [Fong Morales Eduardo, Galán Galván Arturo David, Martínez Paredes Eric]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pyudev								#Gestión y control de dispositivos USB
import tkinter								#Generaración de  GUI
from tkinter import *				
import os 									#Funciones de sistema
from time import sleep
import subprocess 							#Generación de subprocesos
import shutil  								#Manejo y gestión de archivos
from shutil import copytree, ignore_patterns

'''
Script para obtener listado de ROMS en directorio, listado de ventanas abiertas,
detección de ventana juego en ejecución, detección de dispositivos USB,
pausa del emulador, generación de GUI para listado memoria USB y detección y gestión
para eventos de dispositivos USB 
'''

#Definición de constantes y variables
WINDOWS_TXT="/home/pi/proyecto/ventanas.txt"
PATH_MEDNAFEN = "/usr/games/mednaffe"
WINDOWS_TXT = "/home/pi/proyecto/ventanas.txt"
PID_TXT = "/home/pi/proyecto/pid.txt"
ROMS_TXT = "/home/pi/proyecto/roms.txt"
USB_TXT = "/home/pi/proyecto/usb.txt"
PATH_ROM = "/home/pi/proyecto/Roms"
PATH_USB_DIR = "/home/pi/proyecto/usb"
PATH_MEDIA = "/media/pi/6061-6154"

'''
Función para obtener ROMS disponibles precargadas
Regresa una lista con todas las ROMS en formato String
'''
def retrieve_rom_names():
	new_list = list()
	os.popen('ls {} > {}'.format(PATH_ROM,ROMS_TXT)) 					#Comando para listar y escribir en archivo .txt
	sleep(0.05)
	with open('{}'.format(ROMS_TXT), 'r') as rom_txt:
		# Using readlines()
		contenido = rom_txt.readlines()									#Se lee el archivo por lineas para obtener ROMS de forma individual

		for x in contenido:												#Se recorre la lista para eliminar saltos de línea y extensión de archivos
			nonl_noext_string = os.path.splitext("{}".format(x))[0]
			new_list.append(nonl_noext_string)
	return new_list

'''
Función para obtener listado de ventanas actualmente abiertas, es decir, minimizadas o maximizadas
Regresa una string que contiene todas las ventanas
'''
def retrieve_windows():
	contenido = ""
	os.popen('wmctrl -l > {}'.format(WINDOWS_TXT))						#Comando para listar las ventanas abiertas y escribir en .txt
	sleep(0.05)
	with open("{}".format(WINDOWS_TXT), 'r') as w_txt:					#Se lee archivo y se almacena todo en una String
		contenido = w_txt.read()
	return contenido

'''
Función para encontrar juego actualmente abierto, mediante coincidencia entre 
el nombre de la ROM y el nombre de la ventana
Regresa la coincidencia entre juego y ventana
'''
def match_rom_window_get_name():
	rom_list = retrieve_rom_names()										#Se obtiene la lista de ROMS
	sleep(0.05)
	window_string = retrieve_windows()									#Se obtiene la lista de ventanas
	for x in rom_list:													#Se compara la lista de ROMS con la String de ventanas
		if window_string.find(x) != -1:									#Al momento de encontrar coincidencia, sale del ciclo
			return x 													
			break

'''
Función para eliminar los espacios una vez encontrado el nombre de la ROM
Regresa el primer elemento de la lista para obtener sólo la primera
palabra del juego
'''
def terminal_xdotool_string(string):
	x = string.split(" ")
	return x[0]

'''
Se crea un monitor para dispositivos USB
'''
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

'''
Variables para control de USB insertada y ciclo para añadir dispositivo
'''
usb_inserted = False
double = 0

source = '/media/pi/6061-6154'											#Ruta para encontrar dispositivo USB montado

'''
Ciclo infinito encargado de monitorear nuevos dispositivos insertados
para ejecutar comandos sobre el juego y abrir GUI de ROMS en USB
'''
while True:
	contenido = ""
	for device in iter(monitor.poll, None):								#Se itera sobre los dispositivos conectados
		if device.action == 'add':										#Cuando se conecte un nuevo dispositivo se
																		#identifica mediante acción "add"
			print('{} connected'.format(device))
			usb_inserted = True											#Se conectó un nuevo dispositivo, se actualizan
			double +=1													#banderas de control	
			break

	'''
	Sección donde son gestionadas las acciones para el juego y el GUI
	'''
	if usb_inserted and double==2:
		rom_name = terminal_xdotool_string(match_rom_window_get_name())	#Se obtiene el nombre de la ROM que se está
		print(rom_name)													#ejecutando al momento

		#Llamada a subproceso que consiste en un script de bash para ejecutar comando y escribir en archivo .txt
		#El bash de script busca el identificador del programa
		subprocess.call(['bash','/home/pi/proyecto/scripts/escribirIDW.sh', rom_name])
		sleep(1)
		with open("{}".format(PID_TXT), 'r') as w_txt:					#Se lee archivo .txt y se eliminan
			contenido = w_txt.read()									#los saltos de línea
			contenido = contenido.split("\n")
			print(contenido)											#Líneas de comprobación para ejecución de 
		print(contenido[0])												#comandos posteriores
		prueba=[]
		prueba[:0]=contenido[0]
		print(prueba)
		sleep(1)
		#Llamada a subproceso que consiste en un script de bash para ejecutar comando
		#El bash de script, mediante el ID del programa, simula la tecla Return
		subprocess.call(['bash','/home/pi/proyecto/scripts/presionar_enter.sh', contenido[0]])
		sleep(2)

		'''
		Sección donde se realiza el copiado y desplegado de GUI con ROMS disponibles
		'''
		if os.path.exists("/home/pi/TMP_ROMS/"):						#Se crea un directorio temporal para almacenar
			if os.listdir():											#las ROMS que son copiadas mediante shutil
				continue
		shutil.copytree(source, "/home/pi/TMP_ROMS/")
		lst_usb_roms = list()
		os.popen('ls /home/pi/TMP_ROMS > /home/pi/proyecto/usb.txt') 	#Se usa el directorio temporal para escribir
		sleep(0.05)														#en .txt las ROMS copiadas
		with open('{}'.format(USB_TXT), 'r') as usb_txt:
			contenido = usb_txt.readlines()
			for x in contenido:											#Se lee del archivo txt las ROMS, se quitan 
				nonl_noext_string = os.path.splitext("{}".format(x))[0]	#saltos de línea y extensiones, así como
				lst_usb_roms.append(nonl_noext_string)					#agregarlas a una nueva lista que se usa en TKINTER
				
		sleep(0.05)
		os.popen("cp -r /home/pi/TMP_ROMS/* /home/pi/proyecto/Roms")	#Se copian las ROMS del directorio temporal al
		sleep(0.05)														#directorio permanente de ROMS.
		os.popen("rm -r /home/pi/TMP_ROMS")
		
		usb_inserted = False											#Se actualizan las banderas de control
		double = 0
		
		rootwindow = tkinter.Tk()										#Se crea un objeto TKINTER
		rootwindow.title("Lista de ROMS USB")							#se agrega un título a la ventana, así como 
		rootwindow.geometry("800x500")									#un tamaño de ventana y fuente fijos
		roms = Text(rootwindow, font=("Helvetica", 20))
		for x in lst_usb_roms:											#Se usa la lista anteriormente creada para 
			roms.insert(END, x + '\n')									#insertarla al objeto texto y juntar las 
		roms.pack()														#String
		rootwindow.eval('tk::PlaceWindow . center')
		
		rootwindow.mainloop()											#Se despliega la ventana creada dentro del MAINLOOP
		
