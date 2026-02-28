"""
Description
    Using ptrace to attach to other processes visible in the sandbox
    and attempt to read or manipulate their memory

    The sandbox should prevent ptrace by running as an unprivileged user
    without CAP_SYS_PTRACE, and the PID namespace limits visible targets

"""

import ctypes
import ctypes.util
import os

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

PTRACE_ATTACH = 16
PTRACE_PEEKDATA = 2
PTRACE_DETACH = 17

targets = [1, os.getppid()]

for pid in targets:
    if pid == os.getpid() or pid <= 0:
        continue
    ret = libc.ptrace(PTRACE_ATTACH, pid, None, None)
    if ret == 0:
        print(f"ptrace ATTACH to PID {pid} SUCCEEDED (CRITICAL)")
        libc.ptrace(PTRACE_DETACH, pid, None, None)

# Also try to ptrace our own child
pid = os.fork()
if pid == 0:
    import time
    time.sleep(1)
    os._exit(0)
else:
    import time
    time.sleep(0.1)
    ret = libc.ptrace(PTRACE_ATTACH, pid, None, None)
    if ret == 0:
        libc.ptrace(PTRACE_DETACH, pid, None, None)
    try:
        os.waitpid(pid, 0)
    except:
        pass
