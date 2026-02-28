"""
Description
    Infinite loop printing to stderr to exhaust memory and disk via
    error output capture, mirroring the stdout flood attack via stderr

    The sandbox should kill the process once stderr output exceeds the
    allowed limit

"""

import sys

while True:
    print("Piston is secure", file=sys.stderr)
