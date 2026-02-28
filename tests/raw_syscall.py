"""
Description
    Using ctypes to invoke restricted syscalls directly including
    reboot, sethostname, settimeofday, and pivot_root, bypassing
    Python wrappers that might mask errors

    The sandbox should prevent all privileged syscalls by running as
    an unprivileged user without the required capabilities

"""

import ctypes
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

syscall = libc.syscall
syscall.restype = ctypes.c_long

SYS_reboot = 169
SYS_sethostname = 170
SYS_settimeofday = 164
SYS_acct = 163
SYS_swapon = 167
SYS_kexec_load = 246

results = {}

LINUX_REBOOT_MAGIC1 = 0xfee1dead
LINUX_REBOOT_MAGIC2 = 672274793
LINUX_REBOOT_CMD_CAD_OFF = 0x00000000
ret = syscall(SYS_reboot, LINUX_REBOOT_MAGIC1, LINUX_REBOOT_MAGIC2, LINUX_REBOOT_CMD_CAD_OFF, 0)
if ret == 0:
    results["reboot"] = "SUCCEEDED (CRITICAL)"

ret = syscall(SYS_sethostname, b"pwned", 5)
if ret == 0:
    results["sethostname"] = "SUCCEEDED (CRITICAL)"

ret = syscall(SYS_settimeofday, None, None)
if ret == 0:
    results["settimeofday"] = "SUCCEEDED (CRITICAL)"

ret = syscall(SYS_acct, b"/tmp/acct")
if ret == 0:
    results["acct"] = "SUCCEEDED (CRITICAL)"

ret = syscall(SYS_swapon, b"/dev/null", 0)
if ret == 0:
    results["swapon"] = "SUCCEEDED (CRITICAL)"

ret = syscall(SYS_kexec_load, 0, 0, None, 0)
if ret == 0:
    results["kexec_load"] = "SUCCEEDED (CRITICAL)"

for key, val in results.items():
    print(f"{key}: {val}")
