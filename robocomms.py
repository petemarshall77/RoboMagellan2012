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

import threading, SocketServer, socket, time
import roboconfig
from roboutils import *

start_time = time.time()
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
            address = self.client_address
            time.sleep(1)  # Allow time for caller's server to start
            transmit_list.append(address)
            log("Comms_server: added %s to transmit list" % address[0])
        else:
            log("Comms_server: invalid data %s" % data)

#
# Class to run the server thread
#
class CommsThread(threading.Thread):

    # Run - create and serve the comms server
    def run(self):
        HOST = get_local_ipv4_address()
        PORT = roboconfig.comms_port
        self.comms_server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
        self.comms_server.serve_forever()

    # Stop - signal the socket server to terminate
    def stop(self):
        log("Terminating comms server")
        self.comms_server.shutdown()
        log("Comms server terminated")
#
# Communications initialization
#
def initialize():
    log("Comms server initialization started")
    comms_thread = CommsThread()
    comms_thread.start()
    log("Comms server initialization completed")
    return True

#
# Log messages
#
def log(message):
    log_time = time.time() - start_time
    for line in message.split('\n'):
        output = "%08.3f %s" % (log_time, line)
        print output
        broadcast(output)

#
# Broadcast data to each socket in client list
#
def broadcast(data):

    global transmit_list
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for address in transmit_list:
        sock.sendto(data, (address[0], roboconfig.monitor_port))
