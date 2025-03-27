from params import *
import numpy as np
from components import Batteries, Motors, Ballast, Structure
from components import neo2ft, gen1_6ft
import materials

class Ball:
    def __init__(self, radius, ballast_thk):
        self.radius = radius

        self.batteries = Batteries(self.radius)
        self.motors = self.select_motors()
        # self.motors    = Motors(self.batteries.number)

        self.volumePendulum = self.pendulum_volume()
        self.lengthPendulum = self.pendulum_length()

        if self.radius < designThreshold:
            structureMaterial = materials.nylon
            overhang = 4/12.0
        else:
            structureMaterial = materials.al6061
            overhang = 0
        
        self.pendulum = Structure(structureMaterial, self.hubRad, overhang, self.radius)
        self.ballast = Ballast(self.hubRad, ballast_thk, materials.tungsten)

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
        
    def check_max_slope(self):
        return np.arcsin(self.r_max()/self.radius*np.sin(90*np.pi/180))*180/np.pi

    def gamma_possible(self):
        return np.arcsin(self.motors.torque/(self.massPendulum*self.radiusGravity))*180/np.pi

    def select_motors(self):
        if self.radius < designThreshold:
            return neo2ft
        else:
            return gen1_6ft

    def r_max(self):
        return (self.radiusGravity*self.massPendulum)/self.mass

    def max_slope(self):
        return np.arcsin(self.torqueApplicable()/(self.radius*self.mass))*180/np.pi

    def torqueApplicable(self):
        return min(self.motors.torque, self.radiusGravity*self.massPendulum)

    def radius_gravity(self):
        # Define relevant locations:
        locationBallast     = self.lengthPendulum - self.ballast.thickness/2
        locationBatteries   = locationBallast     - ((self.batteries.height) 
                                                     if   self.radius > designThreshold 
                                                     else (self.batteries.width/2))
        locationSteerMotors = locationBatteries   - self.motors.radius
        locationDriveMotors = self.radius/12/2 + self.motors.radius
        locations = [self.pendulum.cg, locationBallast, locationBatteries, locationSteerMotors, locationDriveMotors]
        masses    = [self.pendulum.mass, self.ballast.mass, self.batteries.mass, self.motors.mass, self.motors.mass]
        numSum = 0
        for location, mass in zip(locations, masses):
            numSum += location*mass
        return numSum/np.sum(np.array(masses))
        # return (cgStructure + cgBatteries + cgActuators + cgBallast) / self.massPendulum - cgPenalty

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
        return 0.9*self.radius
    
    def pendulum_volume(self):
        if self.radius > designThreshold:
            self.hubRad = 22*0.0833
        else: 
            self.hubRad = 19*0.0833
        return self.hubRad**2 * np.pi * self.pendulum_length()

    def pendulum_mass(self):
        return self.motors.mass*2 + self.batteries.mass + self.pendulum.mass + self.ballast.mass 

    def get_total_mass(self):
        return self.massShell+self.massPendulum