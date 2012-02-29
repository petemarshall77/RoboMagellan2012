# Sensor processing for RoboMagellan2012

import threading,serial,re,time
import roboconfig
from robocomms import log
from roboutils import * 

# Sensor values
compass_value = 999

# Compass communication thread
class CompassThread(threading.Thread):

    ser = serial.Serial(roboconfig.compass_serial_port-1, \
                            roboconfig.compass_serial_baud)
    compass_re = re.compile('(\d+)\.(\d)')
    run_flag = True

    # Get the compass data
    def run(self):
        while self.run_flag == True:
            global compass_data
            self.ser.flushInput() # Discard readings buffered during sleep
            data = self.ser.readline()
            m = self.compass_re.match(data)
            if m:
                compass_data = int(m.group(1)) + 0.1 * int(m.group(2))
            else:
                log("robosensors - recieved invalid compass data: %s" % data)
            time.sleep(roboconfig.compass_read_delay)
    
    # Stop the thread
    def stop(self):
        self.run_flag = False

def initialize():
    log("Sensor initialization started")
    compass_thread = CompassThread()
    compass_thread.start()
    log("Sensor initialization completed")
    return True

# get_compass() - get the compass data
#
#    Returns the compass heading - based on true (not magnetic) north -
#    as an integer between 0 and 359, where 0 is north, 90 is east, 180
#    is south, and 270 is west
def get_compass():
    global compass_data
    return compass_data

# touch_down() - return True if the touch sensor is activated
def touch_down():
    return True
