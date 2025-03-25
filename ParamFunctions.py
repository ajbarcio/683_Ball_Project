import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize as opt

motorTypes = {'example type': []}
g = 32.1740
volBattery = (2.5 * 7 * 7) * 0.000578704 # volume of battery (h x w x l in in3) to ft3 
batteryMass = 15 # lbs
structureDensity = 1.2 # lb/ft^3 ??
shellDensity = 51 # lb/ft^3 ??

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
    def __init__(self, radius):
        self.radius = radius
        
        self.batteries = Batteries(self.radius)
        self.motors    = Motors(self.batteries.number)

        self.volumePendulum = self.pendulum_volume()
        self.lengthPendulum = self.pendulum_length()

        self.massPendulum = self.pendulum_mass()
        self.massShell = self.mass_shell()
        
        self.mass = self.get_total_mass()

        self.radiusGravity = self.radius_gravity()
        # self.radius
        self.masses = {"Motors": self.motors.mass, 
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
        Cg_structure =  self.volumePendulum*structureDensity * (self.lengthPendulum*0.5) #half way along pendulum length
        if self.radius > 1.5:
            Cg_batteries = self.batteries.mass * (self.lengthPendulum - self.batteries.height) #midway between batteries
            Cg_actuators = self.motors.mass * (self.lengthPendulum - self.batteries.height*2 - self.motors.radius) #above batteries
            Cg_penalty = 0
        else:
            Cg_batteries = self.batteries.mass * (self.lengthPendulum - self.batteries.width/2) #midway between batteries
            Cg_actuators = self.motors.mass * (self.lengthPendulum - self.batteries.width - self.motors.radius) #above batteries
            Cg_penalty = 0.266
        return (Cg_structure + Cg_batteries + Cg_actuators) / self.massPendulum - Cg_penalty

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
        return self.motors.mass + self.batteries.mass + self.volumePendulum*structureDensity

    def get_total_mass(self):
        return self.massShell+self.massPendulum

def shellMass(radiusShell):
    return 4.0/3.0*np.pi*(radiusShell-(radiusShell-shellThickness(radiusShell)))

def shellThickness(radiusShell):
    if radiusShell > 1.5:
        return 1/4.0
    else:
        return 1/8.0
    
def main():
    # parse some arument for radius of ball
    print(Ball(1).masses)
    print(Ball(1).r_max())
    R = np.linspace(1,3,1001)
    slope = np.empty_like(R)
    i = 0
    for radius in R:
        testBall = Ball(radius)
        slope[i] = testBall.max_slope()
        i+=1
    plt.plot(R, slope)
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