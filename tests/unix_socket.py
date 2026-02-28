"""
Description
    Creating a Unix domain socket file in writable directories to attempt
    cross-sandbox communication between different job instances

    The sandbox should isolate writable directories per sandbox instance,
    preventing any cross-sandbox communication via Unix domain sockets

"""

import socket
import os

paths = [
    "/tmp/exploit.sock",
    "/dev/shm/exploit.sock",
]

for sock_path in paths:
    try:
        if os.path.exists(sock_path):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(sock_path)
            print(f"CONNECTED to existing socket at {sock_path} (CRITICAL)")
            client.close()
        else:
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(sock_path)
            server.listen(1)
            print(f"LISTENING on {sock_path}")
            server.close()
    except (OSError, ConnectionRefusedError):
        pass

# Also try abstract namespace sockets (not filesystem-bound)
try:
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind("\0exploit_abstract")
    server.listen(1)
    print("LISTENING on abstract namespace socket")
    server.close()
except OSError:
    pass
