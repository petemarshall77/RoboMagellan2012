# Navigation processing for RoboMagellan2012

from roboutils import * 
from math import sin, cos, atan2, radians, degrees, sqrt

earth_radius = 6371000.0    # meters

def initialize():
    log("Navigation initialization started")
    log("Navigation initialization completed")
    return True

# vector_to_target(latitude, longitude)
#
#   Latitude and longitude are the target we are seeking. This
#   function gets the latest GPS data and, using that, calculates the
#   distance and angle to the given target from the current position
#
def vector_to_target(latitude, longitude):

    print latitude, longitude
    (gps_lat, gps_lon) = get_gps_coordinates()

    # Convert to radians
    latitude = radians(latitude)
    longitude = radians(longitude)
    gps_lat = radians(gps_lat)
    gps_lon = radians(gps_lon)

    # Calculate distance to target using Haversine formula
    delta_lat = latitude - gps_lat
    delta_lon = longitude - gps_lon
    a = sin(delta_lat/2.0) * sin(delta_lat/2.0) + \
        sin(delta_lon/2.0) * sin(delta_lon/2.0) * \
        cos(gps_lat) * cos(latitude)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    distance = earth_radius * c

    # Calculate the (great circle!!!) bearing
    y = sin(delta_lon) * cos(latitude)
    x = cos(gps_lat) * sin(latitude) - \
        sin(gps_lat) * cos(latitude) * cos(delta_lon)
    bearing = degrees(atan2(y,x))                                              
    print distance, bearing

    return(1.0, 90)

def get_gps_coordinates():

    return(118.4191, 33.77881667)
