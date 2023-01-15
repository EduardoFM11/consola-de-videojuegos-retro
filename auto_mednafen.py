#! /usr/bin/env python3
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

import os					#Libreria para acceder a funciones del sistema											
from time import sleep		

'''
Script para abrir la interfaz gráfica del emulador 
Se espera la apertura de la ventana para ejecutar un comando y
maximizar la ventana
'''

#Definición de constantes y variables
WINDOWS_TXT="/home/pi/proyecto/ventanas.txt" 
salir = False

if __name__ == '__main__':
	#Se utiliza el método POPEN del sistema para ejecutar comandos de línea
	
	os.popen("cd /usr/games/ ; ./mednaffe")	#Se ejecuta la GUI del emulador	
	
	#Ciclo que espera la confirmación de la apertura de la ventana mediante el listado de las ventanas
	#abiertas al momento, esto se escribe a un archivo que posteriormente es leido.
	while salir == False:
		os.popen('wmctrl -l > {}'.format(WINDOWS_TXT)) 					#Listado de ventanas y escritura en .txt
		with open("{}".format(WINDOWS_TXT), 'r') as w_txt:				#Se abre el .txt y se lee, obteniendo String completa
			contenido = w_txt.read()
			if contenido.find('Mednaffe') != -1:						#Se busca una coincidencia con el nombre de la ventana
				os.popen("wmctrl -r 'Mednaffe' -b toggle,fullscreen")
				salir = True											#Se activa la bandera para terminar el ciclo infinito
			else:
				salir = False											#No se ha encontrado la ventana,sigue ciclo infinito