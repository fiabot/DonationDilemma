import random
import time


# a couple global variables for ease/constants
wallet = 500
threshold = 800
TIMETHRES = 1

def run_2players(pop, debug=False):
    """
    The main tournament for a series of two agent rounds
    :param pop: the full population of agents
    :param debug: switch to turn on debug mode
    :return: the victor (may the odds be ever in your favor)
    """
    current_round = pop[:]
    turn = 0
    start_time = time.perf_counter()
    while len(current_round) > 1:
        if debug:
            timer = time.perf_counter() - start_time
            if timer > TIMETHRES:
                print(turn, len(current_round))
        random.shuffle(current_round)
        next_round = []

        for i in range(1, len(current_round), 2):
            one = current_round[i - 1]
            two = current_round[i]
            next_round.extend(round_fitness_2players(one, two, turn))

        if len(current_round) % 2 == 1:
            current_round[-1].add_savings(wallet)
            next_round.append(current_round[-1])
        current_round = next_round
        turn += 1
    return current_round


def round_fitness_2players(one, two, turn):
    """
    conducts the donation process between two agents,
    which therefore updates each agent's total savings
    as well as determines who lives and dies in this round
    :param one: agent P
    :param two: PERRY THE PLATYPUS???
    :return: the victor (if there is one)
    """
    one_donation = round(one.donate(two, turn))
    two_donation = round(two.donate(one, turn))

    if is_valid_donation(one_donation) and is_valid_donation(two_donation):
        one_current = __individual_result(one_donation, two_donation)
        two_current = __individual_result(two_donation, one_donation)
        one.add_savings(one_current)
        two.add_savings(two_current)
        return __survived_2players(one, two, one_current, two_current)

    elif is_valid_donation(one_donation):
        one.add_savings(wallet)
        return [one]
    elif is_valid_donation(two_donation):
        two.add_savings(wallet)
        return [two]
    else:
        return []


def is_valid_donation(donation):
    """
    a check to confirm that the value donating by an agent is legal
    in the context of the Donation Dilemma
    :param donation: the int value of an agent's donation
    """
    return donation <= wallet and donation >= 0


def __individual_result(donating, receiving):
    """
    calculates the final money of an agent at the end of an individual round
    :param donating: the amount the agent's giving to another
    :param receiving: the collective amount this agent is getting from others
    :return: the agent's final amount of the round
    """
    return wallet + receiving - donating


def __survived_2players(one, two, one_current, two_current):
    """
    determines who lives and who dies in a two agent round
    :param one: an agent
    :param two: a different agent
    :param one_current: the wallet of agent one
    :param two_current: the wallet of agent two
    :return: the survived agent (if there is one)
    """
    if one_current >= threshold:
        return [one]
    elif two_current >= threshold:
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
