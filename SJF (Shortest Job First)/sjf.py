import os
import psutil
import time
from tabulate import tabulate

def get_running_processes():
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'status']):
        try:
            pinfo = proc.info
            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'create_time': pinfo['create_time'],
                'cpu_percent': pinfo['cpu_percent'],
                'status': pinfo['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return sorted(processes, key=lambda x: x['create_time'])

def sjf_scheduler():
    #Logica SJF
    return

