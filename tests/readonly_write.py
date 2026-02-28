"""
Description
    Attempting to write files to read-only bind-mounted directories
    including /usr, /bin, /lib, and /etc

    The sandbox should enforce read-only mount restrictions, causing all
    write attempts to these paths to fail with filesystem or permission
    errors

"""

import os

readonly_paths = [
    "/usr/local/pwned",
    "/bin/pwned",
    "/lib/pwned",
    "/etc/pwned",
]

for path in readonly_paths:
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        continue
    try:
        with open(path, "w") as f:
            f.write("pwned")
        print(f"{path}: WRITE SUCCEEDED (CRITICAL)")
        os.unlink(path)
    except (PermissionError, OSError):
        pass
