import numpy as np

psi2Pa = 6894.76

# CUSTOMARY UNITS!!!
# PSI

class Material:
    def __init__(self, name, density, cost):
        self.name=name
        self.density=density
        self.costperpound = cost

    def __str__(self):
        return f"{self.name}"

# Initialize materials here
# Structure materials
nylon    = Material("Nylon",     8.74,   1)
al6061   = Material("AL6061",  186.55,   1) # garbage costs, these are structure materials and deprecated
# Ballast Materials
a36      = Material("a36",      491,     1.92)
ss304    = Material("SS304",    490,     8.50)
copper   = Material("Copper",   559,     15.50)
lead     = Material("Lead",     707.9,   3.00)
tungsten = Material("Tungsten", 1201.74, 125)
osmium   = Material("Osmium",   1410.2,  5840)

ballastMaterials = [a36, ss304, copper, lead, tungsten, osmium]