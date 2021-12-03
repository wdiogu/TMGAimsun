import sys
import time
from PyANGBasic import *
from PyANGKernel import *
from PyANGConsole import *
import shlex


# Main script to complete the full netowrk import
overallStartTime = time.perf_counter()


def main(argv):
    if len(argv) < 3:
        print("Incorrect Number of Arguments")
        print("Arguments: -script script.py campnou_network.ang output_folder")
        return -1

    # Start a console
    console = ANGConsole()

    # Load network
    load_network(console, argv[1])

    # Start the model
    model = console.getModel()

    # Export the matrices
    _execute(model, argv)


def load_network(console, network_file):
    if console.open(network_file):
        print("load campnou network")
    else:
        console.getLog().addError("Cannot load the network")
        print("cannot load network")
        return -1


# Write the matrix to the currently open file
# Change this method if you want to change the format of the file (ie from a list of trips
# to a matrix)
def exportMatrix(file, matrix):
    centroids = matrix.getCentroidConfiguration().getCentroidsInOrder()
    file.write("%u %s\n" % (matrix.getId(), matrix.getName()))
    if matrix.getVehicle() != None:
        file.write(
            "%u %s\n" % (matrix.getVehicle().getId(), matrix.getVehicle().getName())
        )
    else:
        file.write("0 None\n")
    file.write("%s\n" % matrix.getFrom().toString())
    file.write("%s\n" % matrix.getDuration().toString())
    for origin in centroids:
        for destination in centroids:
            if origin != destination:
                trips = matrix.getTrips(origin, destination)
                if trips > 0:
                    file.write(
                        "%u %u %f\n" % (origin.getId(), destination.getId(), trips)
                    )
    file.write("\n")


# Export all the matrices in a centroid configuration
def exportMatricesConf(model, file, centroidConf):
    odMats = centroidConf.getODMatrices()
    if odMats != None:
        for matrix in odMats:
            if matrix.isA("GKODMatrix"):
                exportMatrix(file, matrix)


# Export all the matrices in a traffic demand
def exportMatricesDemand(model, file, trafficDemand):
    for schedule in trafficDemand.getSchedule():
        if schedule.getTrafficDemandItem().isA("GKODMatrix"):
            exportMatrix(file, schedule.getTrafficDemandItem())


# Export matrices from object "entry". It can be either a traffic demand or a centroid configuration.
# Change here the file name and path if required.
def export(model, entry, matrixFilePath):
    container = model.getCatalog().find(int(entry))
    if container != None:
        file = open(matrixFilePath, "w")
        if file != None:
            if container.isA("GKCentroidConfiguration"):
                exportMatricesConf(model, file, container)
                print("Centroid configuration matrices exported")
            elif container.isA("GKTrafficDemand"):
                exportMatricesDemand(model, file, container)
                print("Traffic demand matrices exported")
            else:
                print("Object is neither a centroid configuration not a traffic demand")
            file.close()
        else:
            print("File cannot be opened")
    else:
        print("No object to export")


def _execute(model, argv):
    # Identifier of the object that holds the matrices to export (either a traffic demand
    # or a centroid configuration)
    objectToExport = 956

    # Full path to the file in where matrices will be written
    matrixFilePath = argv[3]

    # Entry code, the script starts here
    # Export the matrices. Set the right ID before using this script.
    export(model, objectToExport, matrixFilePath)
    print("Done")


if __name__ == "__main__":
    main(sys.argv)


overallEndTime = time.perf_counter()
print(f"Overall Runtime: {overallEndTime-overallStartTime}s")
