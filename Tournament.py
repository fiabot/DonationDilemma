import random


def round_fitness(my, op):
    my_donation = my.donate()
    op_donation = op.donate()

    my.add_savings(op_donation)
    op.add_savings(my_donation)
    my_current = 500 + op_donation - my_donation
    op_current = 500 + my_donation - op_donation
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


class Tournament:

    def __init__(self, pop, gametype, debug):
        self.pop = pop
        self.gametype = gametype
        self.popsize = len(pop)
        self.__debug = debug

    def run_2players(self):
        current_round = self.pop[:]
        round = 0
        while len(current_round) > 1:
            if self.__debug:
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
