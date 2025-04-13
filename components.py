from params import *
from materials import Material
import numpy as np

class Ballast:
    def __init__(self, thickness, material: Material, radius):
        self.material = material
        self.density = material.density
        self.thickness = thickness
        self.volume = np.pi*radius**2*thickness
        self.mass = self.volume*material.density

class Batteries:
    def __init__(self, radius):
        self.radius = radius
        self.number = self.num_batteries()
        self.mass = 15*self.number
        self.volume = self.number*volBattery 

        self.height = 2.5/12.0
        self.width  = 7  /12.0
        self.length = 7  /12.0

    def num_batteries(self):
        if self.radius > 1.5:
            return 4
        else:
            return 2

    def __str__(self):
        f"mass: {self.mass:.2f}, number: {self.number}, volume: {self.volume:.2f}"


class Motors:
    def __init__(self, torque, reduction, mass, radius, length):
        # self.num_batteries = num_batteries
        self.torque = torque*reduction
        self.mass   = mass
        self.radius = radius
        self.length = length

    def __str__(self):
        return f"{self.name} motor, mass: {self.mass:.2f}, \
                                    torque: {self.torque:.2f}"
                                    # volume: {self.volume:.2f}"

neo2ft   = Motors(3.6*0.74*2,  21.5, 2*.98,   1/12.0, 1)
gen1_6ft = Motors(6.03*0.74*2, 21,   2*5*2.2, 4/12.0, 1)

motorTypes = [neo2ft, gen1_6ft]
