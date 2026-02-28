"""
Description
    Using the mount syscall to attempt mounting filesystems such as proc,
    sysfs, or bind mounts to access data outside the chroot boundary

    The sandbox should prevent mount operations by running as an
    unprivileged user without CAP_SYS_ADMIN capability

"""

import ctypes
import ctypes.util
import os

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

try:
    os.makedirs("/tmp/mnt", exist_ok=True)
except OSError:
    pass

mount_attempts = [
    (b"none", b"/tmp/mnt", b"proc", 0, b"", "mount proc"),
    (b"none", b"/tmp/mnt", b"sysfs", 0, b"", "mount sysfs"),
    (b"none", b"/tmp/mnt", b"tmpfs", 0, b"", "mount tmpfs"),
    (b"/", b"/tmp/mnt", b"none", 4096, b"", "bind mount /"),
]

for source, target, fstype, flags, data, desc in mount_attempts:
    ret = libc.mount(source, target, fstype, flags, data)
    if ret == 0:
        print(f"{desc}: SUCCEEDED (CRITICAL)")
        try:
            entries = os.listdir("/tmp/mnt")
            print(f"  Contents: {entries[:5]}")
        except:
            pass
        libc.umount(target)
