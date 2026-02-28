"""
Description
    Attempting to open raw hardware devices including disk, memory, and
    kernel message devices that are bind-mounted from the host

    The sandbox should prevent access to hardware device files by running
    as an unprivileged user without the necessary capabilities to open
    raw devices

"""

import os

devices = [
    "/dev/sda",
    "/dev/mem",
    "/dev/kmsg",
    "/dev/port",
]

for dev in devices:
    if not os.path.exists(dev):
        continue
    try:
        fd = os.open(dev, os.O_RDONLY)
        data = os.read(fd, 16)
        os.close(fd)
        print(f"{dev}: READ SUCCEEDED - {repr(data)} (CRITICAL)")
    except PermissionError:
        pass
    except OSError:
        pass
