import psutil
import os
from datetime import datetime

HEADER_HEIGHT = 2

def get_pid_info(pid):
    if not psutil.pid_exists(pid):
        print("PID '%d' does not exists" % pid)
        return

    process = psutil.Process(pid)

    info = { "pid": pid }
    info["name"] = process.name()
    info["mem"] = process.memory_percent()
    info["cpu"] = process.cpu_percent()
    info["threads"] = process.num_threads()
    info["creation_time"] = int(process.create_time())
    info["owner"] = process.username()

    return info

def get_process_list():
    pids = psutil.pids()
    process_list = []

    for pid in pids:
        process_list.append(get_pid_info(pid))

    return process_list

def filter_by_name(process_list, query):
    return [p
            for p in process_list
            if query in p["name"]]

def format_process(process):
    # pid   name    mem%    cpu%    threads     yyyy-mm-dd hh:mm:ss     owner
    creation_date = datetime.fromtimestamp(process["creation_time"])
    formatted_date = creation_date.strftime("%Y-%m-%d %H:%M:%S")

    return "%d\t%s\t%.2f%%\t%.2f%%\t%d\t%s\t%s" % (process["pid"], process["name"],
                                                   process["mem"], process["cpu"], process["threads"],
                                                   formatted_date, process["owner"])

def get_process_list_header():
    return "PID\tName\tMem%\tCPU%\tThreads\tDate\tOwner\n" + ("─" * os.get_terminal_size().columns)

available_lines = os.get_terminal_size().lines - HEADER_HEIGHT
process_list = get_process_list()
print(get_process_list_header())

for i, process in enumerate(process_list):
    if i + 1 >= available_lines:
        break

    print(format_process(process))
