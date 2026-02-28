"""
Description
    Creating SysV message queues and semaphores to attempt cross-sandbox
    communication and interference between different job instances

    The sandbox should isolate SysV IPC namespaces per sandbox instance
    via CLONE_NEWIPC, preventing cross-sandbox message queue and
    semaphore access

"""

import ctypes
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

IPC_CREAT = 0o1000
IPC_EXCL = 0o2000
IPC_RMID = 0

msg_key = 0xDEAD0001
msqid = libc.msgget(msg_key, IPC_CREAT | IPC_EXCL | 0o666)
if msqid >= 0:
    print(f"SysV msgqueue created: msqid={msqid}")
    libc.msgctl(msqid, IPC_RMID, None)
else:
    msqid = libc.msgget(msg_key, 0o666)
    if msqid >= 0:
        print(f"SysV msgqueue from previous run found: msqid={msqid} (CRITICAL)")

sem_key = 0xDEAD0002
semid = libc.semget(sem_key, 1, IPC_CREAT | IPC_EXCL | 0o666)
if semid >= 0:
    print(f"SysV semaphore created: semid={semid}")
    libc.semctl(semid, 0, IPC_RMID)
else:
    semid = libc.semget(sem_key, 1, 0o666)
    if semid >= 0:
        print(f"SysV semaphore from previous run found: semid={semid} (CRITICAL)")
