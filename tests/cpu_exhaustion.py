"""
Description
    Pure CPU busy-loop with no I/O or sleep, designed to exhaust the
    CPU time limit enforced by the sandbox cgroup controller

    The sandbox should terminate the process once the CPU time limit
    is exceeded, returning a timeout status

"""

x = 0
while True:
    x = (x * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
