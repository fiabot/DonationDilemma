import deap.gp as gp
import operator
from deap import base
import math
import random
import copy
#import pygraphviz as pgv


def div(numer, denom):
    """
    division that considers undefined situation
    :param numer: the numerator in division
    :param denom: the denominator in division
    :return: the quotient, or 1 in case of undefined case
    """
    try:
        return numer / denom
    except ZeroDivisionError:
        return 1

def randomNum(min = 0, max = 500):
    return random.randint(min, max)

"""pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(div, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("whatever", lambda: random.randint(-1, 1))"""


class RandAgent:

    def __init__(self):
        """
        base constructor of a RANDOM agent
        an agent with no history and no savings (and no sanity)
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def reset(self):
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def donate(self, other, round):
        """
        calculates the donation of this agent for one round,
        the donation being a randomly generated amount
        :param other: the agent who will receive the donation
        :param round: the current round number
        :return: a donation from this agent to another
        """
        donation = random.randint(0, 500)

        self.hist3 = self.hist2
        self.hist2 = self.hist1
        self.hist1 = donation
        return donation


    def add_savings(self, amount):
        """
        adding a specified amount to the agent's savings
        :param amount: the value to add to agent's total savings
        """
        self.savings += amount


class Agent:

    def __init__(self, min_height=3, max_height=5, tree=None):
        """
        Either create a new agent given a tree or
        create a random tree

        initialize starting variables
        :param min_height: minimum tree depth complexity
        :param max_height: maximum tree depth complexity
        :param tree: the algorithmic tree to copy onto the agent, must use same primative set
        """
        self.create_prim_set()

        if tree != None:
            tree_copy = gp.PrimitiveTree.from_string(str(tree), self.pset)
            self.tree = tree_copy
        else:
            expr = gp.genHalfAndHalf(self.pset, min_=min_height, max_=max_height)
            self.tree = gp.PrimitiveTree(expr)

        self.height = self.tree.height
        self.min_height = min_height
        self.max_height = max_height
        self.runTree = gp.compile(self.tree, self.pset)

        self.alive = True
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0
        #self.fitness = base.Fitness()


    def reset(self):
        """
        restart starting variables,
        specifically the life, savings, and history of the agent
        """
        self.alive = True
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def create_prim_set(self):
        """
        Set up the basic operations and arguments for
        the program tree
        """
        pset = gp.PrimitiveSet("main", 9)
        pset.addPrimitive(max, 2)
        pset.addPrimitive(operator.add, 2)
        pset.addPrimitive(operator.mul, 2)
        pset.addPrimitive(operator.abs, 1)
        pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(div, 2)
        pset.addTerminal(0)
        pset.addTerminal(500)
        #pset.addTerminal(random.randint(0,500))
        #pset.addEphemeralConstant("Random", randomNum, int)
        #pset.addEphemeralConstant("Random", lambda: random.randint(0, 500))

        """pset = gp.PrimitiveSet("MAIN", 1)
        pset.addPrimitive(operator.add, 2)
        pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(operator.mul, 2)
        pset.addPrimitive(div, 2)
        pset.addPrimitive(operator.neg, 1)
        pset.addPrimitive(math.cos, 1)
        pset.addPrimitive(math.sin, 1)
        pset.addEphemeralConstant("whatever", lambda: random.randint(-1, 1))"""

        pset.renameArguments(ARG0="mySave")
        pset.renameArguments(ARG1="opSave")
        pset.renameArguments(ARG2="myHist1")
        pset.renameArguments(ARG3="myHist2")
        pset.renameArguments(ARG4="myHist3")
        pset.renameArguments(ARG5="opHist1")
        pset.renameArguments(ARG6="opHist2")
        pset.renameArguments(ARG7="opHist3")
        pset.renameArguments(ARG8="turn")

        self.pset = pset


    def donate(self, other, turn):
        """
        calculates the donation of this agent for one round
        using program tree and update agent's history,
        the donation being a randomly generated amount
        :param other: the agent who will receive the donation
        :param round: the current round number
        :return: a donation from this agent to another
        """
        try:
            donation = self.runTree(self.savings, other.savings, self.hist1, self.hist2, self.hist3, other.hist1, other.hist2, other.hist3, turn)
            if donation > 500 or donation < 0:
                donation = 600
        except Exception as exec:
            print("DONATION ERROR", self.tree.height)
            print(exec)
            donation = 600
        self.hist3 = self.hist2
        self.hist2 = self.hist1
        self.hist1 = donation
        return donation


    def add_savings(self, amount):
        """
        add specified amount to savings
        :param amount: the value to add to agent's total savings
        """
        self.savings += amount


    def get_savings(self):
        """
        :return: the current savings of the agent
        """
        return self.savings


    def get_tree(self):
        """
        Return tree of agent
        Could cause trouble but...
        """
        return self.tree


    def crossover(self, other):
        """
        a one point crossover between the algorithmic trees of two agents
        :param other: the other agent to use in crossover
        :return: tuple of children agents
        """
        newTree1, newTree2 = gp.cxOnePoint(self.getTree, other.getTree)
        return Agent(self.min_height, self.max_height, tree=newTree1), Agent(self.min_height, self.max_height,
                                                                             tree=newTree1)

    def mutate(self, muts=10):
        """
        trio-combined mutation option; capable of adding,
        removing, or replacing a node in the tree
        :param muts: specified number of mutations to occur
        """
        for i in range(muts):
            num = random.randint(0,2)
            if num == 0:
                self.tree = gp.mutNodeReplacement(self.tree, self.pset)[0]
            elif num == 1:
                self.tree = gp.mutShrink(self.tree)[0]
            elif num == 2:
                self.tree = gp.mutInsert(self.tree, self.pset)[0]
        self.runTree = gp.compile(self.tree, self.pset)

def copy_agent_tree(agent):
    return gp.PrimitiveTree.from_string(str(agent.tree), agent.pset)

def mate(agent1, agent2, max_height = 17, toolbox = None, i = 0):
    """
    Return the offspring of a one point crossover between two
    agents. If one offspring exceeds the max height, return one
    of the parents (chosen randomly)
    :param agent1: first agent to mate
    :param agent2: second agent
    :param max_height: max height of tree
    :return: two new agents
    """
    parent1 = copy_agent_tree(agent1)
    parent2 = copy_agent_tree(agent2)
    newTree1, newTree2 = gp.cxOnePoint(parent1, parent2)
    if newTree1.height > max_height:
        newTree1 = random.choice([agent1.tree, agent2.tree])

    if newTree2.height > max_height:
        newTree2 = random.choice([agent1.tree, agent2.tree])

    if toolbox  != None:
        return toolbox.individual(tree =newTree1), toolbox.individual(tree =newTree2)
    else:
        return Agent(agent1.min_height, agent1.max_height, tree=newTree1), Agent(agent1.min_height, agent1.max_height,
                                                                         tree=newTree2)


def mutate(agent, expr, max_height = 17):
    """
    functionality of random mutation for an agent
    :param agent: the agent to mutate
    :param expr: the used to generate the node for replacement
    :param max_height: maximum height to confirm mutation
    :return: a tuple containing the agent, mutated or not
    """
    #expr = gp.genHalfAndHalf(agent.pset, 0, 2)
    tree_copy = copy_agent_tree(agent)
    new_tree = gp.mutUniform(tree_copy, expr, agent.pset)
    new_tree = new_tree[0]
    if new_tree.height <= max_height:
        agent.tree = new_tree
        agent.runTree = gp.compile(agent.tree, agent.pset)
    return agent,


if __name__ == "__main__":
    print(randomNum())
    agent = Agent(1, 5)
    agent2 = Agent(1, 5)
    a1, a2 = mate(agent, agent2, max_height=6)
    print("Offsprint iteration:")
    print(a1.tree.height, a2.tree.height)
