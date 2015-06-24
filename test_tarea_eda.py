#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from sys import argv as args
from os import system as run

programa = args [1]
run ('valgrind --tool=massif --stacks=yes --time-unit=i --massif-out-file=massif.out ' + programa)

archivo = open ('massif.out', 'r')
lineas = archivo.readlines ()
archivo.close ()

maxmem = 0
for linea in lineas:
	if linea.startswith ('mem_heap_B='):
		tempmem = int (linea.split ('=') [1].split ('\n') [0])
	if linea.startswith ('mem_stacks'):
		tempmem = tempmem + int (linea.split ('=') [1].split ('\n') [0])
		if maxmem < tempmem:
			maxmem = tempmem
	if linea.startswith ('time='):
		time = int (linea.split ('=') [1].split ('\n') [0])
	
print 'Memoria máxima utilizada:', maxmem, 'B'
print 'Tiempo de ejecución:', time, 'instr.'
