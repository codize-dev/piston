"""
Description
    Attempting to load kernel modules via init_module and finit_module
    syscalls, which would allow arbitrary kernel code execution

    The sandbox should prevent module loading by running as an
    unprivileged user without CAP_SYS_MODULE capability

"""

import ctypes
import ctypes.util
import os

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

SYS_init_module = 175
SYS_finit_module = 313
SYS_delete_module = 176

syscall = libc.syscall
syscall.restype = ctypes.c_long

dummy_module = b"\x00" * 64
ret = syscall(SYS_init_module, dummy_module, len(dummy_module), b"")
if ret == 0:
    print("init_module SUCCEEDED (CRITICAL)")

try:
    fd = os.open("/dev/null", os.O_RDONLY)
    ret = syscall(SYS_finit_module, fd, b"", 0)
    if ret == 0:
        print("finit_module SUCCEEDED (CRITICAL)")
    os.close(fd)
except OSError:
    pass

ret = syscall(SYS_delete_module, b"dummy_module", 0)
if ret == 0:
    print("delete_module SUCCEEDED (CRITICAL)")
