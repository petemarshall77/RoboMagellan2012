#
# Configuration data for RoboMagellan2012
#

# Radius of error for GPS in meters
gps_radius = 3.0

# Maximum reliable camera distance in meters
max_camera_distance = 2.5

# Maximum time before warning that no camera data is recieved in seconds
camera_timeout = 10

# Number of times to re-try sighting a cone and time
# between attempts
re_sight_attempts = 10
re_sight_sleep_time = 0.5

# Time between speed changes (for smooth acceleration)
power_delay = 0.25

# **** Serial connections ****
power_serial_port = 6
power_serial_baud = 9600
compass_serial_port = 2
compass_serial_baud = 19200
compass_read_delay = 0.25     # read compass every n.n seconds
sensor_serial_port = 5
sensor_serial_baud = 9600
sensor_read_delay = 0.1     # read sensor data every n.n seconds
gps_serial_port = 1
gps_serial_baud = 4800
gps_serial_timeout = 5

# **** Network Configuration ****
camera_host = "localhost"      # hostname of camera server (RoboRealm)
camera_port = 4040             # port of camera server
comms_port = 4041              # incoming communications requests
monitor_port = 4042            # outgoing log messages
command_port = 4043            # port for incoming command
