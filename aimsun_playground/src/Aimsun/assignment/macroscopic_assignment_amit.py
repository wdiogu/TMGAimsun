import sys
import time
from PyANGBasic import *
from PyANGKernel import *
from PyANGConsole import *
import shlex
import inspect



def vdf(context, section, funcVolume):
    """this function is the default function found in the ang file we were playing with
    over the weekend keepting it here for backup and reference"""
    volume = funcVolume.getVolume()
    capacity = section.getCapacity()
    addVolume = section.getAdditionalVolume()

    factor1 = ( 60.0 / section.getSpeed() ) * section.length3D() / 1000.0
    factor2 = 15.0 * 22.0 * 0.985 ** 3.6 * (  ( (volume + addVolume) / capacity ) - 0.985 ) + 1.0 + 4.8 * 0.985 ** 4.6
    factor3 = 1.0 + 4.8 * ( (volume + addVolume) / capacity ) ** 4.6
    time = factor1 * max( factor2 , factor3 )

    #print (dir(section))
    #print( dir(context.userClass) )
    model = context.userClass.getModel()
    sectionType = model.getType( "GKUserClass" )
    attributes  = sectionType.getColumns( GKType.eSearchOnlyThisType )
    for x in attributes:
        #print ( str(x.getName()), str(x.getExternalName()) )
        if x.getExternalName() == "value_of_time":
            value_of_time = context.userClass.getDataValueDouble(x)
            break
    print ('value of time ', value_of_time) 
    vehicle = context.userClass.getVehicle()
    #print ( "ID ", section.getId(), vehicle.getValueOfTimeMean() )
    #print ( context.userClass.getVehicle(), "***", context.userClass.getId(), "***" , context.userClass.getName() )
    if context.userClass.getName() == "Car":
        time = 1000.0
    return time

def loadModel(filepath, console):
    """to load the model"""
    if console.open(filepath):
        #model = console.getModel()
        model = GKSystem.getSystem().getActiveModel()
        print("Open network")
    else:
        console.getLog().addError("Cannot load the network")
        print("Cannot load the network")
        return -1
    catalog = model.getCatalog()
    geomodel = model.getGeoModel()
    return model, catalog, geomodel

def addColumn(userClassType, arg_list):
    userClassType.addColumn( arg_list[0], arg_list[1], arg_list[2] ) 
    print ('columns were successfully added')

def save(console, model):
    console.save("C:\\Users\\sandhela\\source\\repos\\williamsProject1\\aimsun_playground\\input_files\\aimsun_files\\test2.ang")
    # Reset the Aimsun undo buffer
    model.getCommander().addCommand( None )
    print ("Network saved Successfully")

def create_and_read_custom_attribute(model, console,  catalog, geomodel):
    #in C interop reference to logic underhood in C of GKuserclass
    #to deal with taht refelction is via string compariosn and returns a 
    #proxy object and proxy boject to get to c object itself 

    #getTYpe() returns an reference to c object type 
    user_class_type = model.getType("GKUserClass")
    #getobjects by type by proxy returns a map of the reference proxy objects 
    #python ojbcts c objects represtns everything here done by proxy
    #actual data is stored in C all python level references to have API calls to understand to C object
    user_classes = catalog.getObjectsByType( user_class_type )

    # #add a new column of a custom attribute
    addColumn(user_class_type, ["GKUserClass::value_of_time_python", "value_of_time_python", GKColumn.Double, GKColumn.eExternal])
    addColumn(user_class_type, ["GKUserClass::value_of_time2_python", "value_of_time2_python", GKColumn.Double, GKColumn.eExternal])


    for x in user_classes:
        print (x, user_classes[x].getName())

    attributes  = user_class_type.getColumns( GKType.eSearchOnlyThisType )
    for x in attributes:
        if x.getExternalName() == "value_of_time_python":
            for user_class in user_classes:
                if user_classes[user_class].getName() == "Car":
                    print (dir(user_classes[user_class]))
                    user_classes[user_class].setDataValueDouble(x, 235.34)
                elif user_classes[user_class].getName() == "Truck":
                    print (dir(user_classes[user_class]))
                    user_classes[user_class].setDataValueDouble(x, 345.45)
                elif user_classes[user_class].getName() == "Bus":
                    print (dir(user_classes[user_class]))
                    user_classes[user_class].setDataValueDouble(x, 678.678)
            break
   
    #save the model 
    save(console, model)

def read_vdf_functions(console, model, catalog):
    """attempt to read the vdfs in a given pre-existing network by looping over the function folder"""
    print('hello')
    #getTYpe() returns an reference to c object type 
    classtype_function_cost = model.getType("GKFunctionCost")
    dict_catalog_function_cost = catalog.getObjectsByType( classtype_function_cost )
    for item in dict_catalog_function_cost:
        val = dict_catalog_function_cost[item]
        #print (item, dict_catalog_function_cost[item].getName(), val.getFunctionType(), val.getLanguage(), val.getDefinition() )
    print (dir(dict_catalog_function_cost[item]))

fun_test = """
def hello_world():
    print("hello world")
"""
def edit_existing_vdf_functions(console, model, catalog):
    """attempt to edit an existing vdf function in the network heer we can create a new python function"""
    print('hello')
    #getTYpe() returns an reference to c object type 
    classtype_function_cost = model.getType("GKFunctionCost")
    dict_catalog_function_cost = catalog.getObjectsByType( classtype_function_cost )
    for item in dict_catalog_function_cost:
        if item == 2826:
            function_of_interest = dict_catalog_function_cost[item]
            function_of_interest.setFunctionType(4)
            function_of_interest.setDefinition(fun_test)


def create_new_functions(console, model, catalog):
    """attempt to create a new vdf function"""
    print('hello')
    classtype_function_cost = model.getType("GKFunctionCost")
    dict_catalog_function_cost = catalog.getObjectsByType( classtype_function_cost )
   

# Main script to complete the full netowrk import
def main(argv):
    overallStartTime = time.perf_counter()
    if len(argv) < 3:
        print("Incorrect Number of Arguments")
        print("Arguments: -script script.py campnou_network.ang output_folder")
        return -1
    # Start a console
    console = ANGConsole()
    Network = sys.argv[1]
    networkFolder = sys.argv[2]
    print ('argv: ', argv)
    # generate a model of the input network
    model, catalog, geomodel = loadModel(Network, console)
    #create_and_read_custom_attribute(model, console, catalog, geomodel)
    #read_vdf_functions(console, model, catalog)
    #edit_existing_vdf_functions(console, model, catalog)
    create_new_functions(console, model, catalog)
    save(console, model)

    overallEndTime = time.perf_counter()
    print(f"Overall Runtime: {overallEndTime-overallStartTime}s")

if __name__ == "__main__":
    main(sys.argv)