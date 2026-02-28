"""
Description
    Accessing external resources could be potentially dangerous

    The sandbox should block all outbound network access

"""

import urllib.request
contents = urllib.request.urlopen("https://emkc.org").read()