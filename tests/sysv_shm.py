"""
Description
    Creating SysV shared memory segments using shmget/shmat syscalls to
    attempt sharing data across sandbox instances via persistent IPC keys

    The sandbox should isolate SysV IPC namespaces per sandbox instance
    via CLONE_NEWIPC, preventing cross-sandbox shared memory access

"""

import ctypes
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

IPC_CREAT = 0o1000
IPC_EXCL = 0o2000
IPC_RMID = 0

key = 0x12345678
size = 4096
shmflg = IPC_CREAT | IPC_EXCL | 0o666

shmid = libc.shmget(key, size, shmflg)
if shmid >= 0:
    libc.shmat.restype = ctypes.c_void_p
    addr = libc.shmat(shmid, None, 0)
    if addr and addr != ctypes.c_void_p(-1).value:
        ctypes.memmove(addr, b"LEAKED_DATA\x00", 12)
        print(f"SysV shm created and written: shmid={shmid}")
        libc.shmdt(addr)
    libc.shmctl(shmid, IPC_RMID, None)
else:
    shmid = libc.shmget(key, size, 0o666)
    if shmid >= 0:
        libc.shmat.restype = ctypes.c_void_p
        addr = libc.shmat(shmid, None, 0)
        if addr and addr != ctypes.c_void_p(-1).value:
            data = ctypes.string_at(addr, 12)
            print(f"SysV shm READ from previous run: {data} (CRITICAL)")
            libc.shmdt(addr)
