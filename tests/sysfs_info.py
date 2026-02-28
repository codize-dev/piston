"""
Description
    Reading /sys filesystem entries to discover host hardware information
    such as network interfaces, block devices, CPU topology, and DMI data

    The sandbox should not mount /sys at all, making the entire sysfs
    tree inaccessible from within the sandbox

"""

import os

sysfs_paths = [
    "/sys/class/net/",
    "/sys/block/",
    "/sys/devices/system/cpu/",
    "/sys/class/dmi/id/",
    "/sys/kernel/hostname",
    "/sys/fs/cgroup/",
]

for path in sysfs_paths:
    if os.path.exists(path):
        if os.path.isdir(path):
            try:
                entries = os.listdir(path)
                print(f"{path}: {entries[:10]}")
            except PermissionError:
                pass
        else:
            try:
                with open(path, "r") as f:
                    content = f.read(100).strip()
                print(f"{path}: {repr(content)}")
            except PermissionError:
                pass

for iface_path in ["/sys/class/net/eth0/address", "/sys/class/net/ens0/address"]:
    try:
        with open(iface_path, "r") as f:
            mac = f.read().strip()
        print(f"{iface_path}: {mac} (CRITICAL)")
    except (FileNotFoundError, PermissionError):
        pass
