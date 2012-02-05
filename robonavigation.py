# Navigation processing for RoboMagellan2012

from roboutils import * 

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
    return(1.0, 90)
