#!/usr/bin/python

# Roboslave - run the robot in remotely-controlled slave mode
import sys,threading,traceback,time, SocketServer
import robocamera,robosensors,robopower,robonavigation,roboconfig
import robocomms
from   robocomms import log
from   roboutils import *

#-------------------------------------------------------------------
# Log the robot status
#-------------------------------------------------------------------
def log_robot_status():
    ping = robosensors.get_sensors()
    touch_sensor = robosensors.get_bumper()
    log(">> Speed=%d" % robopower.get_power())
    log(">> Compass=%3.2f" % robosensors.get_compass())
    log(">> Touch=%s, Ping1=%d, Ping2=%d, Ping3=%d" % \
            (touch_sensor, ping[0], ping[1], ping[2]))

#-------------------------------------------------------------------        
# Robot initialization
#
#   Call the intialize() function on each of the robot subsystems. If
#   the subsystems run into problems they will throw a RobotError which
#   will be caught here to terminate processing.
# 
def initialize():
    try:
        robocomms.initialize()
        robopower.initialize()
        robocamera.initialize()
        robosensors.initialize()
        robonavigation.initialize()
    except RobotError as e:
        log("RobotException: " + e.value)
        log("Exception occurred in initialization - ending")
        robopower.halt()
        exit(0)
    return
#-------------------------------------------------------------------------
# Process the received command
#-------------------------------------------------------------------------
def process_command(command):

    # Ignore blank lines
    if command == "":
        return

    # Speed command
    if command[0:5].lower() == 'speed':
        speed_re = re.compile('speed\s+([+|-]*)(\d+)')
        match = speed_re.search(command)
        if not match:
            log("Invalid speed command, usage is: speed <integer>")
            return
        speed = int("%s%s" % (match.group(1), match.group(2)))
        if speed < -16 or speed > 16:
            log("Invalid speed: must be -16 <= speed <= 16")
            return
        robopower.speed(speed)
        log("Speed set to %d" % speed)
        return
    
    # Stop command
    if command[0:4].lower() == 'stop':
        robopower.stop()
        log("Robot stopped")
        return
    
    # No match - must be an invalid command
    log("Invalid command: %s" % command)

#-------------------------------------------------------------------------
# UDP Server
#-------------------------------------------------------------------------
class MyUDPHandler(SocketServer.BaseRequestHandler):

    # Handle incoming data
    def handle(self):
        data = self.request[0].strip()
        process_command(data)
        log_robot_status()

#-------------------------------------------------------------------------
# Main processing loop
#
# Start the UDP server. This server will handle incoming commands.
#-------------------------------------------------------------------------
def mainloop():
    
    log("Starting command server")
    HOST = get_local_ipv4_address()
    PORT = roboconfig.command_port
    command_server = SocketServer.UDPServer((HOST,PORT),MyUDPHandler)
    command_server.serve_forever()

#-----------------------------------------------------------------------
# Main
#
#    Call initialize to start the robot. Then call mainloop() inside a
#    try statement - if error occur, catch the exception and stop the
#    robot before terminating the program.
#
#    On exiting (cleanly or otherwise) terminate all threads that were
#    created at initialization time.
#
def main():
    log("RoboMagellan 2012 started")
    initialize()
    time.sleep(1)  # Allow time for processing threads to start
    try:
        mainloop()
    except:
        log("*** ERROR *** A fatal error has occured *** ERROR ***")
        log(str(traceback.format_exc()))
    else:
        log("RoboMagellan 2012 ended - Champagne Time!")

    # Stop the robot
    robopower.halt()
    
    # Terminate running threads
    for thread in threading.enumerate():
        if thread.name != 'MainThread':
            log("Terminating thread: " + str(thread))
            thread.stop()

if __name__ == '__main__':
    main()

