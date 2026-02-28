"""
Description
    Attempting to raise resource limits using Python's resource module to
    bypass the rlimits set by the sandbox, such as increasing the maximum
    process count or file size limit beyond the configured hard limits

    The sandbox should prevent raising resource limits beyond the hard
    limits configured by isolate, as the process has no CAP_SYS_RESOURCE
    capability

"""

import resource

limits_to_try = [
    ("RLIMIT_NPROC", resource.RLIMIT_NPROC),
    ("RLIMIT_FSIZE", resource.RLIMIT_FSIZE),
    ("RLIMIT_NOFILE", resource.RLIMIT_NOFILE),
]

for name, res in limits_to_try:
    soft, hard = resource.getrlimit(res)
    print(f"{name}: soft={soft}, hard={hard}")
    try:
        resource.setrlimit(res, (hard + 1, hard + 1))
        new_soft, new_hard = resource.getrlimit(res)
        print(f"  RAISED to soft={new_soft}, hard={new_hard} (CRITICAL)")
    except (ValueError, resource.error):
        pass
