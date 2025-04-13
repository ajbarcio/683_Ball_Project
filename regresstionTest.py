import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
from materials import ballastMaterials, copper
# from params import *
import params
from components import Ballast

from ball import Ball

# motorTypes = {'example type': []}
# g = 32.1740
# volBattery = (2.5 * 7 * 7) * 0.000578704 # volume of battery (h x w x l in in3) to ft3 
# batteryMass = 15 # lbs
# structureDensity = 1.2 # lb/ft^3 ??
# shellDensity     = 51 # lb/ft^3 ??

def match(slope, radius):
    slopeTarget = slope
    radius = radius
    def zero(x):
        structureDensity = x
        return Ball(radius, 0, ballastMaterials[0], params=[params.shellDensity, structureDensity]).max_slope() - slopeTarget
    # plt.plot(np.linspace(-1000,1000,11), zero(np.linspace(-1000,1000,11)))
    sol = opt.root_scalar(zero, bracket=[0,10000])
    return sol.x

def main():

    # print(match(7.5, 1))
    # print(match(9, 3))

    print(Ball(3, 0, ballastMaterials[0]).max_slope())
    print(Ball(1, 14.5/(np.pi*9.5**2*copper.density), copper).max_slope())

    # R = np.linspace(1,3,101)
    # materials = ballastMaterials
    # # print(B)
    # slope = np.zeros_like(R)
    # i = 0
    # for radius in R:
    #     # print(params.cgPenalty)
    #     testBall = Ball(radius, 0, ballastMaterials[0])
    #     slope[i] = testBall.max_slope()
    #     i+=1
    # # print(f"best slope angle for {material.name} is {np.max(slope):.4f}")
    # # Rg, Bg = np.meshgrid(R, B)
    
    # plt.figure()
    # plt.plot(R, slope)

    # try:
    #     plt.show()
    # except KeyboardInterrupt:
    #     return 0



if __name__ == "__main__":
    main()