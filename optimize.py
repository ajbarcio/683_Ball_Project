import numpy as np
from scipy.optimize import differential_evolution
import ball 



def optimize_ball_design():

    bounds = [
        (1, 3),                   #rad
        (0, 10),                  #ballast thickness
        (0, 10)      # material, idk how to discretize
    ]

    result = differential_evolution(
        ball.ball_objective,
        bounds,
        strategy='best1bin',
        maxiter=1000,
        popsize=15,
        tol=1e-6,
        polish=True
    )

if __name__ == '__main__':
    optimize_ball_design()
