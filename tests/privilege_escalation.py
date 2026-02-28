"""
Description
    Attempting to escalate to root privileges using setuid, setgid,
    and seteuid system calls from within the sandbox

    The sandbox should run as an unprivileged user with no capabilities,
    making all privilege escalation attempts fail with permission errors

"""

import os
import ctypes

results = {}

try:
    os.setuid(0)
    results["setuid(0)"] = "SUCCEEDED (CRITICAL)"
except PermissionError:
    results["setuid(0)"] = "blocked"

try:
    os.setgid(0)
    results["setgid(0)"] = "SUCCEEDED (CRITICAL)"
except PermissionError:
    results["setgid(0)"] = "blocked"

try:
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    ret = libc.seteuid(0)
    if ret == 0:
        results["seteuid(0)"] = "SUCCEEDED (CRITICAL)"
    else:
        results["seteuid(0)"] = f"blocked (errno={ctypes.get_errno()})"
except Exception as e:
    results["seteuid(0)"] = f"error: {e}"

results["uid"] = os.getuid()
results["gid"] = os.getgid()

for key, val in results.items():
    print(f"{key}: {val}")
