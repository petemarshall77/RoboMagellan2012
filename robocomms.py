# Remote communications for RoboMagellan 2012

#-------------------------------------------------------------------------
# This module provides the ability to remotely monitor the robot activity
# by enabling messages written by roboutils.log() to be sent over a 
# network (wireless, presumably!) to an external computer.
#
# The external computer runs the program robomonitor.py which works in
# conjunction with this program to achieve remote monitoring.
#
# NOTE: all communications are UDP based for simplicity's sake.
#
# This program consists of two parts. First is a UDP server that waits
# for incoming requests from robomonitor.py. On receiving a request
# (simply a packet with a simple identification token in it) it adds the
# client's ip address to a transmit list.
#
# The second part of the program is a routine called by roboutils.log()
# which takes the log data and and writes it to each ip address in the
# transmit list. The receiver - robomonitor.py - will establish it's 
# own UDP server to recieve the data.
#-------------------------------------------------------------------------

import threading, SocketServer, socket
import roboconfig
from roboutils import *

transmit_list = []

#
# UDP Server
#
class MyUDPHandler(SocketServer.BaseRequestHandler):

    # Handle incoming data
    def handle(self):
        global transmit_list
        data = self.request[0].strip()
        
        # Add to transmit list if identifier token is correct
        if data == "BaCoN":
            host = socket.gethostbyname(self.client_address[0])
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            time.sleep(1)  # Allow time for callers server to start
            log("Comms_server: added %s to transmit list" % self.client_address[0])
            transmit_list.append((s, host))

        print data


#
# Class to run the server thread
#
class CommsThread(threading.Thread):

    # Run - create and serve the comms server
    def run(self):
        HOST = roboconfig.comms_host
        PORT = roboconfig.comms_port
        self.comms_server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
        self.comms_server.serve_forever()

    # Stop - signal the socket server to terminate
    def stop(self):
        log("Terminating comms server")
        self.comms_server.shutdown()

#
# Communications initialization
#
def initialize():
    log("Comms server initialization started")
    comms_thread = CommsThread()
    comms_thread.start()
    log("Comms server initialization completed")
    return True
