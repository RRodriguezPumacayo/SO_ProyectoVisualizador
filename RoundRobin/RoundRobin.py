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
            
            # Significa que el proceso termino durante el proceso del quantum
            tiempo_restante = quantum - self.tiempo_total_ejecucion[self.proceso_actual[0]]

            if tiempo_restante < 0:
                # El proceso ha consumido el quantum completo
                self.queue.append(self.proceso_actual)
                self.procesos_atendidos[-1] = (self.proceso_actual[0], self.proceso_actual[1], tiempo_restante, 'Espera')
                self.proceso_actual = None
            elif tiempo_restante > 0:
                # El quantum ha terminado, pero el proceso no ha consumido el quantum completo
                self.queue.append(self.proceso_actual)
                self.procesos_atendidos[-1] = (self.proceso_actual[0], self.proceso_actual[1], 0, 'Terminado')
                self.proceso_actual = None

                # Simular el tiempo de ejecución del proceso durante el quantum
                tiempo_restante_decimal = tiempo_ejecucion % 1
                time.sleep(tiempo_restante_decimal)                
    
    def obtener_tiempo_total_ejecucion(self):
        return self.tiempo_total_ejecucion
    
def obtener_procesos():
    procesos = psutil.process_iter(['pid', 'name', 'cpu_percent'])
    procesos_info = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) for p in procesos]
    return procesos_info

def round_robin():
    proceso_actual = scheduler.siguiente_proceso()
    if proceso_actual:
        tiempo_acumulado = scheduler.obtener_tiempo_total_ejecucion()
        tabla_data = tabulate([(proceso_actual[0], proceso_actual[1], tiempo_acumulado)], headers=encabezados1, tablefmt="pretty")
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

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

tree = ttk.Treeview(frame, columns=encabezados2, show='headings')
for col in encabezados2:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

tree.pack(expand=True, fill=tk.BOTH)


procesos_info = obtener_procesos()
quantum = 5
scheduler = RoundRobinScheduler(procesos_info, quantum)

# Calcular tiempo total de ejecución antes de iniciar Round Robin
tiempo_total_ejecucion_inicial = scheduler.obtener_tiempo_total_ejecucion()
print(f'Tiempo Total de Ejecución Inicial: {tiempo_total_ejecucion_inicial}')

root.mainloop()
