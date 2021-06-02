import random
from Agent import Agent


class GenerousAgent:
    """
    A Generous agent is one that loves to donate everything
    they got (or almost everything they got). There is a
    little bit of variance in its determined donation so that
    Generous agents have a less likely chance to tie (and
    therefore do not kill themselves consistently).
    """

    def __init__(self):
        """
        base constructor of a Generous agent
        an agent with no history and no savings (and no sanity)
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def reset(self):
        """
        reverts the agent back to its initiation state
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def donate(self, other, round):
        """
        calculates the donation of this agent for one round,
        the donation being a HIGH amount
        :param other: the agent who will receive the donation
        :param round: the current round number
        :return: a donation from this agent to another
        """
        donation = random.randint(490, 500)

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


class StingyAgent:
    """
    A Stingy agent is one that hates donating their money.
    A Stingy agent wants to keep onto all (or nearly all) of its money.
    There is a little bit of variance in its determined donation so that
    Stingy agents have a less likely chance to tie (and
    therefore do not kill themselves consistently).
    """

    def __init__(self):
        """
        base constructor of a Stingy agent
        an agent with no history and no savings (and no sanity)
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def reset(self):
        """
        reverts the Stingy agent back to its initiation state
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def donate(self, other, round):
        """
        calculates the donation of this agent for one round,
        the donation being a LOW amount
        :param other: the agent who will receive the donation
        :param round: the current round number
        :return: a donation from this agent to another
        """
        donation = random.randint(0, 10)

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


class TitForTatAgent:
    """
    This agent is an incarnation of the widely proclaim optimal
    strategy for the Prisoner's Dilemma, Tit for Tat. Specifically,
    this agent copies the previous donation of its opponent. If it
    is the very first round (and therefore no donations have been
    preformed yet), the agent acts randomly.
    """

    def __init__(self):
        """
        base constructor of a TitForTat agent
        an agent with no history and no savings (and no sanity)
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def reset(self):
        """
        reverts the agent back to its initiation state
        """
        self.savings = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def donate(self, other, round):
        """
        calculates the donation of this agent for one round,
        the donation being the opponent's previous amount or
        a random donation should it be the first round.
        :param other: the agent who will receive the donation
        :param round: the current round number
        :return: a donation from this agent to another
        """
        if round == 0:
            donation = random.randint(0, 500)
        else:
            donation = other.hist1

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