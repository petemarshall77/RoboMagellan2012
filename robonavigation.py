# Navigation processing for RoboMagellan2012

import threading,serial
from robocomms import *
from roboutils import * 
from math import sin, cos, atan2, radians, degrees, sqrt

earth_radius = 6371000.0    # meters
global gps_latitude, gps_longitude

#----------------------------------------------------------------------------
# GPS Processing Thread
#----------------------------------------------------------------------------
class GpsThread(threading.Thread):
    
    ser = serial.Serial(roboconfig.gps_serial_port-1, \
                            roboconfig.gps_serial_baud, \
                            timeout = roboconfig.gps_serial_timeout)
    run_flag = True

    # Get the GPS data
    def run(self):
        while self.run_flag == True:
            self.ser.flushInput() # Discard any buffered readings
            self.ser.readline()   # Force the next read to be a full line
            data = self.ser.readline()
            if data == "":
                log("Warning: no GPS data recived")
            else:
                log("GPS data: %s" % data)
        log("GPS thread terminated")

    # Stop the thread
    def stop(self):
        log("Terminating GPS Thread")
        self.run_flag = False


def initialize():
    log("Navigation initialization started")
    gps_thread = GpsThread()
    gps_thread.start()
    log("Navigation initialization completed")
    return True

# vector_to_target(latitude, longitude)
#
#   Latitude and longitude are the target we are seeking. Return the
#   distance and bearing from the current GPS location to the target.
#
def vector_to_target(latitude, longitude):

    (gps_lat, gps_lon) = get_gps_coordinates()
    return vector_between(gps_lat, gps_lon, latitude, longitude)

# vector_between(lat1, lon1, lat2, lon2)
#  
#   Return the distance and (initial) bearing from the point at
#   (lat1, lon1) to the point at (lat2, lon2).
# 
def vector_between(lat1, lon1, lat2, lon2):

    # Convert to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Calculate distance to target using Haversine formula
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = sin(delta_lat/2.0) * sin(delta_lat/2.0) + \
        sin(delta_lon/2.0) * sin(delta_lon/2.0) * \
        cos(lat1) * cos(lat2)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    distance = earth_radius * c

    # Calculate the (great circle!!!) bearing
    y = sin(delta_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - \
        sin(lat1) * cos(lat2) * cos(delta_lon)
    bearing = (degrees(atan2(y,x)) + 360) % 360

    return(distance, bearing)

# get_steer_angle(vehicle_angle, target_angle)
#
#   Vehicle_angle is the robot heading relative to north.
#   Target angle is the heading from the robot to the target,
#   relative to north.
#   This function returns the angle to steer to align the robot
#   to the target. This angle should be in the range -180 < x < +180
#
def get_steer_angle(vehicle_angle, target_angle):

    target_value = target_angle - vehicle_angle
    if abs(target_value) > 180.0:
        if target_value < 0.0:
            target_value = target_value + 360
        else:
            target_value = target_value - 360

    return target_value
        
def get_gps_coordinates():

    return(118.0, 33.00)
