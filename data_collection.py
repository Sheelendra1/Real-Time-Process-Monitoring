import psutil
import time

def check_computer_health():
    processor_busy = psutil.cpu_percent(interval=1)
    memory_status = psutil.virtual_memory()
    memory_used = memory_status.percent
    running_tasks = []
    for task in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        running_tasks.append(task.info)
    computer_stats = {
        'processor_busy': processor_busy,
        'memory_used': memory_used,
        'running_tasks': running_tasks
    }
    return computer_stats
