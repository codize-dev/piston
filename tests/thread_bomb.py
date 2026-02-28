"""
Description
    Creating a massive number of threads to exhaust system resources
    through a different code path than the fork bomb, since threads
    share address space but still consume kernel scheduling resources

    The sandbox should limit the total number of tasks (threads + processes)
    via the RLIMIT_NPROC limit and terminate the process on timeout

"""

import threading
import time

def spin():
    while True:
        time.sleep(1)

threads = []
while True:
    try:
        t = threading.Thread(target=spin, daemon=True)
        t.start()
        threads.append(t)
    except:
        pass
