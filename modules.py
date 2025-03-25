from params import *
import numpy as np

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
    def __init__(self, num_batteries):
        self.num_batteries = num_batteries
        self.torque = self.actuator_torques()
        self.mass   = self.actuator_masses()
        self.radius = self.actuator_radius()

    def actuator_radius(self):
        if self.num_batteries == 4:
            return 4/12.0
        elif self.num_batteries == 2:
            return 1/12.0

    def actuator_torques(self):
        if self.num_batteries == 4:
            self.reduction = 21
            return 6.03 * 0.74 * 2 * self.reduction
        elif self.num_batteries == 2:
            self.reduction = 21.5
            return 3.6 * 0.74 * 2 * self.reduction
            
    def actuator_masses(self):
        if self.num_batteries == 4:
            return 2 * 5 * 2.2 #actuator mass from kg to lb, 2 actuators on steer (drive is part of shell)
        elif self.num_batteries == 2:
            return 2 * 0.98 # just lbs from Neo Vortex Data sheet

    def __str__(self):
        return f"{self.name} motor, mass: {self.mass:.2f}, \
                                    torque: {self.torque:.2f}"
                                    # volume: {self.volume:.2f}"

class Ball:
    def __init__(self, radius, ballast):
        self.radius = radius
        self.ballast = ballast

        self.batteries = Batteries(self.radius)
        self.motors    = Motors(self.batteries.number)

        self.volumePendulum = self.pendulum_volume()
        self.lengthPendulum = self.pendulum_length()

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

    def r_max(self):
        return (self.radiusGravity*self.massPendulum)/self.mass

    def max_slope(self):
        return np.arcsin(self.torqueApplicable()/(self.radius*self.mass))*180/np.pi

    def torqueApplicable(self):
        return min(self.motors.torque, self.radiusGravity*self.massPendulum)

    def radius_gravity(self):
        cgStructure =  self.volumePendulum*structureDensity * (self.lengthPendulum*0.5) #half way along pendulum length
        cgBallast   =  self.ballast*self.lengthPendulum
        if self.radius > 1.5:
            cgBatteries = self.batteries.mass * (self.lengthPendulum - self.batteries.height) #midway between batteries
            cgActuators = self.motors.mass * (self.lengthPendulum - self.batteries.height*2 - self.motors.radius) #above batteries
            cgPenalty = 0
        else:
            cgBatteries = self.batteries.mass * (self.lengthPendulum - self.batteries.width/2) #midway between batteries
            cgActuators = self.motors.mass * (self.lengthPendulum - self.batteries.width - self.motors.radius) #above batteries
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
        if self.radius > 1.5:
            return 1/(4.0*12)
        else:
            return 1/(8.0*12)
        
    def pendulum_length(self):
        return 0.9*self.radius
    
    def pendulum_volume(self):
        if self.radius > 1.5:
            hub_rad = 22*0.0833
        else: 
            hub_rad = 19*0.0833
        return hub_rad**2 * np.pi * self.pendulum_length()

    def pendulum_mass(self):
        return self.motors.mass + self.batteries.mass + self.volumePendulum*structureDensity + self.ballast 

    def get_total_mass(self):
        return self.massShell+self.massPendulum