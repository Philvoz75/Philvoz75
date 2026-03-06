#!/usr/bin/env python
from http.client import responses

import requests
import re
url = "10.0.2.5/mutillidae/"
def request(url):
    try:
        rep = requests.get("http://" + url)
        return rep
    except requests.exceptions.ConnectionError:

        pass
    except requests.exceptions.InvalidURL:
        pass
with open("files-and-dirs-wordlist.txt", "r") as worldlist_file:
    for line in worldlist_file:
        world = line.strip()
        # test_url = world + "." +url
        test_url = url + "/" + world
        responses = request(test_url)
        if responses:
            print("[+] Discover subdomains -->" + test_url)
        else:
            pass
