"""
Description
    Creating a large number of small files to exhaust filesystem inodes
    on the shared tmpfs, potentially denying service to other jobs

    The sandbox should terminate the process via timeout or filesystem
    quota before inode exhaustion can affect the host system

"""

import os

i = 0
while True:
    try:
        with open(f"/tmp/f{i}", "w") as f:
            f.write("x")
        i += 1
    except OSError:
        print(f"Stopped at {i} files")
        break
