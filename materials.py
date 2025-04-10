import numpy as np

psi2Pa = 6894.76

# CUSTOMARY UNITS!!!
# PSI

class Material:
    def __init__(self, name, density, thickness):
        self.name=name
        self.density=density
        self.thickness=thickness

    def __str__(self):
        return f"{self.name}"

# Initialize materials here
# Structure materials
nylon    = Material("Nylon",     8.74,  .25/12)
al6061   = Material("AL6061",  186.55,  .125/12)
# Ballast Materials
ss304    = Material("SS304",    490,     .0625/12)
copper   = Material("Copper",   559,     .25/12)
lead     = Material("Lead",     707.9,   1)
tungsten = Material("Tungsten", 1201.74, .03125/12)
osmium   = Material("Osmium",   1410.2,  .03125/12)

ballastMaterials = [ss304, copper, lead, tungsten, osmium]