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

def filter_by_mem(process_list):
   process_list.sort(key=lambda x: 100 - x["mem"])

def format_process(process):
    # pid   name    mem%    cpu%    threads     yyyy-mm-dd hh:mm:ss     owner
    creation_date = datetime.fromtimestamp(process["creation_time"])
    formatted_date = creation_date.strftime("%Y-%m-%d %H:%M:%S")

    return "%d\t%s\t%.2f%%\t%.2f%%\t%d\t%s\t%s" % (process["pid"], process["name"].split("/")[0],
                                                   process["mem"], process["cpu"], process["threads"],
                                                   formatted_date, process["owner"])

def show_process_list():
    terminal_size = os.get_terminal_size()

    terminal_cols = terminal_size.columns
    terminal_rows = terminal_size.lines
    available_rows = terminal_rows - HEADER_HEIGHT

    print("PID\tName\tMem%\tCPU%\tThreads\tDate\tOwner\n" + ("─" * terminal_cols))

    process_list = get_process_list()
    filter_by_mem(process_list)
    for i, process in enumerate(process_list):
        if i + 1 >= available_rows: break
        print(format_process(process))

    print("\033[{};{}H".format(0, 0), end='', flush=True) # move cursor to the start of screen

while 1: show_process_list()
