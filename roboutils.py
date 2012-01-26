# Utility functions for RoboMagellan2012

# NOTE - everything in this module is imported (from roboutils import *), so
#        don't add anything here unless it truly is a shared utility function
#        or object. Let's keep that namespace clean, folks!

class RobotError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def log(message):
    print message
