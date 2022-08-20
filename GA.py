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
import PrisonerAgent as p
import Tournament
import Graph
import pickle
import time
import CustomAgents
import matplotlib.pyplot as plt
import RoundRobin
import CustomPrisoners
# new comment here! 
MAX_HEIGHT = 4
TIMETHRES = 5
def evaluate(agents, num_tours,debug = False, donation = True, indivual = True):
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
        if donation:
            Tournament.run_2players(agents, debug = debug)
        else:
            RoundRobin.round_robin(agents)
    for a in agents:
        if indivual:
            a.fitness.values = a.savings / num_tours,
        else:
            a.savings = a.savings / num_tours,


def average_savings(pop, donation = True):
    """
    Takes a given population of agents and
    calculates the average of all their savings
    :param pop: the selected given population
    :param donation: boolean stating whether its the donations or prisoner dilemma
    :return: the average savings for the given pop
    """
    s = 0
    for a in pop:
            s += a.savings
    return s / len(pop)

def pop_v_pop(pop1, pop2, num_tours, donation = True):
    """
    challenges two populations against each other
    and perpares their average savings for future comparison
    :param pop1: a given population
    :param pop2: another given population
    :param num_tours: number of iterations for either tournament or round robins
    :param donations: boolean stating whether its the donations or prisoner dilemma
    :return: a tuple of average_savings for both pops
    """
    total = pop1[:] + pop2[:]
    for i in range(num_tours):
        if donation:
            Tournament.run_2players(total)
        else:
            RoundRobin.round_robin(total)
    for a in total:
        a.savings = a.savings / num_tours
    return average_savings(pop1, donation), average_savings(pop2, donation)

def reset(agents):
    """
    takes a whole collection of agents and
    reverts them back to their original state
    :param agents: a collection of different agents
    """
    for a in agents:
        a.reset()


