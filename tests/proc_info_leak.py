"""
Description
    Reading /proc entries to check if host process information or
    sensitive kernel data is exposed through the procfs interface

    The sandbox should isolate /proc with hidepid=2 and PID namespace,
    preventing access to host process information

"""

import os

# Try to list processes visible in /proc
pids = [d for d in os.listdir("/proc") if d.isdigit()]
print(f"Visible PIDs: {pids}")

# Try to read PID 1's info (outside PID namespace, this would be host init)
sensitive_paths = [
    "/proc/1/cmdline",
    "/proc/1/environ",
    "/proc/1/maps",
]

for path in sensitive_paths:
    try:
        with open(path, "r") as f:
            content = f.read(100)
        print(f"{path}: {repr(content[:50])}")
    except (PermissionError, FileNotFoundError, ProcessLookupError):
        pass
