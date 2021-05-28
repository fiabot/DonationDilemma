from deap import gp
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import operator
import math
import random
import Agent as a
import Tournament

class GA:
    def __init__(self, max_gens, pop_size, xover, mut):

        self.max_gens = max_gens
        self.pop_size = pop_size
        self.xover = xover
        self.mut = mut

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", a.Agent, fitness=creator.FitnessMax)
        #creator.create("Tourament", Tournament.Tournament)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", creator.Individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, self.pop_size)

        #toolbox.register("tourament", creator.Tourament, )
        self.toolbox.register("evaluate", print, "Evaluating")  # <- set up method or evaluation
        self.toolbox.register("select", tools.selTournament, tournsize=3, fit_attr = "saving")  # <- select indivuals from a tourment style thingy
        self.toolbox.register("mate", a.mate)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", a.mutate)

        self.toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)) #<- I imagine this will cause problems
        self.toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

        #TODO add statitics
    def run(self):
        gen = 0
        pop = self.toolbox.population()
        while gen < self.max_gens:

            # Vary the population
            new_pop = algorithms.varAnd(pop, self.toolbox, self.xover, self.mut)

            #evaluate population
            self.toolbox.evalate(new_pop)

            #select indivuals
            pop = self.toolbox.select(new_pop, len(new_pop)) #TODO figure out what the fuck is going here
            #^ is what the co-evolution example had for selections, but doesn't this just select everyone?
            # I am so confused

            gen += 1
        return pop 


