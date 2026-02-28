"""
Description
    Files created in /dev/mqueue persist across sandbox runs,
    potentially allowing information leakage and disk space exhaustion

    Run this test twice and there should be no output

"""

import os
import subprocess

fpath = "/dev/mqueue/bean"

if os.path.exists(fpath):
    print(f"{fpath} exists")
else:
    subprocess.run(["touch", fpath])
