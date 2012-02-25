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
# **** Network Configuration ****
camera_host = "localhost"      # hostname of camera server (RoboRealm)
camera_port = 4040             # port of camera server
comms_port = 4041              # incoming communications requests
monitor_port = 4042            # outgoing log messages
command_port = 4043            # port for incoming command
