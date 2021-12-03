import sys
import time
from PyANGBasic import *
from PyANGKernel import *
from PyANGConsole import *
import shlex
import datetime

# from PySide6 import QtCore


# Main script to complete the full netowrk import
overallStartTime = time.perf_counter()


# def main(argv):
#     if len(argv) < 3:
#         print("Incorrect Number of Arguments")
#         print("Arguments: -script script.py campnou_network.ang input_matrix")
#         return -1

    # Start a console
    # console = ANGConsole()

    # # Load network
    # load_network(console, argv[1])

    # # Start the model
    # model = console.getModel()
    # target = model.getCatalog().find(956)

    # # Export the matrices
    # _execute(console, model, argv, target)


def load_network(console, network_file):
    if console.open(network_file):
        print("load campnou network")
    else:
        console.getLog().addError("Cannot load the network")
        print("cannot load network")
        return -1


def importMatrix(fileName, centroidConf, model):
    state = 0
    matrix = None
    for line in open(fileName, "r").readlines():
        line = line.strip()
        if len(line) == 0:
            state = 0
        else:
            if state == 0:
                state = 1
                # read identifier and name
                matrixId = int(line[: line.index(" ")])
                matrixName = line[line.index(" ") + 1 :]
                matrix = centroidConf.getModel().getCatalog().find(matrixId)
                if matrix == None or matrix.isA("GKODMatrix") == False:
                    matrix = GKSystem.getSystem().newObject("GKODMatrix", model)
                    matrix.setName(matrixName)
                    centroidConf.addODMatrix(matrix)
                else:
                    print("New Matrix")
            elif state == 1:
                state = 2
                # read vehicle id and name
                vehId = int(line[: line.index(" ")])
                vehName = line[line.index(" ") + 1 :]
                vehicle = centroidConf.getModel().getCatalog().find(vehId)
                if vehicle == None:
                    vehicle = centroidConf.getModel().getCatalog().findByName(vehName)
                if vehicle != None:
                    matrix.setVehicle(vehicle)
            elif state == 2:
                state = 3
                # From Time
                matrix.setFrom(datetime.datetime.strptime(line, "%H:%M:%S").time())
                # matrix.setFrom().fromString(line)

            elif state == 3:
                state = 4
                # Duration
                # matrix.setDuration(GKTimeDuration.fromString(line))
                matrix.setDuration(GKTimeDuration.fromString(line))

            elif state == 4:
                # Trips
                tokens = line.split(" ")
                if len(tokens) == 3:
                    fromCentroid = (
                        centroidConf.getModel().getCatalog().find(int(tokens[0]))
                    )
                    toCentroid = (
                        centroidConf.getModel().getCatalog().find(int(tokens[1]))
                    )
                    trips = float(tokens[2])
                    # Set the value if the section is valid
                    if fromCentroid != None and toCentroid != None:
                        matrix.setTrips(fromCentroid, toCentroid, trips)
    matrix.setStatus(GKObject.eModified)


def _execute(console, model, argv, target):
    matrixFilePath = argv[2]
    # Import matrices. Set the right ID before using this script.
    if target != None:
        importMatrix(matrixFilePath, target, model)
        # Be sure that you reset the UNDO buffer after a modification that cannot be undone
        model.getCommander().addCommand(None)
        print("Done")
    else:
        model.reportError(
            "Import Matrices",
            "The script must be launched from a Centroid Configuration context menu",
        )

    # save(console, model, argv)


# def save(console, model, argv):

#     console.save(argv[3])

#     # Reset the Aimsun undo buffer

#     model.getCommander().addCommand(None)

#     print("Network saved Successfully")


# if __name__ == "__main__":
#     main(sys.argv)


overallEndTime = time.perf_counter()
print(f"Overall Runtime: {overallEndTime-overallStartTime}s")