class GA:

    def __init__(self, pop_size, xover, mut, elites, rand_agents = 20, human_agents = 20, donation = True):
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

        if (donation):
            self.BuildDonationTools(rand_agents, human_agents)
        else:
            self.BuildPrisonTools(rand_agents, human_agents)


    def BuildDonationTools(self, rand_agents, human_agents):
        """
        perpares the tools necessary for the GP to evolve
        agents belonging to Donations Dilemma experimentation
        :param rand_agents: agents that give random donation(s)
        :param human_agents: agents with a algorithm guiding their donation(s)
        """
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", a.Agent, fitness=creator.FitnessMax)
        creator.create("RandomAgent", CustomAgents.RandAgent, fitness=creator.FitnessMax)
        creator.create("GenerousAgent", CustomAgents.GenerousAgent, fitness=creator.FitnessMax)
        creator.create("StingyAgent", CustomAgents.StingyAgent, fitness=creator.FitnessMax)
        creator.create("TitForTatAgent", CustomAgents.TitForTatAgent, fitness=creator.FitnessMax)
        creator.create("AveragingAgent", CustomAgents.AveragingAgent, fitness=creator.FitnessMax)
        creator.create("VengfulAgent", CustomAgents.VengefulAgent, fitness=creator.FitnessMax)
        # creator.create("Tourament", Tournament.Tournament)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", creator.Individual, max_height=MAX_HEIGHT)
        self.toolbox.register("random", creator.RandomAgent)
        self.toolbox.register("human",
                              random.choice([creator.GenerousAgent, creator.StingyAgent, creator.TitForTatAgent,
                                             creator.AveragingAgent, creator.VengfulAgent]))
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, self.pop_size)

        # toolbox.register("tourament", creator.Tourament, )
        self.toolbox.register("evaluate", evaluate, num_tours=30, donation = True)  # <- set up method or evaluation
        self.toolbox.register("pop_v_pop", pop_v_pop, num_tours = 10, donation = True)
        self.toolbox.register("select", tools.selTournament,
                              tournsize=3)  # <- select indivuals from a tourment style thingy
        self.toolbox.register("mate", a.mate, max_height=MAX_HEIGHT, toolbox=self.toolbox)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", a.mutate, expr=self.toolbox.expr_mut, max_height=MAX_HEIGHT)
        self.toolbox.register("get_elites", tools.selBest, k=self.elites)
        self.toolbox.register("get_best", tools.selBest, k=1)
        self.toolbox.register("top_half", tools.selBest, k=int(self.pop_size / 2))
        self.toolbox.register("reset", reset)

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "rand", "hum", "std", "min", "avg", "max"

        self.rand_agents = [self.toolbox.random() for i in range(rand_agents)]
        self.human_agents = [self.toolbox.human() for i in range(human_agents)]


    def BuildPrisonTools(self, rand_agents, human_agents):
        """
        perpares the tools necessary for the GP to evolve
        agents belonging to Prisoners Dilemma experimentation
        :param rand_agents: agents that give random decision(s)
        :param human_agents: agents with a algorithm guiding their decision(s)
        """
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", p.PrisonerAgent, fitness=creator.FitnessMax)
        creator.create("RandomAgent", CustomPrisoners.RandomPrisoner, fitness=creator.FitnessMax)
        creator.create("AlwaysCoop", CustomPrisoners.AlwaysCoop, fitness=creator.FitnessMax)
        creator.create("AlwaysDefect", CustomPrisoners.AlwaysDefect, fitness=creator.FitnessMax)
        creator.create("TitForTat", CustomPrisoners.TitForTat, fitness=creator.FitnessMax)
        # creator.create("Tourament", Tournament.Tournament)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", creator.Individual, max_height=MAX_HEIGHT)
        self.toolbox.register("random", creator.RandomAgent)
        self.toolbox.register("human",
                              random.choice([creator.AlwaysCoop, creator.AlwaysDefect, creator.TitForTat]))
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, self.pop_size)

        # toolbox.register("tourament", creator.Tourament, )
        self.toolbox.register("evaluate", evaluate, num_tours=30, donation = False)  # <- set up method or evaluation
        self.toolbox.register("pop_v_pop", pop_v_pop, num_tours=10, donation=False)
        self.toolbox.register("select", tools.selTournament,
                              tournsize=3)  # <- select indivuals from a tourment style thingy
        self.toolbox.register("mate", a.mate, max_height=MAX_HEIGHT, toolbox=self.toolbox)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", a.mutate, expr=self.toolbox.expr_mut, max_height=MAX_HEIGHT)
        self.toolbox.register("get_elites", tools.selBest, k=self.elites)
        self.toolbox.register("get_best", tools.selBest, k=1)
        self.toolbox.register("top_half", tools.selBest, k=int(self.pop_size / 2))
        self.toolbox.register("reset", reset)

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "rand", "hum", "std", "min", "avg", "max"

        self.rand_agents = [self.toolbox.random() for i in range(rand_agents)]
        self.human_agents = [self.toolbox.human() for i in range(human_agents)]

    def Probability(self, prob):
        '''
        return True with probability prob, False otherwise
        '''
        return numpy.random.random() < prob

    def run(self, max_gens, debug = False):
        """
        the main performance
        :param max_gens: total number of generations for GA to perform
        """
        gen = 0
        pop = self.toolbox.population()
        self.random_test = [self.toolbox.random() for i in range(int(self.pop_size/2))]
        self.human_test = [self.toolbox.human() for i in range(int(self.pop_size / 2))]
        self.toolbox.evaluate(pop + self.rand_agents + self.human_agents, debug=debug)

        while gen < max_gens:

            # Vary the population -- not working bc mutate and xover return agents
            new_pop = algorithms.varAnd(pop, self.toolbox, self.xover, self.mut)
            #new_pop = pop

            # evaluate population
            self.toolbox.evaluate(new_pop + self.rand_agents + self.human_agents, debug=debug)



            # Elitism
            elites = self.toolbox.get_elites(pop)
            pop = elites
            #select indivuals
            #this will replace the previous generation, but with mostly good indivuals
            #because select will replace indivuals
            pop += self.toolbox.select(new_pop, len(new_pop) - len(elites))

            best = self.toolbox.top_half(pop)

            avg_agent, avg_rand = self.toolbox.pop_v_pop(best, self.random_test)
            total = avg_agent + avg_rand
            rand_ratio = avg_agent / total # greater then %50 if better
            avg_agent2, avg_human = self.toolbox.pop_v_pop(best, self.human_test)
            human_ratio = avg_agent2 / (avg_agent2 + avg_human)


            record = self.stats.compile(pop)
            self.logbook.record(gen=gen, evals=len(pop), rand = rand_ratio, hum = human_ratio, **record)

            if debug:
                # best = self.toolbox.get_best(new_pop)[0]
                print(self.logbook.stream)
                # print("Generation:", gen, "best fitness:", best.savings)
                # print("Tree", best.tree)
                if gen % 20 == 0:
                    best = self.toolbox.top_half(pop)

                    avg_agent, avg_rand = self.toolbox.pop_v_pop(best, self.random_test)
                    print("Agent Average:", avg_agent, "Random Average:", avg_rand)

                    avg_agent, avg_human = self.toolbox.pop_v_pop(best, self.human_test)
                    print("Agent Average:", avg_agent, "Human Average:", avg_human)

            self.toolbox.reset(pop)
            gen += 1
        return pop, self.logbook, self.toolbox

