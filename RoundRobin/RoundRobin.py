import psutil
import tkinter as tk
from tkinter import ttk
import time

def accion():
    # La acción que quieres realizar después de esperar un tiempo
    print("¡Acción realizada!")

class RoundRobinScheduler:
    def __init__(self, procesos_info, quantum):
        self.procesos_info = procesos_info
        self.queue = list(procesos_info)
        self.quantum = quantum
        self.proceso_actual = None
        self.procesos_atendidos = []
        self.tiempo_inicio_proceso = 0
        self.tiempo_total_ejecucion = {pid: 0.0 for pid, _, _ in procesos_info}

    def siguiente_proceso(self):
        if not self.proceso_actual or time.time() - self.tiempo_inicio_proceso >= self.quantum:
            if self.queue:
                self.proceso_actual = self.queue.pop(0)
                self.tiempo_inicio_proceso = time.time()                
                self.procesos_atendidos.append((self.proceso_actual[0], self.proceso_actual[1], self.tiempo_total_ejecucion[self.proceso_actual[0]], 'En espera'))
            else:
                self.proceso_actual = None
        return self.proceso_actual
    def resolver_proceso(self):
        if self.proceso_actual:
            tiempo_ejecucion = time.time() - self.tiempo_inicio_proceso

            # Acumular el tiempo de ejecución total del proceso
            self.tiempo_total_ejecucion[self.proceso_actual[0]] += tiempo_ejecucion

            # Significa que el proceso terminó durante el proceso del quantum            
            tiempo_restante = quantum - tiempo_ejecucion

            if tiempo_restante < 0:
                # El proceso es mayor al quantum
                self.queue.append(self.proceso_actual)
                self.procesos_atendidos[-1] = (
                    self.proceso_actual[0], 
                    self.proceso_actual[1], 
                    tiempo_ejecucion,   # Tiempo de ráfaga
                    tiempo_restante,
                    'Espera'
                )
                self.proceso_actual = None
            else:                            
                # El proceso se consume durante el tiempo del quantum
                self.queue.append(self.proceso_actual)
                self.procesos_atendidos[-1] = (
                    self.proceso_actual[0], 
                    self.proceso_actual[1], 
                    tiempo_ejecucion,  
                    0,  
                    'Terminado'
                )
                self.proceso_actual = None

                # Programar la próxima iteración del Round Robin después de un cierto tiempo
            root.after(int(tiempo_restante * 1000), round_robin)


def obtener_procesos():
    procesos = psutil.process_iter(['pid', 'name', 'cpu_percent'])
    procesos_info = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) for p in procesos]
    return procesos_info


def round_robin():
    proceso_actual = scheduler.siguiente_proceso()
    if proceso_actual:
        scheduler.resolver_proceso()
        actualizar_procesos_atendidos()

def actualizar_procesos_atendidos():
    tree.delete(*tree.get_children())
    for pid, nombre, tiempo_rafaga, tiempo_restante, estado in scheduler.procesos_atendidos:        
        tree.insert('', 'end', values=(pid, nombre, tiempo_rafaga, tiempo_restante, estado))

def salir():
    root.destroy()

root = tk.Tk()
root.title("Visualizador de Procesos - Round Robin")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menú", menu=file_menu)

file_menu.add_command(label="Round Robin", command=round_robin)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=salir)

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

tree = ttk.Treeview(frame, columns=["PID", "Nombre", "Tiempo Rafaga", "Tiempo Restante", "Estado"], show='headings')
for col in ["PID", "Nombre", "Tiempo Rafaga", "Tiempo Restante", "Estado"]:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

tree.pack(expand=True, fill=tk.BOTH)

procesos_info = obtener_procesos()
quantum = 2
scheduler = RoundRobinScheduler(procesos_info, quantum)

root.mainloop()
