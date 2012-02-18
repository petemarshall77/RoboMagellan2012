# Control file processing for RoboMagellan2012

import sys, re
from roboutils import *

def process_goto_directive(line):
    pass

def process_driv_directive(line):
    pass

def process_cone_directive(line):
    # Parse Cone data
    cone_re = re.compile('CONE\s+(\d\d)(\d\d).(\d+)\s+(\d\d\d)(\d\d).(\d+)')
    m = cone_re.search(line)
    if not m:
        log("Invalid CONE directive in line: " + line)
        return False

    # Validate and calculate latitude
    lat_deg = int(m.group(1))
    lat_min = int(m.group(2))
    if lat_min > 59:
        log("Minutes must be less than 60 in latitude specification in line: " + line)
        return False
    lat_min = lat_min + int(m.group(3))/1000.0
    lat_deg = lat_deg + lat_min/60.0
    
    # Validate and calculate longitude
    lon_deg = int(m.group(4))
    lon_min = int(m.group(5))
    if lon_min > 59:
        log("Minutes must be less than 60 in longitude specification in line: " + line)
        return False
    lon_min = lon_min + int(m.group(6))/1000.0
    lon_deg = lon_deg + lon_min/60.0
    
    return {'command': "CONE", 'latitude': lat_deg, 'longitude': lon_deg}
def process_stop_directive(line):
    pass

def process_control_line(line):
    """Processes a line from the RoboMagellen control file."""

    # skip comments and blank lines
    if line[0] == '#':
        return None
    if line == "":
        return None
    re_anything = re.compile('\S+')
    if re_anything.match(line) == None:
        return None

    # determine and process line type
    line = line.rstrip()
    if line[0:4] == "DRIV":
        return process_driv_directive(line)
    elif line[0:4] == "GOTO":
        return process_goto_directive(line)
    elif line[0:4] == "CONE":
        return process_cone_directive(line)
    elif line[0:4] == "STOP":
        return process_stop_directive(line)
    elif line[0:4] == "STER":
        return process_ster_directive(line)
    elif line[0:4] == "POWR":
        return process_powr_directive(line)
    elif line[0:4] == "WAIT":
        return process_wait_directive(line)
    else:
        log("Undefined directive " + line[0:4] +" in line: " + line)
        return False

def process_control_file(filename):
    """Parses the RoboMagellan control file. Returns a data structure with
    the route details if sucessful, otherwise NULL if an error is
    found"""

    log("Processing control file: " + filename)
    error_count = 0
    control_data = []

    # Process the file
    f = open(filename)
    while True:
        line = f.readline()
        log(">>> " + line.rstrip())
        if not line: break
        result = process_control_line(line)
        if result == False:
            error_count = error_count + 1
        elif result == None:
            pass
        else:
            control_data.append(result)
    f.close()

    # Return the control data or None to the caller
    if error_count == 1:
        log("Control file processed, " + str(error_count) + " error.")
    else:
        log("Control file processed, " + str(error_count) + " errors.")

    if error_count == 0:
        return control_data
    else:
        raise RobotError('Control file error')
