import Agent
import math
import pickle
from sklearn.cluster import AffinityPropagation
from deap import tools
import matplotlib.pyplot as plt
import Graph

class AnaylizeAgent:
    """
    A supporting agent to the Donation Dilemma agents,
    takes evolved agents and runs them through some tests
    in order to find displayable, understandable results
    """

    def __init__(self, agent, turns = 10):
        """
        constructor for an agent designed to analysis
        noteworthy features about a DD's agent and its history
        :param agent: the DD agent selected for analysis
        :param turns: the amount of rounds to test the agent for
        """
        self.agent = agent
        self.turns = turns
        high_savings = 1000
        mid_savings = 600
        low_savings = 201

        high_donation = 500
        mid_donation =250
        low_donation = 0

        self.saving_values = (("high", high_savings), ("low", low_savings), ("mid", mid_savings))
        self.donation_values = (("high", (high_donation, high_donation, high_donation)),
                                ("low", (low_donation, low_donation, low_donation)), ("mid", (mid_donation, mid_donation, mid_donation)),
                                ("ascend",(low_donation, mid_donation, high_donation)), ("descend" , (high_donation, mid_donation, low_donation)))

        self.invalid = -1


    def run(self):
        self.total = []

        #saving specifc
        self.don_my_saving = {"high": [], "low": [], "mid": []}
        self.don_op_saving = {"high": [], "low": [], "mid": []}

        self.don_my_don = {"high": [], "low": [], "mid": [], "ascend": [], "descend": []}
        self.don_op_don = {"high": [], "low": [], "mid": [], "ascend": [], "descend": []}

        self.by_turn = []

        for turn in range(self.turns):
            turn_dons = []

            for my_save_value, my_save in self.saving_values:
                for op_save_value, op_save in self.saving_values:
                    for my_don_value, my_don in self.donation_values:
                        for op_don_value, op_don in self.donation_values:
                            my_hist1 = 0
                            my_hist2 = 0
                            my_hist3 = 0
                            op_hist1 = 0
                            op_hist2 = 0
                            op_hist3 = 0

                            if turn >= 1:
                                my_hist1 = my_don[0]
                                op_hist1 = op_don[0]
                            if turn >= 2:
                                my_hist1 = my_don[1]
                                op_hist1 = op_don[1]
                            if turn >= 3:
                                my_hist1 = my_don[2]
                                op_hist1 = op_don[2]

                            try:
                                donation = self.agent.runTree(my_save * turn, op_save *turn, my_hist1, my_hist2, my_hist3, op_hist1,
                                                              op_hist2, op_hist3, turn)
                                if donation > 500 or donation < 0 or math.isnan(donation):
                                    donation = self.invalid
                            except:
                                donation = self.invalid

                            self.total.append(donation)
                            turn_dons.append(donation)
                            self.don_my_saving[my_save_value].append(donation)
                            self.don_op_saving[op_save_value].append(donation)

                            self.don_my_don[my_don_value].append(donation)
                            self.don_op_don[op_don_value].append(donation)
            self.by_turn.append(turn_dons)
        return self.total


    def number_invalid(self):
        """
        checks the validity of AnaylizeAgent's total
        """
        return self.total.count(self.invalid)


if __name__ == "__main__":


    trees = pickle.load(open("Ten10Gens.p", "rb"))
    print(len(trees))
    agents = [Agent.Agent(tree=tree) for tree in trees]
    totals = []
    analysis = []
    print("Depickled Agents")

    for agent in agents:
        a = AnaylizeAgent(agent, turns = 5)
        total = a.run()
        totals.append(total)
        analysis.append(a)
    print("Analyized Agents")

    #af = AffinityPropagation(preference=-50).fit(totals)
    #print("Clustered agents")
    #cluster_centers_indices = af.cluster_centers_indices_
    #labels = af.labels_

    #n_clusters_ = len(cluster_centers_indices)
    #print("Number of Groups" , n_clusters_)


    invalid_donations = [a.number_invalid() for a in analysis]
    plt.hist(invalid_donations)
    plt.title("Number of Invalid Donations")
    plt.savefig('InvalidDonations.png')
