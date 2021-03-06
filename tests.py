#!/bin/python3
"""requestspool simple tests"""

from itertools import product
from pprint import pprint

from requestspool import RequestsPool

URLS = ("https://pypi.org/", "https://git.io", "https://gentoo.org")


print("map() 2 processes test:")

def get_url(url, session):
    return session, session.get(url)

with RequestsPool(2) as rp:
    RESULTS = rp.map(get_url, URLS, flatten=False)
    pprint(RESULTS)

# Ensure every process had their own unique session.
SESSIONS = (RESULTS[proc][0] for proc in range(len(RESULTS)))
assert len(set(SESSIONS)) == 2


print("\nstarmap() 3 processes test:")

def get_url_timeout(url, timeout, session):
    return session, session.get(url, timeout=timeout)

with RequestsPool(3) as rp:
    RESULTS = rp.starmap(get_url_timeout, product(URLS, (6,)), flatten=False)
    pprint(RESULTS)

SESSIONS = (RESULTS[proc][0] for proc in range(len(RESULTS)))
assert len(set(SESSIONS)) == 3
