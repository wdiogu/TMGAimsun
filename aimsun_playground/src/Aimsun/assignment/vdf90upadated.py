
"""
VDFs as defined in Network Coding Standard (NCS) 16 for:

-VDF 90

Assumptions:
- section 90 is a centroid connector therefore it does not need a section.getAdditionalVolume()

"""
def time(context, section, volume):
    """
    this is for the power of 6
    """
    speed = section.getSpeed()
    length = section.length2D()/1000
    return length*60.0/speed

def get_gas_cost(context, section):
    """
    function to extract the gas cost
    """
    cost_of_gas_perkm = 0.067603
    length = section.length2D()/1000

    return length * cost_of_gas_perkm

def getDouble(object, attribute_name, sectionType):
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
    return toll + get_gas_cost(context, section)

def vdf(context, section, volume):
    """
    output unit utils normalizezd to min
    """
    return (60.0*cost(context, section))/get_value_of_time(context) + time(context, section, volume)

