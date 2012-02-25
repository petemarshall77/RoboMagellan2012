#!/usr/bin/python

#----------------------------------------------------------------------
# robocommander.py <host> send commands to a robot running roboslave
#
# Note: this program does not recieve data back from the robot. Use
# robomonitor.py to do that
#----------------------------------------------------------------------
import socket,sys
import roboconfig

# Check valid command line: i.e. host specified
if len(sys.argv) < 2:
    print "Usage robocommander.py <host>"
    exit

hostname = sys.argv[1]
port = roboconfig.command_port

host = socket.gethostbyname(hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = raw_input()
    s.sendto(data, (host,port))
    
