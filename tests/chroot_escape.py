"""
Description
    Using the classic double-chroot escape technique: create a new chroot,
    then chdir to the original root via relative path traversal to break
    out of the sandbox chroot

    The sandbox should prevent chroot by running as an unprivileged user
    without CAP_SYS_CHROOT capability

"""

import ctypes
import ctypes.util
import os

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

try:
    os.makedirs("/tmp/escape", exist_ok=True)
except OSError:
    pass

ret = libc.chroot(b"/tmp/escape")
if ret == 0:
    try:
        os.chdir("/" + "../" * 20)
        ret2 = libc.chroot(b".")
        if ret2 == 0:
            try:
                entries = os.listdir("/")
                if "etc" in entries and "home" in entries:
                    print(f"CHROOT ESCAPED - see real root: {entries[:10]} (CRITICAL)")
            except:
                pass
    except:
        pass
