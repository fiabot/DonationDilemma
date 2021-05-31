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


def evaluate(agents, num_tours):
    """
    averaging the results of multiple tournaments
    with the same collection of agents
    :param agents: a collection of different agents
    :param num_tours: the amount of tournaments for a single collection of agents
    """
    for i in range(num_tours):
        Tournament.run_2players(agents)
    for a in agents:
        a.fitness.values = a.savings / num_tours,


def reset(agents):
    """
    takes a whole collection of agents and
    reverts them back to their original state
    :param agents: a collection of different agents
    """
    for a in agents:
        a.reset()


class GA:

    def __init__(self, pop_size, xover, mut, elites):
        """
        main contructor for the genetic algorithm
        :param pop_size: number of agents in the pop
        :param xover: crossover rate
        :param mut: mutation rate
        :param elites: number of elites to maintain
        """

        self.pop_size = pop_size
        self.xover = xover
        self.mut = mut
        self.elites = elites

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", a.Agent, fitness=creator.FitnessMax)
        #creator.create("Tourament", Tournament.Tournament)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", creator.Individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, self.pop_size)

        #toolbox.register("tourament", creator.Tourament, )
        self.toolbox.register("evaluate", evaluate, num_tours = 10)  # <- set up method or evaluation
        self.toolbox.register("select", tools.selTournament, tournsize=3)  # <- select indivuals from a tourment style thingy
        self.toolbox.register("mate", a.mate, max_height = 17, toolbox = self.toolbox)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", a.mutate, expr=self.toolbox.expr_mut, max_height = 17)
        self.toolbox.register("get_elites", tools.selBest, k=self.elites)
        self.toolbox.register("get_best", tools.selBest, k=1)
        self.toolbox.register("reset", reset)

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "std", "min", "avg", "max"


    def run(self, max_gens, debug = False):
        """
        the main performance
        :param max_gens: total number of generations for GA to perform
        """
        gen = 0
        pop = self.toolbox.population()

        if debug:
            print(pop[0].tree)
            #print(self.toolbox.individual(tree =pop[0].tree))
        while gen < max_gens:

            # Vary the population -- not working bc mutate and xover return agents
            new_pop = algorithms.varAnd(pop, self.toolbox, self.xover, self.mut)
            #new_pop = pop

            #evaluate population
            self.toolbox.evaluate(new_pop)

            record = self.stats.compile(new_pop)
            self.logbook.record(gen=gen, evals=len(new_pop), **record)

            if debug:
                #best = self.toolbox.get_best(new_pop)[0]
                print(self.logbook.stream)
                #print("Generation:", gen, "best fitness:", best.savings)
                #print("Tree", best.tree)

            #Elitism
            elites = self.toolbox.get_elites(new_pop)
            pop = elites

            #select indivuals
            #this will replace the previous generation, but with mostly good indivuals
            #because select will replace indivuals
            pop += self.toolbox.select(new_pop, len(new_pop) - len(elites))

            self.toolbox.reset(pop)

            gen += 1
        return pop, self.logbook


if __name__ == "__main__":
    ga = GA(30, 0.5, 0.5, 1)
    pop, log = ga.run(100, True)
    #Run random tourament
    print("Random Game")

    rand = a.RandAgent()
    agents = pop[:]
    agents.append(rand)
    Tournament.run_2players(agents)
    print("Agent savings:", agents[0].savings, ", rand savings", rand.savings)
