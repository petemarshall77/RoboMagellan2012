# Power processing for RoboMagellan2012
#
#    This module handles the power interfaces. As this is a quad steering
#    robot, steering commands will also be handled here
#
import time,threading
import roboconfig
from robocomms import log
from roboutils import * 

# Speed values
target_speed = 0
current_speed = 0

#
# Power control thread
#
# This thread is started by initialize. It runs continuously, checking 
# for a match between target_speed and current_speed. If they differ, it
# will send control commands to speed up or slow down the robot in a
# smooth fashion.
# 
# Example: if the current speed is 6 and the target speed it 11, this
# code will send the power controller a series of updates: 7,8,9,10,11
# with time delays between them.
#
# Note on speed values:
#      
#      The power controlling Arduino uses a speed value from 1 (fast)
#      to 16 (slow) with separate flags for reversing and braking.
#      For control purposes we use use -16 to 16. These will get 
#      translated into the appropriate commands here.
#
#      There are two motors in the robot, one of which runs in the
#      opposite direction to the other. Any speed change requires
#      sending two commands, one with the reverse flag set.
#
class PowerThread(threading.Thread):

    run_flag = True

    def run(self):
        while self.run_flag:
            global current_speed, target_speed
            
            if current_speed != target_speed:
                if current_speed < target_speed:
                    values = range(current_speed+1, target_speed+1)
                else:
                    values = range(current_speed-1, target_speed-1, -1)
                for k in values:
                    log("Setting speed to %d" % k)
                    current_speed = target_speed
                    time.sleep(roboconfig.power_delay)

            time.sleep(roboconfig.power_delay)

        log("Power thread terminated")    

    def stop(self):
        log("Terminating power thread")
        self.run_flag = False

# Initialize power controls
def initialize():
    log("Power initialization started")
    power_thread = PowerThread()
    power_thread.start()
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
#   Speed is defined as an integer between -16 (full reverse) and +16 (full
#   ahead. 
def speed(speed_value):
    assert(-16 <= speed_value <= 16)
    global target_speed
    log("Old target speed = %d" % target_speed)
    target_speed = speed_value
    log("New target speed = %d" % target_speed)

# Stop the robot
def halt():
    """Stop the robot"""
    speed(0)
    pass

# Stop the robot - same as halt()
def stop():
    """ Stop the robot """
    halt()
