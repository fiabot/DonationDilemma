import random

class RandomPrisoner:
    def __init__(self):
        """
                Either create a new agent given a tree or
                create a random tree

                initialize starting variables
                :param min_height: minimum tree depth complexity
                :param max_height: maximum tree depth complexity
                :param tree: the algorithmic tree to copy onto the agent, must use same primative set
                """

        # self.alive = True
        self.savings = 0
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
        return random.choice([0, 1])

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


class AlwaysDefect:
    def __init__(self):
        """
                Either create a new agent given a tree or
                create a random tree

                initialize starting variables
                :param min_height: minimum tree depth complexity
                :param max_height: maximum tree depth complexity
                :param tree: the algorithmic tree to copy onto the agent, must use same primative set
                """

        # self.alive = True
        self.savings = 0
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
        return 0

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

class AlwaysCoop:
    def __init__(self):
        """
                Either create a new agent given a tree or
                create a random tree

                initialize starting variables
                :param min_height: minimum tree depth complexity
                :param max_height: maximum tree depth complexity
                :param tree: the algorithmic tree to copy onto the agent, must use same primative set
                """

        # self.alive = True
        self.savings = 0
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
        return 1

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

class TitForTat:
    def __init__(self):
        """
                Either create a new agent given a tree or
                create a random tree

                initialize starting variables
                :param min_height: minimum tree depth complexity
                :param max_height: maximum tree depth complexity
                :param tree: the algorithmic tree to copy onto the agent, must use same primative set
                """

        # self.alive = True
        self.savings = 0
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
        if turn == 0:
            return 1
        else:
            return other.hist1

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