import psutil

def get_pid_info(pid):
    if not psutil.pid_exists(pid):
        print("PID '%d' does not exists" % pid)
        return

    process = psutil.Process(pid)

    info = { "pid": pid }
    info["name"] = process.name()
    info["mem_percent"] = process.memory_percent()
    info["cpu_percent"] = process.cpu_percent()
    info["threads"] = process.num_threads()
    info["creation_time"] = int(process.create_time())
    #info["path"] = process.exe()
    info["owner"] = process.username()

    return info

def get_process_list():
    pids = psutil.pids()
    process_list = []

    for pid in pids:
        process_list.append(get_pid_info(pid))

    return process_list
