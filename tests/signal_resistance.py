"""
Description
    Installing handlers to catch or ignore all catchable signals in an
    attempt to resist being killed by the sandbox timeout mechanism

    The sandbox should still terminate the process when the wall-time
    or CPU-time limit is exceeded, as the keeper process delivers SIGKILL
    which cannot be caught or ignored

"""

import signal

catchable = [
    signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM,
    signal.SIGALRM, signal.SIGUSR1, signal.SIGUSR2, signal.SIGPIPE,
    signal.SIGABRT,
]

for sig in catchable:
    try:
        signal.signal(sig, signal.SIG_IGN)
    except (OSError, ValueError):
        pass

x = 0
while True:
    x += 1
