"""
Description
    Unbounded memory allocation to exhaust available RAM and potentially
    trigger an OOM condition on the host system

    The sandbox should terminate the process before host memory is exhausted,
    either via a memory cgroup limit or a wall-time/CPU-time timeout

"""

import sys

chunks = []
while True:
    chunks.append(b'x' * (1024 * 1024))  # Allocate 1 MB at a time
