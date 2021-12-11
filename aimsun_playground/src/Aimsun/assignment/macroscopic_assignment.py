import sys
import time
from PyANGBasic import *
from PyANGKernel import *
from PyANGConsole import *
import shlex
import import_matrix

# Main script to complete the full netowrk import
def main(argv):
    # overallStartTime = time.perf_counter()
    if len(argv) < 3:
        print("Incorrect Number of Arguments")
        print(
            "Arguments: -script script.py input_network.ang output_network.ang input_matrix.txt"
        )
        return -1
    # Start a console
    console = ANGConsole()
    # Load a network
    load_network(console, argv[1])

    model = console.getModel()

    centroid_config = create_gkobject(
        "GKCentroidConfiguration", model, "Centroid Configuration"
    )
    add_folder_to_gkobject("GKModel::centroidsConf", model, centroid_config)

    functions = create_gkobject("GKFunctionCost", model, "Amits_VDFs")
    add_folder_to_gkobject("GKModel::functions", model, functions)
    ##########################################################################################
    sectionType = model.getType("GKSection")

    for types in model.getCatalog().getUsedSubTypesFromType(sectionType):

        for section in types.values():
            attr = section.getType().getColumn(
                "GKSection::numberOfPTLinesAtt", GKType.eSearchThisAndParentTypes
            )
            section.setSpeed(section.getSpeed() * 0)

            print(
                section.getId(),
                " : ",
                section.getSpeed(),
                "km/h : ",
                section.getRoadType().getName(),
            )
    ############################################################################################
    # sectionType = model.getType("GKSection")
    # attributes = sectionType.getColumns(GKType.eSearchOnlyThisType)

    # for x in attributes:

    #     print("Name :" + str(x.getName()))

    #     print("External Name: " + str(x.getExternalName()))

    #     print("Column Type: " + str(x.getColumnType()))

    #     print("Description: " + str(x.getDescription()))
    save_network(console, model, argv)

    ####################################################################
    # sectionType = model.getType("GKSection")
    # attributes = sectionType.getColumns(GKType.eSearchOnlyThisType)

    # sectionType = model.getType("GKSection")

    # for types in model.getCatalog().getUsedSubTypesFromType(sectionType):

    #     for section in types.values():

    #         attr = section.getType().getColumn(
    #             "GKSection::numberOfPTLinesAtt", GKType.eSearchThisAndParentTypes
    #         )
    #         print(
    #             section.getId(),
    #             ",",
    #             section.getSpeed(),
    #             ",",
    #             section.getDataValueDouble(attr),
    #         )


def load_network(console, network_file):
    if console.open(network_file):
        print("load campnou network")
    else:
        console.getLog().addError("Cannot load the network")
        print("cannot load network")
        return -1


def create_gkobject(gk_object_internal_name, model, target_name):
    gk_object = GKSystem.getSystem().newObject(str(gk_object_internal_name), model)
    gk_object.setName(str(target_name + " " + str(gk_object.getId())))
    return gk_object


def add_folder_to_gkobject(internal_folder_name, model, gkobject):
    folder_name = str(internal_folder_name)
    folder = model.getCreateRootFolder().findFolder(folder_name)
    if folder == None:
        folder = GKSystem.getSystem().createFolder(
            model.getCreateRootFolder(), folder_name
        )
    folder.append(gkobject)


def save_network(console, model, argv):
    console.save(argv[2])
    # Reset the Aimsun undo buffer
    model.getCommander().addCommand(None)
    print("Network saved Successfully")


if __name__ == "__main__":
    main(sys.argv)
