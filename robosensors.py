# Sensor processing for RoboMagellan2012

import threading,serial,re,time
import roboconfig
from robocomms import log
from roboutils import * 

# Sensor values
compass_value = 999
bumper_status = False
ping_data = [999,999,999,999]

#------------------------------------------------------------------------
# Compass communication thread
#------------------------------------------------------------------------
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


#------------------------------------------------------------------------
# PING and bumper communication thread
#------------------------------------------------------------------------
class SensorThread(threading.Thread):

    ser = serial.Serial(roboconfig.sensor_serial_port-1, \
                            roboconfig.sensor_serial_baud)
    sensor_re = re.compile('sensor (\d): (\d+)')
    run_flag = True

    # Get the sensor data
    def run(self):
        while self.run_flag == True:
            global ping_data, bumper_status
            self.ser.flushInput() # Discard readings buffered during sleep
            self.ser.readline()
            # Read five lines of data to get complete input
            for i in range(5):
                data = self.ser.readline().lower().strip()
                if data.find('bumper') == 0:
                    if data.find('on') > 0:
                        bumper_status = True
                    elif data.find('off') > 0:
                        bumper_status = False
                    else:
                        log("robosensors - recieved invalid bumper data: %s" % \
                                data)
                elif data.find('sensor') == 0:
                    m = self.sensor_re.match(data)
                    if m:
                        ping_data[int(m.group(1))-1] = int(m.group(2))
                    else:
                        log("robosensors - recieved invalid sensor data: %s" % \
                                data)
                else:
                    log("robosensor - received invalid data %s" % data)

            time.sleep(roboconfig.sensor_read_delay)

    
    # Stop the thread
    def stop(self):
        self.run_flag = False


def initialize():
    log("Sensor initialization started")
    compass_thread = CompassThread()
    compass_thread.start()
    sensor_thread = SensorThread()
    sensor_thread.start()
    log("Sensor initialization completed")
    return True

#-----------------------------------------------------------------------
# Return the sensor data
#-----------------------------------------------------------------------
def get_compass():
    global compass_data
    return compass_data

def get_bumper():
    global bumper_status
    return bumper_status

def get_sensors():
    global ping_data
    return ping_data

# touch_down() - return True if the touch sensor is activated
def touch_down():
    return get_bumper()
