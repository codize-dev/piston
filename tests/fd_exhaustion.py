"""
Description
    Opening the maximum number of file descriptors to exhaust the
    per-process fd table, potentially causing denial of service for
    the sandbox infrastructure that needs fds to function

    The sandbox should enforce RLIMIT_NOFILE to cap the number of
    open file descriptors per process

"""

import os

fds = []
i = 0
while True:
    try:
        fd = os.open("/dev/null", os.O_RDONLY)
        fds.append(fd)
        i += 1
    except OSError:
        break

print(f"Opened {i} file descriptors before hitting limit")

if i > 10000:
    print(f"WARNING: Opened {i} fds, limit may be too high")

for fd in fds:
    try:
        os.close(fd)
    except:
        pass
