#!/usr/bin/python

# Main control program

import robocamera
import robosensors
import robopower
from roboutils import *

        
# Robot initialization
def initialize():
    try:
        robopower.initialize()
        robocamera.initialize()
        robosensors.initialize()
        robonavigation.initialize()
    except RobotError as e:
        log("RobotException: " + e.value)
        log("Exception occurred in initialization - ending")
        robopower.halt()
        exit(0)

# Main processing loop
def mainloop():
    mode = "GPS"
    while mode != "STOP":
        pass

# Processing starts here
log("RoboMagellan 2012 started")
initialize()
mainloop()
log("RoboMagellan 2012 ended - Champagne Time!")
