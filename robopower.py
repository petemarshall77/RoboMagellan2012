# Power processing for RoboMagellan2012
#
#    This module handles the power interfaces. As this is a quad steering
#    robot, steering commands will also be handled here
#
from robocomms import log
from roboutils import * 

# Initialize power controls
def initialize():
    log("Power initialization started")
    log("Power initialization completed")
    return True

# Steer the robot
#
#   Steer value is a integer from -10 (hard left) to +10 (hard right) with
#   0 meaning straight ahead. Steering is accomplished by driving the motors
#   at differing speeds. The mapping between the steer value and the physical
#   radius of turn is defined here
def steer(steer_value):
    assert(-10 <= steer_value <= 10)
    pass

# Set robot speed
#
#   Speed is defined as an integer between 0 (stopped) and 5 (full speed).
#   The mapping between the steer value and the physical speed is defined
#   here
def speed(speed_value):
    assert(0 <= speed_value <= 5)
    pass

# Stop the robot
def halt():
    """Stop the robot"""
    pass

# Stop the robot
def stop():
    """ Stop the robot """
    halt()
