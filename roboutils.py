# Utility functions for RoboMagellan2012

# NOTE - everything in this module is imported (from roboutils import *), so
#        don't add anything here unless it truly is a shared utility function
#        or object. Let's keep that namespace clean, folks!
import commands,re,os,socket

# Get the IPv4 address of the current computer
def get_local_ipv4_address():
    
    if os.name == 'posix':
        output = commands.getoutput("/sbin/ifconfig | grep inet | grep -v inet6 | grep -v 127.0.0.1")
        ip_re = re.compile('inet addr:(\S+)')
        m = ip_re.search(output)
        if m:
            return m.group(1)
        else:
            return 'localhost'

    elif os.name == 'nt':
        return(socket.gethostbyname(socket.gethostname()))

class RobotError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

