"""
Description
    Enumerating all environment variables visible inside the sandbox to
    check whether host environment variables are unintentionally leaked

    The sandbox should only expose explicitly configured environment
    variables, with no host-origin secrets or credentials present

"""

import os

env = dict(os.environ)
print(f"Total env vars: {len(env)}")
for key in sorted(env.keys()):
    print(f"{key}={env[key]}")
