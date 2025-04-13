import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
from materials import ballastMaterials
from params import *
from components import Ballast

from ball import Ball

# motorTypes = {'example type': []}
# g = 32.1740
# volBattery = (2.5 * 7 * 7) * 0.000578704 # volume of battery (h x w x l in in3) to ft3 
# batteryMass = 15 # lbs
# structureDensity = 1.2 # lb/ft^3 ??
# shellDensity     = 51 # lb/ft^3 ??

def main():

    R = np.linspace(1,3,101)
    # B = np.zeros_like(R)
    B = np.linspace(0,.5,len(R))
    materials = ballastMaterials
    # print(B)
    k = 0
    for material in materials:
        slope = np.zeros([len(R),len(R)])
        i = 0
        for radius in R:
            j = 0
            for ballastThickness in B:
                testBall = Ball(radius, ballastThickness, material)
                slope[j, i] = testBall.max_slope()
                j+=1
            i+=1
        print(f"best slope angle for {material.name} is {np.max(slope):.4f}")
        Rg, Bg = np.meshgrid(R, B)
        
        plt.figure(f"material: {material.name}")
        ax = plt.axes(projection='3d')
        ax.plot_surface(Rg, Bg*12, slope)
        
        ax.set_xlabel("Ball Radius (ft)")
        ax.set_ylabel("Ballast Thickness (in)")
        ax.set_zlabel("Slope Angle (deg)")

        k+=1

    try:
        plt.show()
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    main()