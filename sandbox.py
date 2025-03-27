import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt
from params import *

from ball import Ball

def ballast_test():
    testBall = Ball(3,1)
    print(testBall.ballast.radius, testBall.ballast.thickness, testBall.ballast.mass)

def main():

    R = np.linspace(1,3,101)
    # B = np.zeros_like(R)
    B = np.linspace(0,0.5,len(R))
    rmaxes = np.empty_like(R)
    slope = np.zeros([len(R),len(R)])
    mass = np.zeros([len(R),len(R)])
    i = 0
    for radius in R:
        j = 0
        for ballast in B:
            testBall = Ball(radius, ballast)
            # if ballast == 0:
            # print(testBall.radius, testBall.outputMasses)
                # pass
            slope[j, i] = testBall.max_slope()
            mass [j, i] = testBall.mass
            j+=1
        i+=1
    Rg, Bg = np.meshgrid(R, B)
    # plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(Rg, Bg, slope)
    
    ax.set_xlabel("Ball Radius")
    ax.set_ylabel("Ballast Thickness")
    ax.set_zlabel("Slope Angle")
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(Rg, Bg, mass)
    
    ax.set_xlabel("Ball Radius")
    ax.set_ylabel("Ballast Thickness")
    ax.set_zlabel("Mass")

    plt.figure()
    plt.plot(R, slope[0,:])

    print(slope[0,0])
    print(slope[0,-1])

    try:
        plt.show()
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    # ballast_test()
    main()