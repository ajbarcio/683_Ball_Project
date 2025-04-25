from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Choice
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import RankAndCrowdingSurvival

from pymoo.visualization.scatter import Scatter

from ball import Ball
from materials import ballastMaterials

class MultiObjectiveMixedVariableProblem(ElementwiseProblem):
    def __init__(self, **kwargs):
        vars = {
            "radius": Real(bounds=(1, 3)),
            "ballastThickness": Real(bounds=(0,1)),
            "ballastMaterial": Choice(options=ballastMaterials)
        }
        super().__init__(vars=vars, n_obj=2, n_ieq_constr=0, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
        radius, ballastThickness, ballastMaterial = X["radius"], X["ballastThickness"], X["ballastMaterial"]

        evaluationBall = Ball(radius, ballastThickness, ballastMaterial)
        # out["maxAngleFactor"] = evaluationBall.slope_factor()
        # out["costFactor"]     = evaluationBall.cost_factor()
        out["F"] = [-evaluationBall.max_slope(), evaluationBall.cost()]

problem   = MultiObjectiveMixedVariableProblem()
algorithm = MixedVariableGA(pop_size=100, survival=RankAndCrowdingSurvival())

res = minimize(problem, algorithm, termination=('n_evals', 1000),
               seed = 1, verbose=False)

plot = Scatter(labels = ["Slope","Cost"], title = "RoboBall Optimizer Pareto Front")
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()

# print(f"Best Solution Found: {res.X} gives {res.F}")