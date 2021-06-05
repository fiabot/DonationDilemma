import deap.gp as gp
import operator
from deap import base
import math
import random
import copy


# import pygraphviz as pgv


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
        self.fitness = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def decide(self, other, turn):
        """
        determines whether or not the PrisonerAgent
        cooperates or defects
        :param other: the opponent PrisonerAgent
        :param turn: the turn number
        :return: a boolean: True for cooperation,
        False for defect
        """
        decision = self.runTree(self.fitness, other.fitness, self.hist1, self.hist2, self.hist3, other.hist1,
                                other.hist2, other.hist3, turn)
        self.hist3 = self.hist2
        self.hist2 = self.hist1
        self.hist1 = decision
        return decision

    def add_fitness(self, amount):
        """
        add specified amount to the agent's fitness
        :param amount: the value to add to agent's total fitness
        """
        self.fitness += amount