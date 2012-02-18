#!/usr/bin/python

# Main control program
import sys,threading,traceback
import robocamera,robosensors,robopower,robocontrol,robonavigation,roboconfig
from   roboutils import *

#-------------------------------------------------------------------        
# Robot initialization
#
#   Parse the control file and then call the intialize() function
#   of each of the robot subsystems. If the subsystems run into problems
#   they will throw a RobotError which will be caught here to terminate
#   processing.
# 
#   If everything starts well, return the control data structure to
#   the main loop
#
def initialize():
    try:
        control_data = robocontrol.process_control_file(sys.argv[1])
        robopower.initialize()
        robocamera.initialize()
        robosensors.initialize()
        robonavigation.initialize()
    except RobotError as e:
        log("RobotException: " + e.value)
        log("Exception occurred in initialization - ending")
        robopower.halt()
        exit(0)
    return control_data

#-------------------------------------------------------------------------
# Main processing loop
#
#    Loop through each of the control data instructions, calling the 
#    appropriate function to handle the call
#
def mainloop(control_data):

    for command in control_data:
        log("Processing command: " + repr(command))

        if command['command'] == 'CONE':
            navigate_to(command['latitude'], command['longitude'], mode='cone')
        elif command['command'] == 'GOTO':
            navigate_to(command['latitude'], command['longitude'], mode='goto')
        elif command['command'] == 'DRIV':
            log("DRIV command not yet implemented")
        elif command['command'] == 'STOP':
            robopower.stop()
            return
        elif command['command'] == 'POWR':
            robopower.set_power(command['power'])
        elif command['command'] == 'STER':
            robopower.set_steering(command['steering'])
        elif command['command'] == 'WAIT':
            time.sleep(command['sleeptime'])
        else:
            # Should never happen: robocontrol should catch, but hey...
            log("Error in mainloop: invalid command " + command['command'])
            robopower.halt()
            raise RobotError

#-------------------------------------------------------------------------
# navigate_to()
#
#    Navigate to a given waypoint, optionally finding the cone that is
#    there.
#
#    Call this function with mode set to 'cone' (the default) or 'goto'.
#    If mode == 'goto', the function will terminate when the waypoint is
#    reached (within the GPS tolerance. If mode == 'cone' then camera-
#    based cone detection will be used to find the cone before the task
#    is completed.
#
def navigate_to(latitude, longitude, mode='cone'):
    assert (mode == 'cone') or (mode == 'goto')

    log("Navigate to lat: " + str(latitude) + ", lon: " + str(longitude))
    log("Navigate to mode=" + mode)

    task_complete = False
    while task_complete == False:  #TODO - probably need to time out
        
        # Get camera, compass heading, and GPS data
        (camera_X, camera_Y, camera_distance) = robocamera.get_data()
        current_heading = robosensors.get_compass()
        (gps_distance, heading_to_target) = \
                robonavigation.vector_to_target(latitude, longitude)
        
        # Test to see if we are at the GPS waypoint (within the radius of
        # error). We we are and we're in goto mode, we're done. Otherwise
        # switch to looking for the cone with the camera.
        if gps_distance < roboconfig.gps_radius:
            log("GPS waypoint found")
            if mode == 'goto':
                log("Goto mode - task complete")
                return
            else: 
                # If we can see the cone at this point, go and locate
                # it. If we can't, keep going until we can see it.
                # 
                # Note that locate_cone() may fail if the camera loses
                # sight of the cone. If that happens, we drop back to
                # locating the GPS waypoint again
                if camera_distance < roboconfig.max_camera_distance:
                    if locate_cone() == True:
                        return
                        
        # Outside of GPS range - set the steer angle and drive/turn 
        # towards the cone            
        steer_angle = \
            robonavigation.get_steer_angle(current_heading, heading_to_target)
        log("Navigate to: steer_angle = " + str(steer_angle))
        robopower.set_speed(5)
        robopower.set_steering(steer_angle)

#------------------------------------------------------------------------
# locate_cone()
#
#   Called when we are within GPS range of the waypoint and have already
#   seen some valid camera data.
# 
#   First we stop the robot and turn to center the cone. Then we drive
#   towards the cone until the touch sensors show we've made contact.
#
#   If we lose sight of the cone for whatever reason, we'll try to re-
#   sight it. If that fails, we return and go back to GPS waypoint 
#   finding in the calling routine.
def locate_cone():

    # First stop the robot
    robopower.speed(0)
    
    # Now drive slowly towards the cone
    while True:
        (camera_X, camera_Y, camera_distance) = robocamera.get_data()

        # If we lose sight of the cone try and find it again
        if camera_distance > roboconfig.max_camera_distance:
            if re_sight_cone() == False:
                return False   # failed to re-sight: go back to GPS
            else:
                continue
        
        # Steer toward the cone     
        robopower.steer(int(camera_X/32.0-10.0))
        robopower.speed(1)
        
        # Check the touch sensor
        if robosensors.touch_down():
            return True

#--------------------------------------------------------------------------
# re_sight_cone()
#
#   Called when the camera loses sight of the cone. Try a number of times
#   to find it again.
def re_sight_cone():
    
    log("Re-sighting cone...")

    # Try a few times
    for i in range(roboconfig.re_sight_attempts):
        (camera_X, camera_Y, camera_distance) = robocamera.get_data()
        if camera_distance < roboconfig.max_camera_distance:
            log("...sucess!")
            return True
        else:
            time.sleep(re_sight_sleep_time)
        
    # Couldn't find it - return False        
    log("...failed")        
    return False

#-----------------------------------------------------------------------
# Main
#
#    Call initialize to start the robot. Initialize will return the
#    control file data structure if all is well. Pass this to the 
#    mainloop() funtion to carry out each control function.
#
#    Note: initialize will terminate with a RobotError exception if
#    problems occur: no need to check returned value.
#
def main():
    log("RoboMagellan 2012 started")
    control_data = initialize()
    time.sleep(1)  # Allow time for processing threads to start
    try:
        mainloop(control_data)
    except:
        log("*** ERROR *** A fatal error has occured *** ERROR ***")
        log(str(traceback.format_exc()))
    else:
        log("RoboMagellan 2012 ended - Champagne Time!")

    # Stop the robot
    robopower.halt()
    
    # Terminate running threads
    for thread in threading.enumerate()[1:]:
        log("Terminating thread: " + str(thread))
        thread.stop()

if __name__ == '__main__':
    main()

