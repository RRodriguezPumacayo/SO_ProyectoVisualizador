#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

class Proceso(object):
	'''Nuestro Objeto de tipo Proeso se inicia vacio'''
	pass

def iniciarMenu(datos_generales):
	'''Menu Principal del programa'''
	global lista_procesos

	clear()
	identificador = 0
	while True:
		identificador += 1
		'''Crea un nuevo proceso y le asigna valores ingresados por el usuario'''
		try:
			print("Agrega los datos con el siguiente formato")
			print("nombre, tiempo_ejecucion, llegada, prioridad, tamano_memoria")
			datos_entrada = input()
			nuevo_proceso = parseador(datos_entrada, identificador)
			lista_procesos.append(nuevo_proceso)

		except (RuntimeError, TypeError, NameError, IndexError, ValueError):
			print("Oops! El proceso no es válido. Vuelve a intentarlo")

		reiniciar = input("Agregar Otro (Y,N): ")
		if (reiniciar == "N" or reiniciar == "n"):
			lista_procesos.sort(key=lambda x: x.prioridad)
			imprimirDetallesLista(lista_procesos) 
			return identificador
			break

def parseador(datos_entrada, identificador):
	"Parseamos los datos y los ubicamos en un ojeto tipo proceso"

	datos = datos_entrada.split(',')
	nuevo_proceso = Proceso()
	nuevo_proceso.identificador = identificador
	nuevo_proceso.nombre = str(datos[0])
	nuevo_proceso.tamano_memoria = int(datos[4])
	nuevo_proceso.tiempo_rafaga = int(datos[1])
	nuevo_proceso.tr_init = int(datos[1])
	nuevo_proceso.prioridad = int(datos[3])
	nuevo_proceso.llegada = int(datos[2])
	nuevo_proceso.proceso_limpio = 1

	return nuevo_proceso

def cargarMemoria(datos):
	'''Carga de la lista de procesos al CPU'''
	global lista_procesos
	global procesos_en_cpu
	tiempo_procesador = datos['tiempo_procesador']
	i = 0

	while i < len(lista_procesos):
		proceso = lista_procesos[i]
		if proceso.llegada <= tiempo_procesador:
			if (datos['tamano_memoria'] - proceso.tamano_memoria) > 0 :
				proceso_cargar = lista_procesos.pop(i)
				procesos_en_cpu.append(proceso_cargar)
				print(str(proceso_cargar.nombre) + ": Cargado en CPU")
				imprimirLista(lista_procesos, procesos_en_cpu, tiempo_procesador)

			else: print("[TP: " + str(tiempo_procesador) + "]" + 
					str(proceso.nombre) + ": No hay memoria suficiente.")
		else: break

	if lista_procesos and not procesos_en_cpu:
		print("[TP: " + str(tiempo_procesador) +"] No se encontraron procesos")
		tiempo_procesador = tiempo_procesador + 1
	if not lista_procesos: return tiempo_procesador
	return tiempo_procesador

def planificadorRR(datos):
	'''Logica del planificador Round Robin'''
	global lista_procesos
	global procesos_en_cpu
	QUANTUM = int(input("Ingresa el valor del Quantum: "))

	while True:
		if(not lista_procesos and not procesos_en_cpu):
			print("El planificador ha terminado.")
			finalizarTiempoPromedio(datos)
			imprimirDictionario(datos)
			break
		datos['tiempo_procesador'] = cargarMemoria(datos)
		tiempo = datos['tiempo_procesador']

		for proceso in procesos_en_cpu:
			print("Subió proceso:" + str(proceso.nombre))
			if proceso.proceso_limpio == 1:
				proceso.proceso_limpio = 0
				proceso.primer_ejecucion = tiempo

			for x in range(QUANTUM):
				if proceso.tiempo_rafaga - QUANTUM <= 0: 
					proceso.ultima_ejecucion = tiempo
					proceso.ya_ejecutado = proceso.tr_init - proceso.tiempo_rafaga
				proceso.tiempo_rafaga -= 1
				tiempo = tiempo + 1
				if proceso.tiempo_rafaga == 0:
					agregarTiempoPromedio(datos,proceso,tiempo)
					indice = procesos_en_cpu.index(proceso)
					procesos_en_cpu.pop(indice)
					print("[TP: " + str(datos['tiempo_procesador']) + "]" + 
					str(proceso.nombre) + ": Termino su Ejecucion")
					imprimirLista(lista_procesos, procesos_en_cpu,tiempo)
					break

			datos['tiempo_procesador'] = tiempo

def finalizarTiempoPromedio(datos):
	'''Imprime los datos de los tiempos'''
	datos['tiempo_ejecucion'] = datos.get('tiempo_ejecucion') / datos.get('num_procesos')
	datos['tiempo_espera'] = datos.get('tiempo_espera') / datos.get('num_procesos')
	datos['tiempo_respuesta'] = datos.get('tiempo_respuesta') / datos.get('num_procesos')
	return datos

def agregarTiempoPromedio(datos, proceso, tiempo):
	'''Suma los timepos promedios de los procesos'''
	datos['tiempo_ejecucion'] = datos.get('tiempo_ejecucion') + tiempo - proceso.llegada
	datos['tiempo_espera'] = datos.get('tiempo_espera') + proceso.ultima_ejecucion - proceso.ya_ejecutado - proceso.llegada
	print(str(proceso.primer_ejecucion) + "-" + str(proceso.llegada))
	datos['tiempo_respuesta'] = datos.get('tiempo_respuesta') + proceso.primer_ejecucion - proceso.llegada
	return datos

def imprimirDetallesLista(lista):
	for proceso in lista:
		print("[" + str(proceso.nombre) + ", " + str(proceso.tiempo_rafaga) +
			", " + str(proceso.llegada) + "]")

def imprimirLista(cola_procesos, cpu_procesos, tiempo):
	'''imprime la todas las listas de procesos'''
	print("[TP: " + str(tiempo) + "]")
	print("LP:", end="", flush=True)
	imprimirProceso(cola_procesos)
	print("LPC:", end="", flush=True)
	imprimirProceso(cpu_procesos)

def imprimirProceso(lista):
	print("[", end="", flush=True)
	for proceso in lista:
		print(proceso.nombre + ", ", end="", flush=True)
	print("]", end="", flush=True)
		
def imprimirDictionario(dictionary):
	for key, value in dictionary.items():
		print (key, value)

def main():
	datos_generales = {'tiempo_procesador':0, 'tamano_memoria':2000, 
	'tiempo_respuesta':0, 'tiempo_ejecucion':0, 'tiempo_espera':0, 
	'num_procesos':0}
	datos_generales['num_procesos'] = iniciarMenu(datos_generales)
	planificadorRR(datos_generales)

if __name__ == '__main__':
	clear = lambda: os.system('clear')
	lista_procesos = []
	procesos_en_cpu = []

	main()


