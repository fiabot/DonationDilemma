import random

class RandomPrisoner:
    def __init__(self):
        """
        Generates a new PrisonerAgent, one that
        randomly decides whether to cooperate or defect

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        return random.choice([0, 1])

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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
        Generates a new PrisonerAgent, one that
        ALWAYS defects

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        return 0

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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
        Generates a new PrisonerAgent, one that
        ALWAYS cooperates

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        return 1

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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
        Generates a new PrisonerAgent, one that
        decides according to the decision of the opponent's
        prior decision

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        if turn == 0:
            return 1
        else:
            return other.hist1

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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

class Pavlov:
    def __init__(self):
        """
        Generates a new PrisonerAgent, one that
        cooperates if its prior decision matches
        its opponent's prior decision, or defects otherwise

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        if self.hist1 == other.hist1:
            return 1
        else:
            return 0

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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


class Brave:
    def __init__(self):
        """
        Generates a new PrisonerAgent, one that
        always cooperates unless the opponent defected
        in all three prior rounds

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        if turn == 0:
            return 1
        else:
            if other.hist1 == 0 and other.hist2 == 0 and other.hist3 == 0:
                return 0
            else:
                return 1

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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


class Nervous:
    def __init__(self):
        """
        Generates a new PrisonerAgent, one that
        always cooperates unless the opponent defected
        in at least ONE of the three prior rounds

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
        :return: an int; 1 for cooperation,
        0 for defect
        """
        if turn == 0:
            return 1
        elif turn == 1:
            if other.hist1 == 0:
                return 0
            else:
                return 1
        elif turn == 2:
            if other.hist1 == 0 or other.hist2 == 0:
                return 0
            else:
                return 1
        else:
            if other.hist1 == 0 or other.hist2 == 0 or other.hist3 == 0:
                return 0
            else:
                return 1

    def reset(self):
        """
        reverts the agent's variables back
        to its initialized states
        """
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
