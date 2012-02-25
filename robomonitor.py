#!/usr/bin/python

# Remote monitoring for RoboMagellan 2012

#------------------------------------------------------------------------
# This is a standalone program that remotely monitors the robot by 
# displaying information sent by the robocomms.py module (which, in turn,
# is data written by the roboutils program.
#
# Top start monitoring, this program sends a UDP message to the server
# in robocomms with the identification string. The server adds the address
# of the machine running this program to its transmit list. Any data is then
# written as UDP packets to the addresses in that list.
#
# Once the initialization string is sent, this program sets up a UDP server
# to receive and print out the data. (Yes, this is a fairly minimalistic
# approach but it beats running around after the robot on the end of a
# usb tether!)
#-------------------------------------------------------------------------

import threading, SocketServer, socket, sys
import roboconfig
from roboutils import *

#
# UDP Server
#
class MyUDPHandler(SocketServer.BaseRequestHandler):

    # Handle incoming data
    def handle(self):
        data = self.request[0].strip()
        print data

#
# Main
#
def main():

    if len(sys.argv) < 2:
        print "Usage robomonitor.py <host>"
        exit

comms_hostname = sys.argv[1]
comms_port = roboconfig.comms_port

monitor_hostname = get_local_ipv4_address()
monitor_port = roboconfig.monitor_port

# Set us socket to send data
comms_host = socket.gethostbyname(comms_hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set up server to receive data
monitor_server = SocketServer.UDPServer((monitor_hostname, monitor_port), MyUDPHandler)

# Send the initialization token and then start the server
s.sendto("BaCoN", (comms_host, comms_port))
monitor_server.serve_forever()
