from params import *
import numpy as np
from components import Batteries, Motors, Ballast
from components import neo2ft, gen1_6ft
from materials import osmium


class Ball:
    def __init__(self, radius, ballastThickness, ballastMaterial, params=[shellDensity, structureDensity]):
        self.radius = radius
        self.ballastThickness = ballastThickness
        self.shellDensity = params[0]
        self.structureDensity = params[1]
        # print(self.shellDensity, self.structureDensity)

        self.batteries = Batteries(self.radius)
        self.motors = self.select_motors()
        # self.motors    = Motors(self.batteries.number)

        self.volumePendulum = self.pendulum_volume()
        # self.lengthPendulum = self.pendulum_length()
        self.ballast = Ballast(ballastThickness, ballastMaterial, self.hubRad)

        self.massPendulum = self.pendulum_mass()
        self.massShell = self.mass_shell()
        
        self.mass = self.get_total_mass()

        self.radiusGravity = self.radius_gravity()
        # self.radius
        self.outputMasses = {"Motors": self.motors.mass, 
                       "Batteries": self.batteries.mass,
                       "Pendulum Structure": self.volumePendulum*self.structureDensity,
                       "Pendulum Mass": self.massPendulum,
                       "Shell": self.massShell, 
                       "Total Ball Mass": self.mass}

    def ball_objective(self):
        weights = np.array([1,-1])
        objectiveVector = self.ball_objective_vector()
        return (objectiveVector.dot(weights))

    def ball_objective_vector(self):
        return np.array([self.slope_factor(), self.cost_factor()])

    def gamma_possible(self):
        return np.arcsin(self.motors.torque/(self.massPendulum*self.radiusGravity))*180/np.pi

    def select_motors(self):
        stackupHeight = self.ballastThickness+self.batteries.height+gen1_6ft.radius*2
        pendulumLength = self.pendulum_length()
        if pendulumLength - stackupHeight > gen1_6ft.radius*2:
            return gen1_6ft
        else:
            return neo2ft

    def r_max(self):
        return (self.radiusGravity*self.massPendulum)/self.mass

    def max_slope(self):
        return np.arcsin(self.torqueApplicable()/(self.radius*self.mass))*180/np.pi

    def slope_factor(self):
        return self.max_slope()*slope_factor

    def cost(self):
        return self.ballast.mass*self.ballast.material.costperpound

    def cost_factor(self):
        # factor = (np.pi*1*self.hubRad**2)*osmium.density
        return self.cost()*cost_factor

    def torqueApplicable(self):
        return min(self.motors.torque, self.radiusGravity*self.massPendulum)

    def radius_gravity(self):
        cgStructure =  self.volumePendulum*self.structureDensity * (self.lengthPendulum*0.5) #half way along pendulum length
        cgBallast   =  self.ballast.mass*(self.lengthPendulum-self.ballast.thickness/2)
        if self.motors == gen1_6ft:
            cgBatteries = self.batteries.mass * (self.lengthPendulum - self.batteries.height - self.ballast.thickness) #midway between batteries
            cgActuators = self.motors.mass * (self.lengthPendulum - self.batteries.height*2 - self.motors.radius - self.ballast.thickness) #above batteries
            cgPenaltyMult = 0
        else:
            cgBatteries = self.batteries.mass * (self.lengthPendulum - self.batteries.width/2 - self.ballast.thickness) #midway between batteries
            cgActuators = self.motors.mass * (self.lengthPendulum - self.batteries.width - self.motors.radius - self.ballast.thickness) #above batteries
            cgPenaltyMult = 1
        return (cgStructure + cgBatteries + cgActuators + cgBallast) / self.massPendulum - cgPenalty*cgPenaltyMult

    def mass_shell(self):
        # print("Mass of bedliner", massBedliner)
        radiusShaft = self.radius/12 # R inches to feet
        if self.motors == gen1_6ft:
            radiusShaft = 6/12.0
        else:
            radiusShaft = 2/12.0
        thicknessShaft = 0.25/12
        massShaft = 169 * (2*self.radius* (radiusShaft**2 - (radiusShaft-thicknessShaft)**2) * np.pi)
        self.mass = self.massPendulum+massShaft
        massBedliner = 4.0/3.0*np.pi*(self.radius**3-(self.radius-self.thickness_shell())**3) * self.shellDensity # (8.75 * 0.133) #8.75 lb per gal, 0.133 ft3 per gal
        return massBedliner + massShaft + 20

    def thickness_shell(self):
        m1, m2 = 86.2, 339.5
        t1, t2 = 1/8.0*12, 1/4.0*12

        m = (t2-t1)/(m2-m1)
        b = t1-m*m1

        return m*self.mass + b
        
    def pendulum_length(self):
        self.lengthPendulum = pendulumRadiusAllowance*self.radius
        return self.lengthPendulum
    
    def pendulum_volume(self):
        if self.motors == gen1_6ft:
            self.hubRad = 11*0.0833 # Could minimize this?
        else: 
            self.hubRad = 9.5*0.0833
        return self.hubRad**2 * np.pi * self.pendulum_length()

    def pendulum_mass(self):
        return self.motors.mass + self.batteries.mass + self.volumePendulum*self.structureDensity + self.ballast.mass 

    def get_total_mass(self):
        return self.massShell+self.massPendulum