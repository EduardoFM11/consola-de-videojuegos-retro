#Script en BASH para ejecutar comando en temrinal y obtener el identificador de proceso de una ventana

#! /bin/bash		#Se especifica el uso de BASH

<<licence
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
licence

ACTION=$1 						#Se recibe la acción del dispositivo
DEVBASE=$2						#Se recibe el punto de montaje inicial
DEVICE="/dev/${DEVBASE}"		#Se construye la ruta entera a partir de /dev/sd[a-z][0-9]


sudo mkdir /media/pi/6061-6154	#Comando para crear punto de montaje
sudo mount ${DEVICE} /media/pi/6061-6154	#Comando para montar el dispositivo