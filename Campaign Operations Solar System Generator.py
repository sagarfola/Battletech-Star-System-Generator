from dice_roller import rolldice
import csv
import random
import math
from tkinter import *

# Determine which table to roll on the Primary Star Generation Table
star_style = -1
while star_style == -1:
    try:
        star_style = int(input("What style of star generation would you like?\n1. Realistic\n2. Life-Friendly\n3. Hot "
                               "Star\n4. Random!\nEnter 1, 2, 3 or 4: "))
        if star_style < 1 or star_style > 4:
            print("\nERROR: Enter 1, 2, 3 or 4 for the star generation style\n")
            star_style = -1
            continue
        elif star_style == 4:
            star_style = random.randint(1, 3)
            break
        else:
            break
    except ValueError:
        continue

starname = input("Enter a name for your star: ")

# Determine star type and subtype
with open("Primary Star Generation Table.csv") as file:
    star_select = rolldice(2, 6)
    star_search = {star_select: tuple(stars) for star_select, *stars in csv.reader(file)}
    real, life, hot = star_search[str(star_select)]
    star_style_list = {1: real, 2: life, 3: hot}
    star_subtype = rolldice(1, 10) - 1
    star_type = (star_style_list[star_style], star_subtype)
print("Your star type is " + str(star_type[0]) + str(star_type[1]) + "V.")

# Store data about the given star type
with open("Primary Solar Stats Table.csv") as file:
    star_stats = {(star_type, star_subtype): tuple(stats) for star_type, star_subtype, *stats in csv.reader(file)}
    charge, transit_time, safe_jump_distance, mass, lum, radius, temp, lifetime, habit_mod, ILZ_dist_km, ILZ_dist_au, ILZ_temp, OLZ_dist_km, OLZ_dist_au, OLZ_temp = \
        star_stats[str(star_type[0]), str(star_type[1])]

# Calculate objects in orbital slots
# First, generate number of orbits (2d6 + 3)
orbit_total = int(rolldice(2, 6) + 3)
print("Orbital slots: " + str(orbit_total))
print("Star mass: " + str(mass) + " (Mstar/Msun)")
# Second, place the orbits based on the mass of the star generated
# Base locations table for calculations starting with slot 1
orbital_locations = []
orbital_baselocations = [
    0.4,
    0.7,
    1.0,
    1.6,
    2.8,
    5.2,
    10.0,
    19.6,
    38.8,
    77.2,
    154.0,
    307.6,
    614.8,
    1229.2,
    2458.0
]
# Fill orbital_locations with the actual star manipulated orbital slots up to the maximum available
slot = 0
while slot < orbit_total:
    orbital_locations.insert(slot, orbital_baselocations[slot] * float(mass))
    slot += 1

# Classify locations as inner or outer system
inner_system = []
outer_system = []
life_system = []
count = 0
while count < orbit_total:
    if orbital_locations[count] <= float(ILZ_dist_au):
        inner_system.insert(count, count + 1)
        count += 1
    elif float(OLZ_dist_au) >= orbital_locations[count] >= float(ILZ_dist_au):
        life_system.insert(count, count + 1)
        count += 1
    else:
        outer_system.insert(count, count + 1)
        count += 1

# Populates orbital slots based on 2d6 roll and split between inner and outer system
inner_system_options = {2: "Empty",
                        3: "Empty",
                        4: "Asteroid Belt",
                        5: "Dwarf Terrestrial Planet",
                        6: "Terrestrial Planet",
                        7: "Terrestrial Planet",
                        8: "Giant Terrestrial Planet",
                        9: "Gas Giant",
                        10: "Gas Giant",
                        11: "Ice Giant",
                        12: "Ice Giant"}
outer_system_options = {2: "Empty",
                        3: "Empty",
                        4: "Asteroid Belt",
                        5: "Dwarf Terrestrial Planet",
                        6: "Gas Giant",
                        7: "Gas Giant",
                        8: "Gas Giant",
                        9: "Terrestrial Planet",
                        10: "Giant Terrestrial Planet",
                        11: "Ice Giant",
                        12: "Ice Giant"}
inner_system_populated = []
outer_system_populated = []
life_system_populated = []
total_system_populated = []
for x in inner_system:
    inner_system_populated.append(inner_system_options[rolldice(2, 6)])
for x in life_system:
    life_system_populated.append(inner_system_options[rolldice(2, 6)])
for x in outer_system:
    outer_system_populated.append(outer_system_options[rolldice(2, 6)])
