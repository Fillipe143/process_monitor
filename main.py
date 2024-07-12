import psutil
import os
from datetime import datetime

def get_pid_info(pid: int) -> list[str]:
    if not psutil.pid_exists(pid):
        print("PID '%d' does not exists" % pid)
        return ["-1", "None", "0.00", "0.00", "0", "0000-00-00 00:00:00", "None"]

    process = psutil.Process(pid)

    creation_date = datetime.fromtimestamp(int(process.create_time()))
    formatted_date = creation_date.strftime("%Y-%m-%d %H:%M:%S")

    return [
            str(pid),
            process.name().split("/")[0],
            str(int(process.memory_percent() * 100) / 100),
            str(int(process.cpu_percent() * 100) / 100),
            str(process.num_threads()),
            formatted_date,
            process.username()
    ]


def fit_text_int(text: str, space: int) -> str :
    text_size = min(len(text), space)
    return text[:text_size] + (" " * (space - text_size))

def print_table(table: list[list[str]], width: float, height: float):
    cols_width = []

    for row in table:
        for i, value in enumerate(row):
            val_size = len(value)
            if i >= len(cols_width): cols_width.append(val_size)
            else: cols_width[i] = max(cols_width[i], val_size)

    cols_ratio = width / sum(cols_width) 
    is_header = True

    for h, row in enumerate(table):
        if h + 2 >= height: break

        for i, value in enumerate(row):
            text = fit_text_int(value, int(cols_width[i] * cols_ratio))
            print(text, end="")
        print()

        if is_header:
            print("─" * int(width))
            is_header = False

def get_list_of_process():
    process = []
    for pid in psutil.pids():
        info = get_pid_info(pid)
        process.append(info)
    return process

def sort_process_by_mem(process_list):
       process_list.sort(key=lambda p: 100 - float(p[2]))

def print_info():
    table = [["PID", "Name", "Mem%", "CPU%", "Threads", "Date", "Owner"]]

    process_list = get_list_of_process()
    sort_process_by_mem(process_list)
    for process in process_list: table.append(process)

    term_size = os.get_terminal_size()
    print_table(table, term_size.columns, term_size.lines)
    print("\033[{};{}H".format(0, 0), end='', flush=True) # move cursor to the start of screen

while 1: print_info()
