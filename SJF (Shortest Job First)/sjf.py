import os
import psutil
from tabulate import tabulate

def get_running_processes():
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            pinfo = proc.info
            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'create_time': pinfo['create_time']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return sorted(processes, key=lambda x: x['create_time'])

def sjf_planificador():
    #Logica SJF
    return
