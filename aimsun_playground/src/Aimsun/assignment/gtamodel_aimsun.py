import sys
import time
from typing import _SpecialForm
from PyANGBasic import *
from PyANGKernel import *
from PyANGConsole import *
import shlex

# Main script to complete the full netowrk import
overallStartTime = time.perf_counter()


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
    overallEndTime = time.perf_counter()
    print(f"Network Load Time: {overallEndTime-overallStartTime}s")

    model = console.getModel()
    # section_type = model.getType("GKSection")
    # for items in section_type.getColumns(GKType.eSearchOnlyThisType):
    #     if items.getExternalName() == "speed" or items.getExternalName() == "SPEED":

    #         print(
    #             items.getExternalName(),
    #             ",",
    #             items.getColumnType(),
    #             ",",
    #             items.getDataValueDouble(items),
    #         )

    sectionType = model.getType("GKSection")

    for types in model.getCatalog().getUsedSubTypesFromType(sectionType):

        for section in types.values():

            attr = section.getType().getColumn(
                "GKSection::numberOfPTLinesAtt", GKType.eSearchThisAndParentTypes
            )
            print(
                section.getId(),
                ":",
                section.getSpeed(),
                ":",
                section.getDataValueDouble(attr),
                ":",
                section.getRoadType().getName(),
            )

    # for types in model.getCatalog().getUsedSubTypesFromType(section_type):
    #     # for section in types.itervalues():
    #     speed = types.getSpeed()
    #     print(speed)

    # save_network(console, model, argv)◘


if __name__ == "__main__":
    main(sys.argv)

overallEndTime = time.perf_counter()
print(f"Overall Loadtime: {overallEndTime-overallStartTime}s")
