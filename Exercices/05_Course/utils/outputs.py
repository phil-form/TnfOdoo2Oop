import threading

__print_lock = threading.Lock()

def locked_print(*args, sep=' ', end='\n'):
    with __print_lock:
        print(*args, sep=sep, end=end)