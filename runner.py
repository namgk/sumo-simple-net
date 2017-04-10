from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci

def run():
    """execute the TraCI control loop"""
    step = 0
    laneMap = {}
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        allVehicles = traci.vehicle.getIDList()
        for v in allVehicles:
            vDirection = 1 if traci.vehicle.getAngle(v) < 180 else 0
            vSpeed = traci.vehicle.getSpeed(v)
            print(vDirection)
            vLane = traci.vehicle.getLaneIndex(v)
            if not v in laneMap:
                laneMap[v] = [vLane]
            elif laneMap[v][-1] != vLane:
                laneMap[v].append(vLane)

        # if veh in allVehicles:
        #     vehLane = traci.vehicle.getLaneIndex(veh)
        #     print(vehLane)
        #     vehLoc = traci.vehicle.getPosition(veh)
        #     vehCoord = traci.simulation.convertGeo(vehLoc[0], vehLoc[1])
        #     lat = vehCoord[1]
        #     lon = vehCoord[0]
            # print("[%s, %s],"%(lat,lon))
        step += 1
    # print(laneMap)
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "osm.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
