import psutil
import tkinter as tk
from tkinter import ttk
from tabulate import tabulate
import time

class RoundRobinScheduler:
    def __init__(self, procesos_info, quantum):
        self.procesos_info = procesos_info
        self.queue = list(procesos_info)
        self.quantum = quantum
        self.proceso_actual = None
        self.procesos_atendidos = []
        self.tiempo_inicio_proceso = 0
        self.tiempo_ejecucion = 0

    def siguiente_proceso(self):
        if not self.proceso_actual or time.time() - self.tiempo_inicio_proceso >= self.quantum:
            if self.queue:
                self.proceso_actual = self.queue.pop(0)
                self.tiempo_inicio_proceso = time.time()
                self.tiempo_ejecucion = 0  # Reiniciar el tiempo de ejecución
                self.procesos_atendidos.append((self.proceso_actual[0], self.proceso_actual[1], "hola", 'En espera'))
            else:
                self.proceso_actual = None
        return self.proceso_actual

    def resolver_proceso(self):
        if self.proceso_actual:
            # Restar el tiempo que ha pasado desde la última vez que se resolvió el proceso
            self.tiempo_ejecucion += time.time() - self.tiempo_inicio_proceso

            if self.tiempo_ejecucion >= self.quantum:
                # El proceso ha consumido el quantum completo
                self.queue.append(self.proceso_actual)
                self.procesos_atendidos[-1] = (self.proceso_actual[0], self.proceso_actual[1], self.quantum, 'Espera')
                self.proceso_actual = None
            elif self.tiempo_ejecucion < self.quantum:
                # El quantum ha terminado, pero el proceso no ha consumido el quantum completo
                self.queue.append(self.proceso_actual)
                self.procesos_atendidos[-1] = (self.proceso_actual[0], self.proceso_actual[1], self.tiempo_ejecucion, 'Terminado')
                self.proceso_actual = None


def obtener_procesos():
    procesos = psutil.process_iter(['pid', 'name', 'cpu_percent'])
    procesos_info = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) for p in procesos]
    return procesos_info

def round_robin():
    proceso_actual = scheduler.siguiente_proceso()
    if proceso_actual:
        tiempo_restante = scheduler.tiempo_inicio_proceso
        tabla_data = tabulate([(proceso_actual[0], proceso_actual[1], tiempo_restante)], headers=encabezados1, tablefmt="pretty")
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, tabla_data)
        text_widget.config(state=tk.DISABLED)
        scheduler.resolver_proceso()
        actualizar_procesos_atendidos()

    root.after(1000, round_robin)  # Programar la próxima iteración del Round Robin

def actualizar_procesos_atendidos():
    tree.delete(*tree.get_children())
    for pid, nombre, estado, tiempo_restante in scheduler.procesos_atendidos:
        tree.insert('', 'end', values=(pid, nombre, estado, tiempo_restante))

def salir():
    root.destroy()

root = tk.Tk()
root.title("Visualizador de Procesos - Round Robin")

encabezados1 = ["PID", "Nombre", "Tiempo Ejecucion"]
encabezados2 = ["PID", "Nombre", "Tiempo Restante", "Estado"]

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget = tk.Text(root, font=("Courier", 10), wrap=tk.NONE, yscrollcommand=scrollbar.set)
text_widget.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

scrollbar.config(command=text_widget.yview)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menú", menu=file_menu)

file_menu.add_command(label="Round Robin", command=round_robin)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=salir)

procesos_info = obtener_procesos()
quantum = 2
scheduler = RoundRobinScheduler(procesos_info, quantum)

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

tree = ttk.Treeview(frame, columns=encabezados2, show='headings')
for col in encabezados2:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

tree.pack(expand=True, fill=tk.BOTH)

root.mainloop()
