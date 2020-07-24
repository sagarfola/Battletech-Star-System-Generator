from dice_roller import rolldice
# Generate Asteroid Belt


def Asteroid_Belt():
    ast_diameter = 400 + 100 * rolldice(3, 6)
    ast_density = rolldice(1, 6) ** 1.15
    ast_day_length = rolldice(2, 6)
    return ast_diameter, ast_density, ast_day_length


# Generate Dwarf Terrestrial
def Dwarf_Terrestrial():
    d_terra_diameter = 400 + 100 * rolldice(3, 6)
    d_terra_density = rolldice(1, 6)
    d_terra_day_length = rolldice(3, 6) + 12
    return d_terra_day_length, d_terra_diameter, d_terra_density


# Generate Terrestrial
def Terrestrial():
    terra_diameter = 2500 + 1000 * rolldice(2, 6)
    terra_density = 2.5 + rolldice(1, 6) ** 0.75
    terra_day_length = rolldice(3, 6) + 12
    return terra_day_length, terra_density, terra_diameter


# Generate Giant Terrestrial
def Giant_Terrestrial():
    g_terra_diameter = 12500 + 1000 * rolldice(1, 6)
    g_terra_density = 2 + rolldice(1, 6)
    g_terra_day_length = rolldice(4, 6)
    return g_terra_day_length, g_terra_density, g_terra_diameter


# Generate Gas Giant
def gas_giant():
    gas_giant_diameter = 50000 + 10000 * rolldice(2, 6)
    gas_giant_density = 0.5 + rolldice(2, 6) / 10
    gas_giant_day_length = rolldice(4, 6)
    return gas_giant_day_length, gas_giant_density, gas_giant_diameter


# Generate Ice Giant
def ice_giant():
    ice_giant_diameter = 25000 + 5000 * rolldice(1, 6)
    ice_giant_density = 1 + rolldice(2, 6) / 10
    ice_giant_day_length = rolldice(4, 6)
    return ice_giant_day_length, ice_giant_density, ice_giant_diameter
