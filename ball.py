from params import *
import numpy as np
from components import Batteries, Motors, Ballast
from components import neo2ft, gen1_6ft

class Ball:
    def __init__(self, radius, ballastThickness, ballastMaterial):
        self.radius = radius

        self.batteries = Batteries(self.radius)
        self.motors = self.select_motors()
        # self.motors    = Motors(self.batteries.number)

        self.volumePendulum = self.pendulum_volume()
        # self.lengthPendulum = self.pendulum_length()
        self.ballast = Ballast(ballastThickness, ballastMaterial, self.hub_rad)

        self.massPendulum = self.pendulum_mass()
        self.massShell = self.mass_shell()
        
        self.mass = self.get_total_mass()

        self.radiusGravity = self.radius_gravity()
        # self.radius
        self.outputMasses = {"Motors": self.motors.mass, 
                       "Batteries": self.batteries.mass,
                       "Pendulum Structure": self.volumePendulum*structureDensity,
                       "Pendulum Mass": self.massPendulum,
                       "Shell": self.massShell, 
                       "Total Ball Mass": self.mass}

    def ball_objective(self):
        return np.array([self.max_slope(), self.cost_factor()])

    def check_max_slope(self):
        return np.arcsin(self.r_max()/self.radius*np.sin(90*np.pi/180))*180/np.pi

    def gamma_possible(self):
        return np.arcsin(self.motors.torque/(self.massPendulum*self.radiusGravity))*180/np.pi

    def select_motors(self):
        if self.radius < designThreshold:
            return neo2ft
        else:
            # TODO: gen2_6ft?
            return gen1_6ft

    def r_max(self):
        return (self.radiusGravity*self.massPendulum)/self.mass

    def max_slope(self):
        return np.arcsin(self.torqueApplicable()/(self.radius*self.mass))*180/np.pi

    def cost_factor(self):
        return self.ballast.mass*self.ballast.material.costperpound

    def torqueApplicable(self):
        return min(self.motors.torque, self.radiusGravity*self.massPendulum)

    def radius_gravity(self):
        cgStructure =  self.volumePendulum*structureDensity * (self.lengthPendulum*0.5) #half way along pendulum length
        cgBallast   =  self.ballast.mass*(self.lengthPendulum-self.ballast.thickness/2)
        if self.radius > designThreshold:
            cgBatteries = self.batteries.mass * (self.lengthPendulum - self.batteries.height - self.ballast.thickness) #midway between batteries
            cgActuators = self.motors.mass * (self.lengthPendulum - self.batteries.height*2 - self.motors.radius - self.ballast.thickness) #above batteries
            cgPenalty = 0
        else:
            cgBatteries = self.batteries.mass * (self.lengthPendulum - self.batteries.width/2 - self.ballast.thickness) #midway between batteries
            cgActuators = self.motors.mass * (self.lengthPendulum - self.batteries.width - self.motors.radius - self.ballast.thickness) #above batteries
            cgPenalty = 0.266
        return (cgStructure + cgBatteries + cgActuators + cgBallast) / self.massPendulum - cgPenalty

    def mass_shell(self):
        massBedliner = 4.0/3.0*np.pi*(self.radius**3-(self.radius-self.thickness_shell())**3) * shellDensity # (8.75 * 0.133) #8.75 lb per gal, 0.133 ft3 per gal
        # print("Mass of bedliner", massBedliner)
        radiusShaft = self.radius/12 # R inches to feet
        thicknessShaft = 0.25/12
        massShaft = 169 * (2*self.radius* (radiusShaft**2 - (radiusShaft-thicknessShaft)**2) * np.pi)
        return massBedliner + massShaft + 20

    def thickness_shell(self):
        if self.radius > designThreshold:
            return 1/(4.0*12)
        else:
            return 1/(8.0*12)
        
    def pendulum_length(self):
        self.lengthPendulum = pendulumRadiusAllowance*self.radius
        return self.lengthPendulum
    
    def pendulum_volume(self):
        if self.radius > designThreshold:
            self.hub_rad = 11*0.0833
        else: 
            self.hub_rad = 9.5*0.0833
        return self.hub_rad**2 * np.pi * self.pendulum_length()

    def pendulum_mass(self):
        return self.motors.mass + self.batteries.mass + self.volumePendulum*structureDensity + self.ballast.mass 

    def get_total_mass(self):
        return self.massShell+self.massPendulum