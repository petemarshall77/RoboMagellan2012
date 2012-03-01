# Camera processing for RoboMagellan2012

#------------------------------------------------------------------------
# Camera processing in RoboMagellan2012 is done through an external
# program: RoboRealm. RoboRealm is configured to send data to this
# module via UDP.
#
# To handle the RoboRealm data, this module starts a thread
# to handle the incoming requests. The data is received, processed
# and the camera data fields are updated. The main control process
# then reads these data asynchronously.
#------------------------------------------------------------------------

import threading,re,math,time
import roboconfig
import SocketServer
from math import log
from robocomms import log
from roboutils import * 

camera_distance = 0.0
camera_x = 0
camera_y = 0
camera_time = time.time()

#
# Camera server - receives data from RoboRealm
#
class MyUDPHandler(SocketServer.BaseRequestHandler):
    
    # Handle incoming data
    def handle(self):
        global camera_x, camera_y, camera_distance, camera_time
        data = self.request[0].strip()
#        socket = self.request[1]
#        socket.sendto(data.upper(), self.client_address)
        camera_regex = re.compile("(\d+);(\d+);(\d+);(\d+)")
        match = camera_regex.search(data)
        if not match:
            log("Invalid camera data: %s" % data)
            return

        cogb = match.group(1)
        dist = match.group(2)
        xval = match.group(3)
        yval = match.group(4)

        # TODO - add value filtering here

        camera_x = int(xval)
        camera_y = int(yval)
        camera_distance = (1/.746) * (math.log(float(cogb)/314.0))
        camera_time = time.time()

 
#
# Thread to run the camera server
#
class CameraThread(threading.Thread):

    # Run - create a UDP socket server
    def run(self):
        HOST = roboconfig.camera_host
        PORT = roboconfig.camera_port
        log("Starting camera server on " + str(HOST) + ":" + str(PORT)) 
        self.camera_server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
        self.camera_server.serve_forever() 

    # Stop - shutdown the socket server, serve_forever will complete    
    def stop(self):
        log("Terminating camera server")
        self.camera_server.shutdown()
        log("Camera server terminated")
        
#
# Camera initialization
#
def initialize():
    log("Camera initialization started")
    camera_thread = CameraThread()
    camera_thread.start()
    log("Camera initialization completed")
    return True

# get_data() - return the camera data
#
#    get the data from the camera and return the X, Y and distance values
#    X and Y are (integer) pixel offsets from the center of the frame.
#    Distance is in meters.
def get_data():
    if (time.time() - camera_time) > roboconfig.camera_timeout:
        log("WARNING: no camera data received for %d seconds" % \
                (time.time()-camera_time))
    return (camera_x, camera_y, camera_distance)
