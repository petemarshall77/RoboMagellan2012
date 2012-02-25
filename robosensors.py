# Sensor processing for RoboMagellan2012

from robocomms import log
from roboutils import * 

def initialize():
    log("Sensor initialization started")
    log("Sensor initialization completed")
    return True

# get_compass() - get the compass data
#
#    Returns the compass heading - based on true (not magnetic) north -
#    as an integer between 0 and 359, where 0 is north, 90 is east, 180
#    is south, and 270 is west
def get_compass():
    return 90

# touch_down() - return True if the touch sensor is activated
def touch_down():
    return True
