"""
Description
    Creating raw and packet sockets for network packet capture or
    injection, which could be used for network sniffing or spoofing

    The sandbox should prevent raw socket creation both by network
    namespace isolation and by lacking CAP_NET_RAW capability

"""

import socket

socket_types = [
    ("AF_INET RAW ICMP", socket.AF_INET, socket.SOCK_RAW, 1),
    ("AF_INET RAW TCP", socket.AF_INET, socket.SOCK_RAW, 6),
    ("AF_INET6 RAW ICMPv6", socket.AF_INET6, socket.SOCK_RAW, 58),
]

for desc, family, stype, proto in socket_types:
    try:
        s = socket.socket(family, stype, proto)
        print(f"{desc}: CREATED (CRITICAL)")
        s.close()
    except PermissionError:
        pass
    except OSError:
        pass

try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    print("AF_PACKET RAW: CREATED (CRITICAL)")
    s.close()
except PermissionError:
    pass
except OSError:
    pass

try:
    NETLINK_KOBJECT_UEVENT = 15
    s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_KOBJECT_UEVENT)
    print("AF_NETLINK KOBJECT_UEVENT: CREATED")
    s.close()
except PermissionError:
    pass
except OSError:
    pass
