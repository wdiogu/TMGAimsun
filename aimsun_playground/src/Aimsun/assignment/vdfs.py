# Exmaple from primary
def distance(context, section, funcVolume):
    distance = section.length3D() / 1000.0
    return distance


def time(context, section, funcVolume):
    volume = funcVolume.getVolume()
    capacity = section.getCapacity()
    addVolume = section.getAdditionalVolume()

    factor1 = (60.0 / section.getSpeed()) * section.length3D() / 1000.0
    factor2 = (
        15.0 * 25.6 * 0.985 ** 2.2 * (((volume + addVolume) / capacity) - 0.985)
        + 1.0
        + 8.0 * 0.985 ** 3.2
    )
    factor3 = 1.0 + 8.0 * ((volume + addVolume) / capacity) ** 3.2
    time = factor1 * max(factor2, factor3)
    return time


def vdf(context, section, funcVolume):
    cost = time(context, section, funcVolume)
    return cost


def get_value_of_time(context):
    """
    function to extract the value_of_time and tollSegment from the userclass object
    """
    model = context.userClass.getModel()
    sectionType = model.getType("GKUserClass")
    attributes = sectionType.getColumns(GKType.eSearchOnlyThisType)
    vehicle = context.userClass.getVehicle()
    for x in attributes:
        if x.getExternalName() == "value_of_time":
            value_of_time = context.userClass.getDataValueDouble(x)
            break
    return value_of_time


def get_toll_on_section(context):
    """
    function to extract the toll on segment
    """

    # each section toll_car, toll_truck
    model = context.userClass.getModel()
    sectionType = model.getType("GKUserClass")
    attributes = sectionType.getColumns(GKType.eSearchOnlyThisType)
    vehicle = context.userClass.getVehicle()
    for x in attributes:
        if x.getExternalName() == "toll_on_section":
            toll_on_segment = context.userClass.getDataValueDouble(x)
            break
    return toll_on_segment


def get_gas_per_km(context):
    """
    function to extract the gas cost
    """
    model = context.userClass.getModel()
    sectionType = model.getType("GKUserClass")
    attributes = sectionType.getColumns(GKType.eSearchOnlyThisType)
    vehicle = context.userClass.getVehicle()
    for x in attributes:
        if x.getExternalName() == "gas_cost":
            gas_cost = context.userClass.getDataValueDouble(x)
            break
    return gas_cost


def cost(context, section):
    length = section.length2D() / 1000.0
    cost_in_dollars = length * get_gas_per_km(context) + get_toll_on_section(context)
    return cost_in_dollars


# a fd11 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 6) * (get(1) .le. 1) + (6 * get(1) - 4) * (get(1) .gt. 1))
# a fd12 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 6) * (get(1) .le. 1) + (6 * get(1) - 4) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    time = (length * 60.0 / ul2) * (1 + putGet ** 6) * (putGet <= 1) + (
        6 * putGet - 4
    ) * (putGet > 1)
    #
    utils = time + get_value_of_time(context) * (length + get_gas_cost(context))
    return utils


# a fd13 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    cost = (length * 60.0 / ul2) * (1 + putGet ** 4) * (putGet <= 1) + (
        4 * putGet - 2
    ) * (putGet > 1)
    return cost


# a fd14 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 6) * (get(1) .le. 1) + (6 * get(1) - 4) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    cost = (length * 60.0 / ul2) * (1 + putGet ** 6) * (putGet <= 1) + (
        6 * putGet - 4
    ) * (putGet > 1)
    return cost


# a fd15 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd16 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd17 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    cost = (length * 60.0 / ul2) * (1 + putGet ** 4) * (putGet <= 1) + (
        4 * putGet - 2
    ) * (putGet > 1)
    return cost


# a fd18 =(length * 60 / ul2) * (((1 + put((volau + volad) / (lanes * ul3)) ^ 6) * (get(1) .le. 1) + (6 * get(1) - 2) * (get(1) .gt. 1))) + 5
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    putGet = (volume + addVolume) / capacity
    cost = (
        (length * 60.0 / ul2) * (1 + putGet ** 6) * (putGet <= 1)
        + (6 * putGet - 2) * (putGet > 1)
        + 5
    )
    return cost


# a fd20 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd21 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd22 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd23 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    cost = (length * 60.0 / ul2) * (1 + putGet ** 4) * (putGet <= 1) + (
        4 * putGet - 2
    ) * (putGet > 1)
    return cost


# a fd30 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd31 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd32 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd33 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd34 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd35 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd36 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd40 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd41 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd42 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd43 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd44 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd45 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd46 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd47 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd48 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    cost = (length * 60.0 / ul2) * (1 + putGet ** 4) * (putGet <= 1) + (
        4 * putGet - 2
    ) * (putGet > 1)
    return cost


# a fd50 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd51 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd52 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd53 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
# a fd54 =(length * 60 / ul2) * ((1 + put((volau + volad + el1) / (lanes * ul3)) ^ 4) * (get(1) .le. 1) + (4 * get(1) - 2) * (get(1) .gt. 1))
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    volume = funcVolume.getVolume()
    addVolume = section.getAdditionalVolume()
    capacity = section.getCapacity()
    model = section.getModel()
    vehicleType = model.getType("GKVehicle")
    el1 = 0.0
    allVehicles = model.getCatalog().getObjectsByType(vehicleType)
    for veh in iter(allVehicles.values()):
        if veh.getTransportationMode().getExternalId() == "b":
            el1 += funcVolume.getVolume(veh)
    putGet = (volume + addVolume + el1) / capacity
    cost = (length * 60.0 / ul2) * (1 + putGet ** 4) * (putGet <= 1) + (
        4 * putGet - 2
    ) * (putGet > 1)
    return cost


# a fd90 =(length * 60 / ul2)
def vdf(context, section, funcVolume):
    length = section.length2D() / 1000.0  # length in km
    ul2 = section.getSpeed()
    cost = length * 60.0 / ul2
    return cost