total_system_populated = inner_system_populated + life_system_populated + outer_system_populated
print("Life zone bounds are " + str(ILZ_dist_au) + " AU to " + str(OLZ_dist_au) + " AU.")

# Parameters to calculate planet parameters.
# Sorted by Asteroid Belt, Dwarf Terrestrial, Terrestrial, Giant Terrestrial, Gas Giant, Ice Giant
planet_type_dict = {"Empty": 0,
                    "Asteroid Belt": 1,
                    "Dwarf Terrestrial Planet": 2,
                    "Terrestrial Planet": 3,
                    "Giant Terrestrial Planet": 4,
                    "Gas Giant": 5,
                    "Ice Giant": 6,
                    "[]": 0}


# Function to calculate Planet Data
def Planetary_Object(planet_type, slot):
    # Values for calculating Planetary Data
    dia_base = [0, 400, 400, 2500, 12500, 50000, 25000]
    dia_mod = [0, 100, 100, 1000, 1000, 10000, 5000]
    dia_die_num = [0, 3, 3, 2, 1, 2, 1]
    den_base = [0, 0, 0, 2.5, 2, 0.5, 1]
    den_die_num = [0, 1, 1, 1, 1, 2, 2]
    den_exp = [1, 1.15, 1, 0.75, 1, 1, 1]
    den_die_div = [1, 1, 1, 1, 1, 10, 10]
    day_die_num = [0, 2, 3, 3, 4, 4, 4]
    day_die_base = [0, 0, 12, 12, 0, 0, 0]

    # Actual Calculations
    diameter = dia_base[planet_type] + dia_mod[planet_type] * rolldice(dia_die_num[planet_type], 6)
    density = den_base[planet_type] + (rolldice(den_die_num[planet_type], 6) / den_die_div[planet_type]) ** den_exp[
        planet_type]
    day_length = rolldice(day_die_num[planet_type], 6) + day_die_base[planet_type]
    gravity = (diameter / 12742) * (density / 5.5153)
    esc_velocity = 11186 * (diameter / 12742) * math.sqrt(density / 5.5153)  # escape velocity in m/s
    yearlength = float(math.sqrt((orbital_locations[slot] ** 3) / float(mass)))
    return diameter, density, day_length, gravity, esc_velocity, yearlength


# Function to calculate Planet Moons
def Moons(planet_type):
    # Initializing Data
    small_moon = 0
    medium_moon = 0
    large_moon = 0
    giant_moon = 0
    rings = False
    moonroll = rolldice(1, 6)

    if planet_type == 0 or planet_type == 1:
        small_moon = 0
        medium_moon = 0
        large_moon = 0
        giant_moon = 0
        rings = False
    else:
        if moonroll < 3:
            if planet_type == 2:
                small_moon = rolldice(1, 6) - 3
                medium_moon = rolldice(1, 6) - 5
            elif planet_type == 3:
                large_moon = rolldice(1, 6) - 5
            elif planet_type == 4:
                small_moon = rolldice(1, 6) - 3
                giant_moon = rolldice(1, 6) - 5
            elif planet_type == 5:
                small_moon = rolldice(5, 6)
                medium_moon = rolldice(1, 6) - 2
                large_moon = rolldice(1, 6) - 1
                giant_moon = rolldice(1, 6) - 4
                if rolldice(1, 6) < 4:
                    rings = True
                else:
                    rings = False
            elif planet_type == 6:
                small_moon = rolldice(2, 6)
                large_moon = rolldice(1, 6) - 3
                giant_moon = rolldice(1, 6) - 4
        elif 5 > moonroll > 2:
            if planet_type == 2:
                small_moon = rolldice(1, 6) - 2
            elif planet_type == 3:
                small_moon = rolldice(1, 6) - 3
                medium_moon = rolldice(1, 6) - 3
            elif planet_type == 4:
                small_moon = rolldice(1, 6) - 2
                medium_moon = rolldice(1, 6) - 3
                large_moon = rolldice(1, 6) - 4
            elif planet_type == 5:
                small_moon = rolldice(5, 6)
                medium_moon = rolldice(1, 6) - 2
                large_moon = rolldice(1, 6) - 3
                if rolldice(1, 6) < 5:
                    rings = True
                else:
                    rings = False
            elif planet_type == 6:
                small_moon = rolldice(2, 6)
                medium_moon = rolldice(1, 6) - 2
                large_moon = rolldice(1, 6) - 3
                if rolldice(1, 6) < 4:
                    rings = True
                else:
                    rings = False
        elif moonroll > 4:
            if planet_type == 3:
                small_moon = rolldice(2, 6) - 4
                if rolldice(1, 6) < 2:
                    rings = True
                else:
                    rings = False
            elif planet_type == 4:
                small_moon = rolldice(2, 6)
                medium_moon = rolldice(1, 6) - 3
                if rolldice(1, 6) < 3:
                    rings = True
                else:
                    rings = False
            elif planet_type == 5:
                small_moon = rolldice(5, 6)
                medium_moon = rolldice(1, 6) - 3
                large_moon = rolldice(1, 6) - 4
                if rolldice(1, 6) < 5:
                    rings = True
                else:
                    rings = False
            elif planet_type == 6:
                small_moon = rolldice(2, 6)
                medium_moon = rolldice(1, 6) - 3
                large_moon = rolldice(1, 6) - 4
                if rolldice(1, 6) < 4:
                    rings = True
                else:
                    rings = False
    small_moon = int((abs(small_moon) + small_moon) / 2)
    medium_moon = int((abs(medium_moon) + medium_moon) / 2)
    large_moon = int((abs(large_moon) + large_moon) / 2)
    giant_moon = int((abs(giant_moon) + giant_moon) / 2)
    return small_moon, medium_moon, large_moon, giant_moon, rings


