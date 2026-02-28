"""
Description
    Using unshare syscall to create new user, mount, or PID namespaces
    in an attempt to gain elevated privileges or bypass sandbox
    constraints

    The sandbox should prevent unprivileged namespace creation, either
    via lacking capabilities or kernel settings restricting
    user namespace creation

"""

import ctypes
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

CLONE_NEWUSER = 0x10000000
CLONE_NEWNS = 0x00020000
CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000
CLONE_NEWIPC = 0x08000000

namespaces = [
    ("CLONE_NEWUSER", CLONE_NEWUSER),
    ("CLONE_NEWNS", CLONE_NEWNS),
    ("CLONE_NEWPID", CLONE_NEWPID),
    ("CLONE_NEWNET", CLONE_NEWNET),
    ("CLONE_NEWIPC", CLONE_NEWIPC),
]

for name, flag in namespaces:
    ret = libc.unshare(flag)
    if ret == 0:
        print(f"unshare({name}) SUCCEEDED (CRITICAL)")

ret = libc.unshare(CLONE_NEWUSER | CLONE_NEWNS)
if ret == 0:
    print("unshare(NEWUSER|NEWNS) SUCCEEDED (CRITICAL)")
