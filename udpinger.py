#!/usr/bin/python

# udpinger.py <host> <port> send data as udp packets

import socket,sys

if len(sys.argv) < 3:
    print "Usage udpinger.py <host> <port>"
    exit

hostname = sys.argv[1]
port = int(sys.argv[2])

host = socket.gethostbyname(hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = raw_input()
    s.sendto(data, (host,port))
    
