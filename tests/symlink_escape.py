"""
Description
    Creating a symlink inside the sandbox pointing to sensitive host paths,
    attempting to read files outside the chroot boundary through the symlink

    The sandbox should confine all path resolution within the chroot, so
    symlinks to absolute paths resolve within the sandbox rather than
    on the host filesystem

"""

import os

targets = [
    ("/tmp/etc_shadow", "/etc/shadow"),
    ("/tmp/root_dir", "/root/.bashrc"),
    ("/tmp/host_proc", "/proc/1/environ"),
]

for link_path, target in targets:
    try:
        os.symlink(target, link_path)
        with open(link_path, "r") as f:
            content = f.read(100)
        print(f"Read via {link_path} -> {target}: {repr(content[:50])}")
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    except Exception as e:
        pass
