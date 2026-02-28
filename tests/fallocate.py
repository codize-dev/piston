"""
Description
    Writing a large file to disk in the jobs directory, exhausting the
    space will temporarly disable other jobs to be started.

    The sandbox should reject the write with a "File too large" error

Discovered by
    Discord     Derpius#9144
"""

with open("beans","w") as f:
    n = 2**24
    f.write("I love beans\n"*n)