# Calculate actual data and create list of tuples
planet_type = []
planet_file = []
moon_file = []
terra_atmosphere = []
lifezone_check = []
lifezone_mod = []

i = 0
while i < len(total_system_populated):
    # Calculates the planet type by converting from string to integer
    planet_type.append(planet_type_dict[total_system_populated[i]])
    # Calculate planet details
    planet_file.append(Planetary_Object(planet_type[i], i))
    # Calculate moon details
    moon_file.append(Moons(planet_type[i]))
    # Determine if planet is in the life zone
    i += 1

# Translate tuple values from Planetary_Object into individual lists
dia_list = [dia_tuple[0] for dia_tuple in planet_file]
den_list = [den_tuple[1] for den_tuple in planet_file]
day_list = [day_tuple[2] for day_tuple in planet_file]
grav_list = [grav_tuple[3] for grav_tuple in planet_file]
esc_velocity_list = [esc_tuple[4] for esc_tuple in planet_file]
year_list = [year_tuple[5] for year_tuple in planet_file]

# Translate moon values from Moon into individual lists
small_moon = [small_tuple[0] for small_tuple in moon_file]
medium_moon = [medium_tuple[1] for medium_tuple in moon_file]
large_moon = [large_tuple[2] for large_tuple in moon_file]
giant_moon = [giant_tuple[3] for giant_tuple in moon_file]
ring = [ring_tuple[4] for ring_tuple in moon_file]


