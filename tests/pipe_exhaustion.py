"""
Description
    Creating a massive number of pipes and filling their buffers to
    exhaust kernel memory allocated for pipe buffers

    The sandbox should enforce RLIMIT_NOFILE to limit the number of
    pipes, and the memory cgroup should prevent kernel buffer
    exhaustion from affecting the host

"""

import os

pipes = []
i = 0
while True:
    try:
        r, w = os.pipe()
        pipes.append((r, w))
        i += 1
        try:
            os.write(w, b'x' * 65536)
        except:
            pass
    except OSError:
        break

print(f"Created {i} pipes before hitting limit")

for r, w in pipes:
    try:
        os.close(r)
        os.close(w)
    except:
        pass
