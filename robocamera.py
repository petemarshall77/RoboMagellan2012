# Camera processing for RoboMagellan2012

from roboutils import * 

def initialize():
    log("Camera initialization started")
    log("Camera initialization completed")
    return True

# get_data() - return the camera data
#
#    get the data from the camera and return the X, Y and distance values
#    X and Y are (integer) pixel offsets from the center of the frame.
#    Distance is in meters.
def get_data():
    return (0, 0, 1.0)
