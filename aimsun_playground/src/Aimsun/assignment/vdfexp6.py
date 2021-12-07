
"""
VDFs as defined in Network Coding Standard (NCS) 16 for:

-VDF 11,12
-VDF 14
-VDF 18

Assumptions 
- value_of_Time attribute is a custom attribute created in UserClass::value_of_time output unit $/hr
- gas_cost_perkm is a constant value with units of $/km
- all sections need the getAdditionalVolume()

"""

def time(context, section, volume):
    """
    this is for the power of 6 
    output is min 
    """
    speed = section.getSpeed()
    length = section.length2D()/1000
    volau = volume.getVolume()
    volad = section.getAdditionalVolume()
    capacity = section.getCapacity()  #section capacity = lane capacity x lanes

    VC = (volau + volad) / capacity

    if VC <= 1:
        t = (length * 60 / speed) * (1 + VC**6)
    else:
        t = (length * 60 / speed) * (6 * VC - 4)
    return t

def get_gas_cost(context, section):
    """
    function to extract the gas cost
    """
    cost_of_gas_perkm = 0.067603
    length = section.length2D()/1000

    return length * cost_of_gas_perkm

def getDouble(object, attribute_name, sectionType):
    """
    a generic function to extract values from an attribute that are of type double
    """
    attributes  = sectionType.getColumns( GKType.eSearchOnlyThisType )
    for x in attributes:
        if x.getExternalName() == attribute_name:
            return object.getDataValueDouble(x)
    return 0.0

def get_value_of_time(context):
    """
    function to extract the value_of_time from the userclass object
    This is an custom attribute created inside UserClas Object
    output unit $/hr
    """
    model = context.userClass.getModel()
    userClassType = model.getType( "GKUserClass" )
    return getDouble(context.userClass, "value_of_time", userClassType)
   
def toll(context, section):
    model = context.userClass.getModel()
    sectionType = model.getType( "GKSection" )
    name = "toll_"  + context.userClass.getName()
    return getDouble(section, name, sectionType)

def cost(context, section):
    """
    output unit $
    """
    return toll(context, section) + get_gas_cost(context, section)

def vdf(context, section, volume):
    """
    output unit utils normalizezd to min
    """
    return (60.0*cost(context, section))/get_value_of_time(context) + time(context, section, volume)