# Atmospheric Information for Terrestrial Planets
def atmosphere(planet_type, slot):
    pressure_options = {0: "Vacuum",
                        1: "Vacuum",
                        2: "Vacuum",
                        3: "Vacuum",
                        4: "Trace",
                        5: "Low",
                        6: "Low",
                        7: "Normal",
                        8: "Normal",
                        9: "High",
                        10: "High",
                        11: "Very High",
                        12: "Very High",
                        13: "Very High",
                        14: "Very High",
                        15: "Very High",
                        16: "Very High",
                        17: "Very High",
                        18: "Very High",
                        19: "Very High",
                        20: "Very High"}

    pressure_roll = rolldice(2, 6) - (2 * lifezone_check[slot])
    esc_velo_mod = (esc_velocity_list[slot] / 11186)
    pressure_roll = round(pressure_roll * esc_velo_mod)
    pressure = pressure_options[pressure_roll]

    # Calculate Habitability
    if pressure_roll < 5 or pressure_roll > 10:
        habitable = False
    else:
        if 10 >= pressure_roll >= 9 or 6 >= pressure_roll >= 5:
            lowhigh_press_check = 1
        else:
            lowhigh_press_check = 0
        if planet_type == 4:
            giant_terra = 1
        else:
            giant_terra = 0
        habit_roll = rolldice(3, 6)
        print("Habitability roll is: " + str(habit_roll) + " - " + str(lowhigh_press_check) +
              " - (2 * " + str(giant_terra) + ") + " + str(habit_mod))
        habit_roll = habit_roll - lowhigh_press_check - (2 * giant_terra) + int(habit_mod)
        if habit_roll >= 9:
            habitable = True
        else:
            habitable = False

    # Calculate Surface temperatures
    if pressure_roll < 5:
        r_mod = 1.0
    elif 4 < pressure_roll < 7:
        r_mod = 0.95
    elif 6 < pressure_roll < 9:
        r_mod = 0.9
    elif 8 < pressure_roll < 11:
        r_mod = 0.8
    elif pressure_roll > 10:
        r_mod = 0.5
    surf_temp = 277 * float(lum) ** 0.25 * math.sqrt(1 / (orbital_locations[slot] * r_mod))

    # Determine Habitable planet features
    if habitable:
        # Percent Water Calculation
        water_roll = round(rolldice(2, 6) * lifezone_mod[slot] * esc_velo_mod) + (3 * giant_terra)
        print("Water Roll modified by life zone (" + str(lifezone_mod[slot]) + "), escape velocity mod ("
              + str(esc_velo_mod) + ") + giant terrestrial mod (3 * " + str(giant_terra) + ")")
        if water_roll < 0:
            percent_water = 0
        elif water_roll == 0:
            percent_water = 5
        elif water_roll == 1:
            percent_water = 10
        elif water_roll == 2:
            percent_water = 20
        elif water_roll == 3:
            percent_water = 30
        elif 5 >= water_roll >= 4:
            percent_water = 40
        elif 7 >= water_roll >= 6:
            percent_water = 50
        elif water_roll == 8:
            percent_water = 60
        elif water_roll == 9:
            percent_water = 70
        elif water_roll == 10:
            percent_water = 80
        elif water_roll == 11:
            percent_water = 90
        elif water_roll >= 12:
            percent_water = 100

        # atmospheric condition
        atmosphere_roll = rolldice(2, 6) - (2 * giant_terra)
        if atmosphere_roll < 2:
            atmos_condition = "Toxic"
        elif 7 > atmosphere_roll > 1:
            atmos_condition = "Tainted"
        elif atmosphere_roll > 6:
            atmos_condition = "Breathable"

        # Highest Life Form
        lifeform_roll = rolldice(2, 6) + int(habit_mod)
        if lifeform_roll <= 0:
            lifeform = "Microbe"
        elif lifeform_roll == 1:
            lifeform = "Plants"
        elif lifeform_roll == 2:
            lifeform = "Insects"
        elif 5 > lifeform_roll > 2:
            lifeform = "Fish"
        elif 7 > lifeform_roll > 4:
            lifeform = "Amphibians"
        elif 9 > lifeform_roll > 6:
            lifeform = "Reptiles"
        elif 11 > lifeform_roll > 8:
            lifeform = "Birds"
        elif lifeform_roll > 10:
            lifeform = "Mammals"
    elif not habitable:
        percent_water = 0
        atmos_condition = "Toxic"
        lifeform = "None"
    return pressure, habitable, surf_temp, percent_water, atmos_condition, lifeform


i = 0

while i < len(total_system_populated):
    if float(OLZ_dist_au) >= orbital_locations[i] >= float(ILZ_dist_au):
        lifezone_check.append(0)  # True
    else:
        lifezone_check.append(1)  # False
    lifezone_mod.append((orbital_locations[i] - float(ILZ_dist_au)) / (float(OLZ_dist_au) - float(ILZ_dist_au)))
    # Use planet type to test for terrestrial planet atmosphere
    if planet_type[i] == 2 or planet_type[i] == 3 or planet_type[i] == 4:
        terra_atmosphere.append(atmosphere(planet_type[i], i))
    else:
        terra_atmosphere.append((False, False, False, 0, "Toxic", "None"))
    i += 1

# Translate tuple values into individual lists from atmosphere
pressure_list = [pressure[0] for pressure in terra_atmosphere]
habitable_list = [habitable[1] for habitable in terra_atmosphere]
surf_temp = [surf_temp[2] for surf_temp in terra_atmosphere]
percent_water_list = [percent_water[3] for percent_water in terra_atmosphere]
atmos_condition_list = [atmos_condition[4] for atmos_condition in terra_atmosphere]
lifeform_list = [lifeform[5] for lifeform in terra_atmosphere]

