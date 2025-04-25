import numpy as np
from scipy.optimize import differential_evolution, NonlinearConstraint, OptimizeResult, Bounds, minimize
from ball import Ball 
from materials import ballastMaterials
from params import *

# def custom_strategy_fn(candidate, population, rng=None):
#     parameter_count = population.shape(-1)
#     mutation, recombination = 0.7, 0.9
#     trial = np.copy(population[candidate])
#     fill_point = rng.choice(parameter_count)
#     pool = np.arange(len(population))
#     rng.shuffle(pool)
#     # two unique random numbers that aren't the same, and
#     # aren't equal to candidate.
#     idxs = []
#     while len(idxs) < 2 and len(pool) > 0:
#         idx = pool[0]
#         pool = pool[1:]
#         if idx != candidate:
#             idxs.append(idx)
#     r0, r1 = idxs[:2]
#     bprime = (population[0] + mutation *
#               (population[r0] - population[r1]))
#     crossovers = rng.uniform(size=parameter_count)
#     crossovers = crossovers < recombination
#     crossovers[fill_point] = True
#     trial = np.where(crossovers, bprime, trial)
#     return trial

def optimize_ball_design():

    bounds = [
        (1, 3),                   #rad
        (0, 0.5),                  #ballast thickness
        (0, len(ballastMaterials)-1)      # material, idk how to discretize
    ]

    def cost(designVector):
        radius, thickness, material_index = designVector
        i = int(np.round(material_index, 0))
        testBall = Ball(radius, thickness, ballastMaterials[i])
        return testBall.cost()

    # def ball_objective(designVector):
    #     radius, thickness, material_index = designVector
    #     i = int(np.round(material_index, 0))
    #     testBall = Ball(radius, thickness, ballastMaterials[i])
    #     return -testBall.ball_objective()

    def ball_objective(designVector):
        radius, thickness, material_index = designVector
        i = int(np.round(material_index, 0))
        testBall = Ball(radius, thickness, ballastMaterials[i])
        return -testBall.ball_objective()

    costConstraint = NonlinearConstraint(cost, 0, 2000)

    # def ball_callback(intermediate_result: OptimizeResult):
    #     objectiveVectors = []
    #     for designVector in intermediate_result.population:
    #         radius, thickness, material_index = designVector
    #         i = int(np.round(material_index, 0))
    #         callbackBall = Ball(radius, thickness, ballastMaterials[i])
    #         objectiveVector = [callbackBall.slope_factor(), callbackBall.cost_factor()]
    #         objectiveVectors.append(objectiveVector)
    #     return objectiveVectors

    result = differential_evolution(
        ball_objective,
        bounds,
        strategy='best1bin',
        maxiter=1000,
        popsize=85,
        tol=1e-6,
        constraints=costConstraint,
        polish=False
    )

    return result

def weighted_objective(x):
    radius, thickness, m_idx = x
    mat_i = int(np.clip(np.round(m_idx), 0, len(ballastMaterials)-1))
    ball = Ball(radius, thickness, ballastMaterials[mat_i])
    return -slope_factor * ball.max_slope() + cost_factor * ball.cost()

def cost_constraint_fun(x):
    radius, thickness, m_idx = x
    mat_i = int(np.clip(np.round(m_idx), 0, len(ballastMaterials)-1))
    return Ball(radius, thickness, ballastMaterials[mat_i]).cost()

def compute_lagrange_sensitivities(cost_limit, x0):
    bnds    = Bounds([1.0, 0.0, 0.0],
                     [3.0, 1.0, len(ballastMaterials)-1])
    cost_con = NonlinearConstraint(cost_constraint_fun, 0, cost_limit)

    lagrange_multipliers = minimize(lambda x: weighted_objective(x),
                   x0=np.array(x0),
                   method='trust-constr',
                   bounds=bnds,
                   constraints=[cost_con],
                   options={'verbose': 0})

    sensitivities = lagrange_multipliers.v


    sens_cost = -sensitivities[0][0]
    sens_radius = -sensitivities[1][0]
    sens_ballastThickness = -sensitivities[1][1]
    sens_ballastMaterial = -sensitivities[1][2]

    print(f"Sensitivity for the cost constraint from negative lagrange multipliers is {sens_cost:.5f}.")
    print(f"Sensitivity for the radius constraint from negative lagrange multipliers is {sens_radius:.2f}.")
    print(f"Sensitivity for the ballast thickness constraint from negative lagrange multipliers is {sens_ballastThickness:.2f}.")
    print(f"Sensitivity for the ballast material constraint from negative lagrange multipliers is {sens_ballastMaterial:.2f}.")

    return lagrange_multipliers

if __name__ == '__main__':
    result = optimize_ball_design()
    print(result)
    resultVector = result.x
    resultVector[-1] = np.round(resultVector[-1], 0)
    material = ballastMaterials[int(resultVector[-1])]
    print(f"design a {resultVector[0]*2} ft ball, with {resultVector[1]*12} inches of {material} ballast")
    
    resultBall = Ball(resultVector[0], resultVector[1], material)
    print(resultBall.max_slope())
    print(resultBall.cost())
    print()
    print(np.linalg.norm([resultBall.lengthPendulum, resultBall.hubRad]))
    print(resultVector[0])

    x0 = resultVector.copy()
    x0[2] = int(np.clip(x0[2], 0, len(ballastMaterials)-1))
    compute_lagrange_sensitivities(
        cost_limit = cost_limit,
        x0         = x0
    )
