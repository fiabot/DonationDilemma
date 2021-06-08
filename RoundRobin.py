
def round_robin(pop, debug=False):
    """
    A round robin interaction pattern for all
    agents of a population for Prisoner's Dilemma
    :param pop: the full population of agents
    :param debug: switch to turn on debug mode
    """
    current_round = pop[:]
    for i in range(0, len(current_round) - 1):
        turn = 0
        for j in range(i + 1, len(current_round)):
            round_fitness(current_round[i], current_round[j], turn)
        turn += 1


def round_fitness(one, two, turn):
    """
    conducts the decision process between two agents,
    which therefore updates each agent's total fitnesses.
    :param one: a PrisonerAgent
    :param two: another PrisonerAgent
    """
    one_decision = round(one.decide(two, turn))
    two_decision = round(two.decide(one, turn))
    if is_valid_decision(one_decision) == 1 and is_valid_decision(two_decision) == 1:
        round_result(one_decision, two_decision)


def is_valid_decision(decision):
    """
    a check to confirm that the agent is either cooperating or defecting
    :param decision: the boolean confirmation of an agent's decision
    """
    return decision == 1 or decision == 0


def round_result(agent1, agent2, decision1, decision2):
    """
    adds to the fitness of the agents according to the decisions
    :param agent1: a PrisonerAgent
    :param agent2: another PrisonerAgent
    :param decision1: decision of agent 1
    :param decision2: decision of agent 2
    :return:
    """
    if decision1 == 1 and decision2 == 1:
        agent1.add_fitness(2)
        agent2.add_fitness(2)
    elif decision1 == 1 and decision2 == 0:
        agent1.add_fitness(0)
        agent2.add_fitness(3)
    elif decision1 == 0 and decision2 == 1:
        agent1.add_fitness(3)
        agent2.add_fitness(0)
    else:
        agent1.add_fitness(1)
        agent2.add_fitness(1)

