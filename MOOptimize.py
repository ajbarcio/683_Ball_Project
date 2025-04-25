from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Choice
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import RankAndCrowdingSurvival

from pymoo.visualization.scatter import Scatter

from ball import Ball
from materials import ballastMaterials, osmium, tungsten

from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib.cm import get_cmap

mpl.rcParams['figure.figsize'] = [7, 4.8]

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

res = minimize(problem, algorithm, termination=('n_gen', 500),
               seed = 1, verbose=False)

# plot = Scatter()
# plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
# # print(res.n_gen)
# plot.add(res.F, facecolor="none", edgecolor="red")
# plot.show()
# print(f"Best Solution Found: {res.X} gives {res.F}")

# Extract F and X
F = res.F
X = res.X  # res.X is likely a structured array or list of dicts, need to inspect

# Ensure X is iterable and we can get ballastMaterial
ballast_types = [x["ballastMaterial"] for x in X]

# Get unique ballast materials
unique_ballast_types = list(set(ballast_types))
print([type.__str__() for type in unique_ballast_types])
# Create color map
cmap = get_cmap("tab10")  # Or any other colormap
color_map = {b: cmap(i) for i, b in enumerate(unique_ballast_types)}

materialExcludesNone = []
materialExcludesOsm  = [osmium]
materialExcludesTung = [osmium, tungsten]

allMaterialExcludes = [materialExcludesNone, materialExcludesOsm, materialExcludesTung]

# Plot with color coding

for materialExcludes in allMaterialExcludes:
    fig, ax = plt.subplots()
    for i in range(len(F)):
        ballast = ballast_types[i]
        if not ballast in materialExcludes:
            ax.scatter(-F[i, 0], F[i, 1], color=color_map[ballast], label=ballast if ballast not in ballast_types[:i] else "")

    # Optional: add legend for ballast types
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Remove duplicates
    ax.legend(by_label.values(), by_label.keys())

    ax.set_xlabel("Objective 1: Max Slope (°)")
    ax.set_ylabel("Objective 2: Cost ($)")
    ax.set_title("Non-Dominated Set of Objectives")
plt.show()