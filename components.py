from params import *
import numpy as np
from materials import Material

# class Shell:
#     def __init__(self):
#         pass

class Ballast:
    def __init__(self, radius, thickness, material):
        self.radius = radius
        self.thickness = thickness
        self.material = material
        self.mass = self.get_mass()

    def get_mass(self):
        return self.radius**2 * np.pi * self.thickness

class Structure:
    def __init__(self, material: Material, hubcap, overhang, radius):
        self.material = material
        self.radius   = hubcap
        self.overhang = overhang
        self.length   = radius*0.9

        self.envelopeVolume = self.get_volume(0)
        self.mass = self.get_mass() 
        self.cg   = self.get_cg()

    def get_volume(self, reduction):
        return (self.radius-reduction)**2*np.pi*(self.overhang+self.length-2*reduction)
    
    def get_mass(self):
        # define structure mass as cylindrical shell of given material
        # with "shelf" for battery, ballast, motors, electronics, pitch center
        self.materialVolume = self.get_volume(0)-self.get_volume(self.material.thickness)
        self.materialVolume+= (self.radius-self.material.thickness)**2 * np.pi * self.material.thickness * 5
        return self.materialVolume*self.material.density

    def get_cg(self):
        return self.mass * (self.length-self.overhang)/2


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
