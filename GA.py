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
import Graph
import pickle

MAX_HEIGHT = 9
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

def average_savings(pop):
    s = 0
    for a in pop:
        s += a.savings
    return s / len(pop)

def pop_v_pop(pop1, pop2, num_tours):
    total = pop1[:] + pop2[:]
    for i in range(num_tours):
        Tournament.run_2players(total)
    for a in total:
        a.savings = a.savings / num_tours


    return average_savings(pop1), average_savings(pop2)

def reset(agents):
    """
    takes a whole collection of agents and
    reverts them back to their original state
    :param agents: a collection of different agents
    """
    for a in agents:
        a.reset()


class GA:

    def __init__(self, pop_size, xover, mut, elites, rand_agents = 20):
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
        creator.create("RandomAgent", a.RandAgent, fitness = creator.FitnessMax)
        #creator.create("Tourament", Tournament.Tournament)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", creator.Individual, max_height = MAX_HEIGHT)
        self.toolbox.register("random", creator.RandomAgent)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, self.pop_size)

        #toolbox.register("tourament", creator.Tourament, )
        self.toolbox.register("evaluate", evaluate, num_tours = 30)  # <- set up method or evaluation
        self.toolbox.register("select", tools.selTournament, tournsize=3)  # <- select indivuals from a tourment style thingy
        self.toolbox.register("mate", a.mate, max_height = MAX_HEIGHT, toolbox = self.toolbox)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", a.mutate, expr=self.toolbox.expr_mut, max_height = MAX_HEIGHT)
        self.toolbox.register("get_elites", tools.selBest, k=self.elites)
        self.toolbox.register("get_best", tools.selBest, k=1)
        self.toolbox.register("top_half", tools.selBest, k = int(self.pop_size / 2))
        self.toolbox.register("reset", reset)

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "std", "min", "avg", "max"

        self.rand_agents = [self.toolbox.random() for i in range(rand_agents)]

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
            self.toolbox.evaluate(new_pop + self.rand_agents)

            record = self.stats.compile(new_pop)
            self.logbook.record(gen=gen, evals=len(new_pop), **record)

            if debug:
                #best = self.toolbox.get_best(new_pop)[0]
                print(self.logbook.stream)
                #print("Generation:", gen, "best fitness:", best.savings)
                #print("Tree", best.tree)

            # Elitism
            elites = self.toolbox.get_elites(pop)
            pop = elites
            #select indivuals
            #this will replace the previous generation, but with mostly good indivuals
            #because select will replace indivuals
            pop += self.toolbox.select(new_pop, len(new_pop) - len(elites))

            self.toolbox.reset(pop)

            gen += 1
        return pop, self.logbook, self.toolbox


if __name__ == "__main__":
    ga = GA(1024, 0.3, 0.3, 1)
    pop, log, toolbox = ga.run(10000, True)
    #get top half
    best = toolbox.top_half(pop)
    random = [a.RandAgent() for i in range(len(best))]

    #pickle population
    pop_trees = [agent.tree for agent in pop]
    pickle.dump(pop_trees, open("LastGeneration.p", "wb"))

    #run random trials
    avg_agent, avg_rand = pop_v_pop(best, random, 30)
    print("Agent Average:", avg_agent, "Random Average:", avg_rand)


    #display an agent
    print(best[0].tree)
    Graph.graphAgent(best[0], title = "Top half of Agents")
