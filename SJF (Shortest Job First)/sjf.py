import os
import psutil
import time
from tabulate import tabulate

class Proceso:
    def __init__(self, pid, nombre, tiempo_ejecucion):
        self.pid = pid
        self.nombre = nombre
        self.tiempo_ejecucion = tiempo_ejecucion

    def __lt__(self, other):
        return self.tiempo_ejecucion < other.tiempo_ejecucion

def sjf_scheduler(procesos):
    tiempo_actual = 0
    cola_listos = []

    while procesos or cola_listos:
        for proceso in list(procesos):
            if psutil.pid_exists(proceso.pid):
                cola_listos.append(proceso)
                procesos.remove(proceso)

        if cola_listos:
            cola_listos.sort()
            proceso_actual = cola_listos.pop(0)

            print(f"Ejecutando {proceso_actual.nombre} (PID: {proceso_actual.pid}) durante {proceso_actual.tiempo_ejecucion} unidades de tiempo")

            if proceso_actual.tiempo_ejecucion > 0:
                time.sleep(1)

    print("\nTodos los procesos han sido ejecutados.")
    

def obtener_procesos():
    procesos = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            pinfo = proc.info
            if pinfo['cpu_percent'] is not None:
                procesos.append(Proceso(pinfo['pid'], pinfo['name'], pinfo['cpu_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return procesos

if __name__ == "__main__":
    procesos_anteriores = set()

    try:
        while True:
            os.system('clear')

            procesos_actuales = obtener_procesos()

            if procesos_actuales != procesos_anteriores:
                procesos_anteriores = procesos_actuales.copy()

                if procesos_actuales:
                    print("Procesos en ejecución:")
                    print(tabulate([(p.nombre, p.pid, p.tiempo_ejecucion) for p in procesos_actuales], headers=["Nombre", "PID", "Tiempo de Ejecución"]))
                    print("\n")

                    print("Planificación SJF:")
                    sjf_scheduler(procesos_actuales)
                else:
                    print("No hay procesos en ejecución.")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nVisualización terminada.")
