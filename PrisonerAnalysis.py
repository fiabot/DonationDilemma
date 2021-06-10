import PrisonerAgent
import math
import pickle
from sklearn.cluster import AffinityPropagation
from deap import tools
import matplotlib.pyplot as plt
import Graph

class AnaylizePrisoner:
    """
    A supporting agent to the Donation Dilemma agents,
    takes evolved agents and runs them through some tests
    in order to find displayable, understandable results
    """

    def __init__(self, agent):
        """
        constructor for an agent designed to analysis
        noteworthy features about a DD's agent and its history
        :param agent: the DD agent selected for analysis
        :param turns: the amount of rounds to test the agent for
        """
        self.agent = agent

        self.options = [0, 1]


        self.invalid = -1


    def run(self):
        self.total = []

        for ophist1 in self.options:
            for ophist2 in self.options:
                for ophist3 in self.options:
                    for myhist1 in self.options:
                        for myhist2 in self.options:
                            for myhist3 in self.options:
                                result = self.agent.runTree(myhist1, myhist2, myhist3, ophist1,
                                ophist2, ophist3)
                                if not result in self.options:
                                    result = self.invalid
                                self.total.append(result)

        return self.total


    def number_invalid(self):
        """
        checks the validity of AnaylizeAgent's total
        """
        return self.total.count(self.invalid)


if __name__ == "__main__":


    trees = pickle.load(open("Prisoners.p", "rb"))
    print(len(trees))
    agents = [PrisonerAgent.PrisonerAgent(tree=tree) for tree in trees]
    totals = []
    analysis = []
    print("Depickled Agents")

    for agent in agents:
        a = AnaylizePrisoner(agent)
        total = a.run()
        totals.append(total)
        analysis.append(a)
    print("Analyized Agents")

    af = AffinityPropagation(preference=-50).fit(totals)
    print("Clustered agents")
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    n_clusters_ = len(cluster_centers_indices)
    print("Number of Groups" , n_clusters_)


    invalid_donations = [a.number_invalid() for a in analysis]
    plt.hist(invalid_donations)
    plt.title("Number of Invalid Prisoners")
    #plt.savefig('InvalidDonations.png')
    plt.show()
    print(invalid_donations.count(0))