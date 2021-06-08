import deap.gp as gp
import operator
from deap import base
import math
import random
import copy
import Graph
import Agent


# import pygraphviz as pgv
NUM_INPUTS = 6


class PrisonerAgent:

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

        # self.alive = True
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def create_prim_set(self):
        pset = gp.PrimitiveSet("MAIN", NUM_INPUTS)
        pset.addPrimitive(operator.and_, 2)
        pset.addPrimitive(operator.or_, 2)
        pset.addPrimitive(operator.xor, 2)
        pset.addPrimitive(operator.not_, 1)
        pset.addTerminal(1)
        pset.addTerminal(0)

        pset.renameArguments(ARG0="myHist1")
        pset.renameArguments(ARG1="myHist2")
        pset.renameArguments(ARG2="myHist3")
        pset.renameArguments(ARG3="opHist1")
        pset.renameArguments(ARG4="opHist2")
        pset.renameArguments(ARG5="opHist3")

        self.pset = pset

    def decide(self, other, turn):
        """
        determines whether or not the PrisonerAgent
        cooperates or defects
        :param other: the opponent PrisonerAgent
        :param turn: the turn number
        :return: a boolean: True for cooperation,
        False for defect
        """
        decision = self.runTree(self.hist1, self.hist2, self.hist3, other.hist1,
                                other.hist2, other.hist3)
        self.hist3 = self.hist2
        self.hist2 = self.hist1
        self.hist1 = decision
        return decision

    def reset(self):
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def add_fitness(self, amount):
        """
        add specified amount to the agent's fitness
        :param amount: the value to add to agent's total fitness
        """
        self.savings += amount

def boo(pset, type_):
    """
    FOR TESTING DELETE THIS LATER
    :param self:
    :return:
    """
    return gp.genFull(pset, type_= type_,  min_ = 0, max_ = 2)

if __name__ == "__main__":
    agent = PrisonerAgent(min_height= 1, max_height= 3)
    agent2 = PrisonerAgent(min_height= 1 , max_height= 3)

    print(agent.decide(agent2,4))
    Graph.graphAgent(agent, title = "Agent org")
    print("Agent org", agent.tree)
    Graph.graphAgent(agent2, title = "Agent 2 org")
    print("Agent 2 org", agent2.tree)

    Agent.mutate(agent, boo)
    Graph.graphAgent(agent, title = "Agent Mutated" )
    print("Agent Mutation", agent.tree)

    new1, new2 = Agent.mate(agent, agent2, donation = False)
    Graph.graphAgent(new1, title= "Mate 1")
    Graph.graphAgent(new2, title="Mate 1")
    print("mate 1", new1.tree)
    print("mate 2:" , new2.tree)



