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
import time
import CustomAgents

MAX_HEIGHT = 4
TIMETHRES = 2
def evaluate(agents, num_tours, debug = False):
    """
    averaging the results of multiple tournaments
    with the same collection of agents
    :param agents: a collection of different agents
    :param num_tours: the amount of tournaments for a single collection of agents
    """
    start_time = time.perf_counter()
    for i in range(num_tours):
        if debug:
            timer = time.perf_counter() - start_time
            if(timer > TIMETHRES):
                print("Tourament", i)
        Tournament.run_2players(agents, debug = debug)
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

    def __init__(self, pop_size, xover, mut, elites, rand_agents = 20, human_agents = 20):
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
        creator.create("GenerousAgent", CustomAgents.GenerousAgent, fitness = creator.FitnessMax)
        creator.create("StingyAgent", CustomAgents.StingyAgent, fitness=creator.FitnessMax)
        creator.create("TitForTatAgent", CustomAgents.TitForTatAgent, fitness=creator.FitnessMax)
        creator.create("AveragingAgent", CustomAgents.AveragingAgent, fitness=creator.FitnessMax)
        creator.create("VengfulAgent", CustomAgents.VengefulAgent, fitness=creator.FitnessMax)
        #creator.create("Tourament", Tournament.Tournament)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", creator.Individual, max_height = MAX_HEIGHT)
        self.toolbox.register("random", creator.RandomAgent)
        self.toolbox.register("human", random.choice([creator.GenerousAgent, creator.StingyAgent, creator.TitForTatAgent,
                                                      creator.AveragingAgent, creator.VengfulAgent] ))
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
        self.human_agents = [self.toolbox.human() for i in range(human_agents)]

    def run(self, max_gens, debug = False):
        """
        the main performance
        :param max_gens: total number of generations for GA to perform
        """
        gen = 0
        pop = self.toolbox.population()
        ex_debug = False

        if debug:
            print(pop[0].tree)
            #print(self.toolbox.individual(tree =pop[0].tree))
        self.random_test = [a.RandAgent() for i in range(int(self.pop_size/2))]
        self.human_test = [self.toolbox.human() for i in range(int(self.pop_size / 2))]
        while gen < max_gens:

            # Vary the population -- not working bc mutate and xover return agents
            new_pop = algorithms.varAnd(pop, self.toolbox, self.xover, self.mut)
            #new_pop = pop

            #evaluate population
            self.toolbox.evaluate(new_pop + self.rand_agents + self.human_agents, debug = debug)

            record = self.stats.compile(new_pop)
            self.logbook.record(gen=gen, evals=len(new_pop), **record)

            if debug:
                #best = self.toolbox.get_best(new_pop)[0]
                print(self.logbook.stream)
                #print("Generation:", gen, "best fitness:", best.savings)
                #print("Tree", best.tree)
                if gen % 20 == 0:
                    best = self.toolbox.top_half(pop)

                    avg_agent, avg_rand = pop_v_pop(best, self.random_test, 30)
                    print("Agent Average:", avg_agent, "Random Average:", avg_rand)

                    avg_agent, avg_human= pop_v_pop(best, self.human_test, 30)
                    print("Agent Average:", avg_agent, "Human Average:", avg_human)

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
    ga = GA(1024, 0.3, 0.3, 100, rand_agents = 300, human_agents= 50)
    pop, log, toolbox = ga.run(1000, True)
    #get top half
    best = toolbox.top_half(pop)
    random = [a.RandAgent() for i in range(len(best))]
    human = [toolbox.human() for i in range(len(best))]

    #pickle population
    pop_trees = [agent.tree for agent in pop]
    pickle.dump(pop_trees, open("LastGeneration.p", "wb"))

    print()
    print("-------------------FINAL EVALUATIONS -------------------")
    print()
    #run random trials
    avg_agent, avg_rand = pop_v_pop(best, random, 50)
    print("Agent Average:", avg_agent, "Random Average:", avg_rand)
    avg_agent, avg_human = pop_v_pop(best, human, 50)
    print("Agent Average:", avg_agent, "Human Average:", avg_human)

    avg_rand, avg_human = pop_v_pop(random, human, 50)
    print("Random Average:", avg_rand, "Human Average:", avg_human)


    #display an agent
    print(best[0].tree)
    Graph.graphAgent(best[0], title = "Top half of Agents")
