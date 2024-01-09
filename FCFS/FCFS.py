import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from queue import Queue

class FCFSVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador FCFS")
        self.root.geometry("800x600")

        self.process_queue = Queue()
        self.current_process = None

        self.create_widgets()
        self.update_process_data()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("PID", "Nombre", "Tiempo de Llegada"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tiempo de Llegada", text="Tiempo de Llegada")
        self.tree.pack(pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def update_process_data(self):
        processes = psutil.process_iter(attrs=['pid', 'name', 'create_time'])

        # Limpia el árbol antes de actualizar
        for item in self.tree.get_children():
            self.tree.delete(item)

        for process in processes:
            pid = process.info['pid']
            name = process.info['name']
            create_time = process.info['create_time']
            self.process_queue.put((pid, name, create_time))
            self.tree.insert("", "end", values=(pid, name, create_time))

        self.update_plot()

        # Actualiza cada 1000 milisegundos (1 segundo)
        self.root.after(1000, self.update_process_data)

    def update_plot(self):
        if self.current_process is not None:
            self.current_process.remove()

        if not self.process_queue.empty():
            pid, _, _ = self.process_queue.get()
            self.current_process = self.ax.text(0.5, 0.5, f"PID {pid}\nEn ejecución",
                                                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
                                                transform=self.ax.transAxes, ha="center", va="center")

        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FCFSVisualizer(root)
    root.mainloop()