# Export planet data in csv file
j = 0
with open(starname + ".csv", "w", newline="") as csvfile:
    planetwriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    planetwriter.writerow(["Star Name: " + str(starname)])
    planetwriter.writerow(["Star Type: " + str(star_type[0]) + str(star_type[1]) + "V"])
    planetwriter.writerow(["Orbital slots: " + str(orbit_total)])
    planetwriter.writerow(["Star mass: " + str(mass) + " (Mstar/Msun)"])
    planetwriter.writerow(["Life zone bounds are " + str(ILZ_dist_au) + " AU to " + str(OLZ_dist_au) + " AU."])
    planetwriter.writerow(["Life Zone slots: " + str(life_system)])
    planetwriter.writerow(["Slot", "Distance (AU)", "Planetary Object", "Diameter (km)", "Density (g/cm^3)",
                           "Day Length (hours)", "Surface Gravity (G)", "Year Length (Earth Years)",
                           "Terrestrial Surface Temp (K)", "Terrestrial Atmospheric Pressure", "Habitable?",
                           "Percent Water", "Atmospheric Condition", "Highest Lifeform",
                           "Small Moons", "Medium Moons", "Large Rooms", "Giant Moons", "Rings"])
    while j < len(planet_type):
        planetwriter.writerow([j + 1, orbital_locations[j], total_system_populated[j], dia_list[j], den_list[j],
                               day_list[j], grav_list[j], year_list[j], surf_temp[j], pressure_list[j],
                               habitable_list[j],
                               percent_water_list[j], atmos_condition_list[j], lifeform_list[j],
                               small_moon[j], medium_moon[j], large_moon[j], giant_moon[j], ring[j]])
        j += 1

# Create Accompanying Graphic
WIDTH = 1500
HEIGHT = 600
tk = Tk()
frame = Frame(tk, width=WIDTH, height=HEIGHT)
frame.pack(expand=True, fill=BOTH)
canvas = Canvas(frame, width=WIDTH, height=HEIGHT, scrollregion=(0, 0, 8000, 600))
hbar = Scrollbar(frame, orient=HORIZONTAL)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=canvas.xview)
canvas.config(width=WIDTH, height=HEIGHT, background="Black")
canvas.config(xscrollcommand=hbar.set)
canvas.pack(side=LEFT, expand=True, fill=BOTH)
tk.title(starname)
frame.pack()


# Canvas will print the star on the left hand side with a diameter of 100 pixels (Sun)
# This diameter will eventually be normalized based on the sun's diameter
# The star's color will depend on the star type based on the dictionary below
def circle(canvas, x, y, r, color, outlinecolor):
    id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=outlinecolor)
    return id


def truncate(f, n):
    # Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * n)[:n]])


class Planet:
    def __init__(self, color, size, loc):
        self.shape = circle(canvas, round(loc), HEIGHT / 2, round(((size / 2) / 400)), color, "White")

starcolor = {"M": "Red",
             "K": "Orange",
             "G": "Yellow",
             "F": "Light Yellow",
             "A": "Ghost White",
             "B": "Turquoise1"}

planetcolor = {"Empty": "",
               "Asteroid Belt": "Gray60",
               "Dwarf Terrestrial Planet": "Dark Olive Green",
               "Terrestrial Planet": "Forest Green",
               "Giant Terrestrial Planet": "Dark Green",
               "Gas Giant": "LightGoldenrod1",
               "Ice Giant": "Cyan"}

star_graph = circle(canvas, 0, HEIGHT / 2, round(75 * float(radius)), starcolor[star_type[0]], "Black")
star_pos = canvas.coords(star_graph)
star_diameter = round(float(radius) * 2 * 696000)
star_radius_plot = float(radius) * 28
startext = canvas.create_text(100, HEIGHT / 2 + 100,
                              text="Star Name: " + str(starname) + "\nStar Type: " + str(star_type[0]) + str(
                                  star_type[1]) + "V\nMass: " + str(mass) + " Mstar/Msol\nDiameter: " + str(
                                  star_diameter) + " km", fill="White")
w = canvas.create_rectangle(canvas.bbox(startext), fill="Black")
canvas.tag_lower(w, startext)



planet_graph = []
orbit_circle = []
ring_circle = []
i = 0
while i < len(total_system_populated):
    orbit_circle.append(circle(canvas, 0, HEIGHT / 2, 500 + 500 * i, "", "White"))
    if ring[i]:
        ring_circle.append(circle(canvas, 500 + 500 * i, HEIGHT / 2, round((dia_list[i] / 2) / 400 + 10), "", "White"))
    planet_graph.append(Planet(planetcolor[total_system_populated[i]], dia_list[i], 500 + 500 * i))
    text = canvas.create_text(500 + 500 * i, HEIGHT / 2 + 100,
                              text=str(total_system_populated[i]) + "\nDiameter: " + str(
                                  dia_list[i]) + "km\nDistance: " +
                                   str(truncate(orbital_locations[i], 3)) + " AU\nHabitable: " +
                                   str(habitable_list[i]), fill="White")
    r = canvas.create_rectangle(canvas.bbox(text), fill="Black")
    canvas.tag_lower(r, text)
    i += 1

tk.mainloop()
