"""
Description
    Sending signals to processes outside the sandbox by targeting PID 1
    and other process IDs, attempting to disrupt the sandbox keeper or
    other system processes

    The sandbox should confine signal delivery within the PID namespace,
    making it impossible to signal processes outside the namespace

"""

import os
import signal

targets = [
    (1, signal.SIGTERM, "PID 1 (namespace init)"),
    (1, signal.SIGKILL, "PID 1 (namespace init)"),
    (2, signal.SIGKILL, "PID 2"),
]

for pid, sig, desc in targets:
    if pid == os.getpid():
        continue
    try:
        os.kill(pid, sig)
        print(f"Signal {sig} to {desc}: DELIVERED")
    except ProcessLookupError:
        pass
    except PermissionError:
        pass
    except OSError:
        pass

for pid in [1000, 2000, 5000, 10000, 32000]:
    try:
        os.kill(pid, 0)
        print(f"PID {pid} EXISTS inside namespace")
    except ProcessLookupError:
        pass
    except PermissionError:
        print(f"PID {pid} exists but permission denied")
    except OSError:
        pass
