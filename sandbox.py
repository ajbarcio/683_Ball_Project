import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
from materials import ballastMaterials
from params import *
from components import Ballast

from StatProfiler import SSProfile

from ball import Ball

# motorTypes = {'example type': []}
# g = 32.1740
# volBattery = (2.5 * 7 * 7) * 0.000578704 # volume of battery (h x w x l in in3) to ft3 
# batteryMass = 15 # lbs
# structureDensity = 1.2 # lb/ft^3 ??
# shellDensity     = 51 # lb/ft^3 ??

def main():

    R = np.linspace(1,3,101)
    materials = ballastMaterials
    # print(B)
    slope = np.zeros_like(R)
    i = 0
    for radius in R:
        # print(params.cgPenalty)
        SSProfile("balleval").tic()
        testBall = Ball(radius, 0, ballastMaterials[0])
        slope[i] = testBall.max_slope()

        if testBall.infeasibleFlag:
            slope[i] = 0

        SSProfile("balleval").toc()
        i+=1
    # print(f"best slope angle for {material.name} is {np.max(slope):.4f}")
    # Rg, Bg = np.meshgrid(R, B)
    # print(slope)
    plt.figure()
    plt.plot(R, slope)


    R = np.linspace(1,3,101)
    # B = np.zeros_like(R)
    B = np.linspace(0,.5,len(R))
    materials = ballastMaterials
    # print(B)
    k = 0
    for material in materials:
        slope = np.zeros([len(R),len(R)])
        cost = np.zeros([len(R),len(R)])
        objective = np.zeros([len(R),len(R)])
        i = 0
        for radius in R:
            j = 0
            for ballastThickness in B:
                SSProfile("balleval").tic()
                testBall = Ball(radius, ballastThickness, material)
                slope[j, i] = testBall.max_slope()
                cost[j, i] = testBall.cost_factor()
                objective[j, i] = testBall.ball_objective()
                if testBall.infeasibleFlag:
                    slope[j, i] = 0
                SSProfile("balleval").toc()
                j+=1
            i+=1
        print(f"best slope angle for {material.name} is {np.max(slope):.4f}")
        # print(f"this occurs at {np.argmax(slope)}")
        Rg, Bg = np.meshgrid(R, B)
        
        plt.figure(f"slope, material: {material.name}")
        ax = plt.axes(projection='3d')
        ax.plot_surface(Rg, Bg*12, slope)
        
        ax.set_xlabel("Ball Radius (ft)")
        ax.set_ylabel("Ballast Thickness (in)")
        ax.set_zlabel("Slope Angle (deg)")

        # plt.figure(f"cost, material: {material.name}")
        # ax = plt.axes(projection='3d')
        # ax.plot_surface(Rg, Bg*12, cost)
        
        # ax.set_xlabel("Ball Radius (ft)")
        # ax.set_ylabel("Ballast Thickness (in)")
        # ax.set_zlabel("Cost Factor ($)")

        # plt.figure(f"objective, material: {material.name}")
        # ax = plt.axes(projection='3d')
        # ax.plot_surface(Rg, Bg*12, objective)
        
        # ax.set_xlabel("Ball Radius (ft)")
        # ax.set_ylabel("Ballast Thickness (in)")
        # ax.set_zlabel("Objective (unitless)")

        k+=1

    try:
        plt.show()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()