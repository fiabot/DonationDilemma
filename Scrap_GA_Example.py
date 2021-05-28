#Note, this is a test example
#this it NOT my code, I just put it here to test Deap functions
from deap import gp
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import operator
import math
import random

# This first part is creaing the operators
# and terminals that the GP will be able to use
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))

pset.renameArguments(ARG0='x')

# this part I am a little more confused about
# it seems that Deap relies on this creator and toolbox
# comands. Here we are essesiantly defining the funcitons
# that we need for the GA, what the indivuals look like, et.c
creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) #Simple minization problem, set to positive 1 for max
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin) #an indivual will be a gp.primative tree in this case

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2) #expression of the tree, which is different from tree itself. Somehow
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr) # to create an indivual, call on the data in "expr" on the method in "indivual
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual, points): #<- this is just the fitness function
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    return math.fsum(sqerrors) / len(points), # <-- deap doesn't like non-tuples

toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-10,10)]) #<- set up method or evaluation
toolbox.register("select", tools.selTournament, tournsize=3) #<- select indivuals from a tourment style thingy
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

stats_fit = tools.Statistics(lambda ind: ind.fitness.values) #<- what stats do you want the ga to record
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
mstats.register("min", numpy.min)
mstats.register("max", numpy.max)

pop = toolbox.population(n=300)

algorithms.varAnd(pop, toolbox,0.5, 0.5)
hof = tools.HallOfFame(1)
pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 40, stats=mstats,
                               halloffame=hof, verbose=True)
