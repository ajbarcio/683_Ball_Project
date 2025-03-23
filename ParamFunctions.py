import numpy as np

def PendLength(R):
    L_p = 0.9*R
    return L_p

def PendVolume(R):
    if R > 3:
        hub_rad = 22*0.0833
    else: 
        hub_rad = 19*0.0833
    V_p = hub_rad**2 * np.pi * PendLength(R)

    return V_p

def PendStructureMass(R):
    densityPend = 100
    StructureMass = PendVolume(R) * densityPend
    return StructureMass

def NumBatteries(R):
    volBattery = (2.5 * 7 * 7) * 0.000578704 # volume of battery (h x w x l in in3) to ft3 
    if vol > 4 * volBattery:
        return 4
    else:
        return 2
    
def ActuatorTorques(R):
    numBat = NumBatteries(R)
    if numBat == 4:
        stall_torque = 6.03 * 0.74
        mass_motor = 2 * 5 * 2.2 #actuator mass from kg to lb, 2 actuators on steer (drive is part of shell)
    elif numBat == 2:
        stall_torque = 3.6 * 0.74
        mass_motor  = 2 * 0.98 # just lbs from Neo Vortex Data sheet
    
    return [stall_torque, mass_motor]

def MassPend(R):
    actuatorTorque, massActuators = ActuatorTorques(R)
    massPend = massActuators + NumBatteries(R) * 15 + PendStructureMass(R)
    return massPend

def MassShell(R):
    massBedliner = 4.0/3.0*np.pi*(R-(R-shellThickness(R)))**3 * (8.75 * 0.133) #8.75 lb per gal, 0.133 ft3 per gal
    radiusShaft = R/12 # R inches to feet
    thicknessShaft = 0.25/12
    massShaft = 169 * (2*R* (radiusShaft - (radiusShaft-thicknessShaft))**2 * np.pi)
    return massBedliner + massShaft

def shellThickness(R):
    if R > 3:
        return 1/(4.0*12)
    else:
        return 1/(8.0*12)
    
def R_g(R):
    lengthPend = PendLength(R)
    structureMass = PendStructureMass(R)
    batteriesMass = NumBatteries(R) * 15
    actuatorsProperties = ActuatorTorques(R)
 
    Cg_structure =  structureMass * (lengthPend*0.5) #half way along pendulum length
    if R > 3: #batteries oriented sideways
        Cg_batteries =  batteriesMass * (lengthPend - 2.5/12) #midway between batteries
        Cg_actuators = actuatorsProperties[1] * (lengthPend - 5/12 - actuatorsProperties[2]) #above batteries
        Cg_penalty = 0
    else: #batteries oriented long ways
        Cg_batteries =  batteriesMass * (lengthPend - 3.5/12)
        Cg_actuators = actuatorsProperties[1] * (lengthPend - 7/12 - actuatorsProperties[2]) #above batteries
        Cg_penalty = 0.05 #penalty in feet due to known amount of mass above the center axis
    R_g = (Cg_structure + Cg_batteries + Cg_actuators) / (structureMass + batteriesMass + actuatorsProperties[1]) - Cg_penalty
 
    return R_g
 