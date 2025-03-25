import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
from params import *

from modules import Ball

# motorTypes = {'example type': []}
# g = 32.1740
# volBattery = (2.5 * 7 * 7) * 0.000578704 # volume of battery (h x w x l in in3) to ft3 
# batteryMass = 15 # lbs
# structureDensity = 1.2 # lb/ft^3 ??
# shellDensity     = 51 # lb/ft^3 ??

def shellMass(radiusShell):
    return 4.0/3.0*np.pi*(radiusShell-(radiusShell-shellThickness(radiusShell)))

def shellThickness(radiusShell):
    if radiusShell > 1.5:
        return 1/4.0
    else:
        return 1/8.0
    
def main():

    R = np.linspace(1,3,101)
    # B = np.zeros_like(R)
    B = np.linspace(0,55,len(R))
    slope = np.zeros([len(R),len(R)])
    i = 0
    for radius in R:
        j = 0
        for ballast in B:
            testBall = Ball(radius, ballast)
            slope[j, i] = testBall.max_slope()
            j+=1
        i+=1
    Rg, Bg = np.meshgrid(R, B)
    # plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(Rg, Bg, slope)
    
    ax.set_xlabel("Ball Radius")
    ax.set_ylabel("Ballast Mass")
    ax.set_zlabel("Slope Angle")
    try:
        plt.show()
    except KeyboardInterrupt:
        return 0

    # print(testBall.mass)
    # print(testBall.masses)
    # print("")
    # print(testBall.radiusGravity)
    # print(testBall.gamma_possible())
    # print(testBall.torqueApplicable(), (testBall.radiusGravity*testBall.massPendulum))
    # print("")
    # print(testBall.max_slope())
    # print(testBall.check_max_slope())

if __name__ == "__main__":
    main()