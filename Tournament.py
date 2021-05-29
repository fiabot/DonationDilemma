import random


def run_2players(pop, debug=False):
    """
    The main tournament for a series of 2 agent rounds
    :param pop: The full population of agents
    :param debug: switch to turn on debug mode
    :return: the victor (may the odds be ever in your favor)
    """
    current_round = pop[:]
    round = 0
    while len(current_round) > 1:
        if debug:
            print(round, len(current_round))
        random.shuffle(current_round)
        next_round = []
        for i in range(1, len(current_round), 2):
            one = current_round[i - 1]
            two = current_round[i]
            next_round.extend(round_fitness_2players(one, two,round))
        if len(current_round) % 2 == 1:
            current_round[-1].add_savings(500)
            next_round.append(current_round[-1])
        current_round = next_round
        round += 1
    return current_round


def round_fitness_2players(one, two, round):
    """
    conducts the donation process between two agents,
    which therefore updates each agent's total savings
    as well as determines who lives and dies in this round
    :param one: agent P
    :param two: PERRY THE PLATYPUS???
    :return: the victor (if there is one)
    """
    one_donation = one.donate(two, round)
    two_donation = two.donate(one, round)

    if is_valid_donation(one_donation) and is_valid_donation(two_donation):
        one_money = __individual_result(one_donation, two_donation)
        two_money = __individual_result(two_donation, one_donation)
        one.add_savings(one_money)
        two.add_savings(two_money)
        return __survived_2players(one, two, one_money, two_money)
    elif is_valid_donation(one_donation):
        one.add_savings(500)
        return [one]
    elif is_valid_donation(two_donation):
        two.add_savings(500)
        return [two]
    else:
        return []

def is_valid_donation(donation):
    return donation <= 500 and donation >= 0

def __individual_result(donating, receiving):
    """
    calculates the final money of an agent at the end of an individual round
    :param donating: the amount the agent's giving to another
    :param receiving: the collective amount this agent is getting from others
    :return: the agent's final amount of the round
    """
    return 500 + receiving - donating


def __survived_2players(one, two, one_current, two_current):
    """
    determines who lives and who dies in a two agent round
    :param one: an agent
    :param two: a different agent
    :param one_current: the wallet of agent one
    :param two_current: the wallet of agent two
    :return: the survived agent (if there is one)
    """
    if one_current >= 800:
        return [one]
    elif two_current >= 800:
        return [two]
    elif one_current > two_current:
        return [two]
    elif two_current > one_current:
        return [one]
    else:
        return []


def round_fitness_n(players):
    donations = []
    for player in players:
        donations.append(player.donate()) #TODO fixed donation for n players

    wallets = []
    for donation in donations:
        wallets.append(69)

    update_savings()

    return __survived_nplayers(players, wallets)


def __survived_nplayers(players, wallets):
    return []


def update_savings():
    pass

"""
def run_2players(pop, debug):
    current_round = pop[:]
    round = 0
    while len(current_round) > 1:
        if debug:
            print(round, len(current_round))
        random.shuffle(current_round)
        next_round = []
        for i in range(1, len(current_round), 2):
            next_round.extend(round_fitness(current_round[i - 1], current_round[i]))
        if len(current_round) % 2 == 1:
            current_round[-1].add_savings(500)
            next_round.append(current_round[-1])
        current_round = next_round
        round += 1
    return current_round
"""

"""
def round_fitness(my, op):
    my_donation = my.donate()
    op_donation = op.donate()

    my_current = 500 + op_donation - my_donation
    op_current = 500 + my_donation - op_donation

    my.add_savings(op_donation)
    op.add_savings(my_donation)

    if my_current >= 800:
        return [my]
    elif op_current >= 800:
        return [op]
    elif my_current > op_current:
        return [op]
    elif op_current > my_current:
        return [my]
    else:
        return []

"""
