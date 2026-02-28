"""
Description
    Triggering a crash to generate a core dump file that might contain
    sensitive information from the process memory such as environment
    variables or runtime secrets

    The sandbox should prevent core dump generation via RLIMIT_CORE=0,
    ensuring no core files are written to disk

"""

import os
import ctypes
import ctypes.util
import resource

soft, hard = resource.getrlimit(resource.RLIMIT_CORE)
print(f"RLIMIT_CORE: soft={soft}, hard={hard}")

if hard > 0:
    print(f"WARNING: RLIMIT_CORE hard limit is {hard}, core dumps may be possible")

try:
    resource.setrlimit(resource.RLIMIT_CORE, (hard + 1, hard + 1))
    new_soft, new_hard = resource.getrlimit(resource.RLIMIT_CORE)
    print(f"RAISED RLIMIT_CORE to {new_hard} (CRITICAL)")
except (ValueError, resource.error):
    pass

try:
    with open("/proc/sys/kernel/core_pattern", "r") as f:
        pattern = f.read().strip()
        print(f"core_pattern: {pattern}")
except (PermissionError, FileNotFoundError):
    pass

secret = "SENSITIVE_DATA_LEAK_TEST_12345"

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
try:
    ctypes.string_at(0, 1)
except:
    pass

for path in ["/tmp/core", "/box/core", "core", f"/tmp/core.{os.getpid()}"]:
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"Core dump found at {path}, size={size} (CRITICAL)")
