import deap.gp as gp
import operator
import random
import copy
#import pygraphviz as pgv
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


class Agent:
    def __init__(self, min_height=3, max_height=10, tree=None):
        """
        Either create a new agent given a tree or
        create a random tree

        initialize starting variables
        """
        self.create_prim_set()

        if tree != None:
            self.tree = tree  # TODO: doesn't copy tree, this could be a problem
        else:
            expr = gp.genHalfAndHalf(self.pset, min_=min_height, max_=max_height)
            self.tree = gp.PrimitiveTree(expr)
        self.min_height = min_height
        self.max_height = max_height
        self.runTree = gp.compile(self.tree, self.pset)

        self.alive = True
        self.saving = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def reset(self):
        """
        restart starting variables
        """
        self.alive = True
        self.saving = 0
        self.hist1 = 0
        self.hist2 = 0
        self.hist3 = 0

    def create_prim_set(self):
        """
        Set up the basic operations and arguments for
        the program tree
        """
        pset = gp.PrimitiveSet("main", 9)
        pset.addPrimitive(max, 2)
        pset.addPrimitive(operator.add, 2)
        pset.addPrimitive(operator.mul, 2)
        pset.addPrimitive(operator.abs, 1)
        pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(protectedDiv, 2)
        # pset.addEphemeralConstant("random", lambda: random.randint(-10, 10))

        pset.renameArguments(ARG0="mySave")
        pset.renameArguments(ARG1="opSave")
        pset.renameArguments(ARG2="myDon1")
        pset.renameArguments(ARG3="myDon2")
        pset.renameArguments(ARG4="myDon3")
        pset.renameArguments(ARG5="opDon1")
        pset.renameArguments(ARG6="opDon2")
        pset.renameArguments(ARG7="opDon3")
        pset.renameArguments(ARG8="turn")

        self.pset = pset

    def donate(self, mySave, opSave, myDon1, myDon2, myDon3, opDon1, opDon2, opDon3, turn):
        """
        Use program tree to give donation
        and update history
        """
        donation = self.runTree(mySave, opSave, myDon1, myDon2, myDon3, opDon1, opDon2, opDon3, turn)
        self.hist3 = self.hist2
        self.hist2 = self.hist1
        self.hist1 = donation
        return donation

    def add_savings(self, amount):
        """
        Add amount to savings
        """
        self.savings += amount

    def get_savings(self):
        """
        Get current savings
        """
        return self.savings

    def get_tree(self):
        """
        Return tree of agent
        Could cause trouble but...
        """
        return self.tree

    def crossover(self, other):
        newTree1, newTree2 = gp.cxOnePoint(self.getTree, other.getTree)
        return Agent(self.min_height, self.max_height, tree=newTree1), Agent(self.min_height, self.max_height,
                                                                             tree=newTree1)

    def mutate(self, muts=10):
        for i in range(muts):
            num = random.randint(0,2)
            if num == 0:
                self.tree = gp.mutNodeReplacement(self.tree, self.pset)[0]
            elif num == 1:
                self.tree = gp.mutShrink(self.tree)[0]
            elif num == 2:
                self.tree = gp.mutInsert(self.tree, self.pset)[0]
        self.runTree = gp.compile(self.tree, self.pset)

if __name__ == "__main__":
    agent = Agent(1, 5)
    print(agent.donate(0, 300, 20, 250, 0, 10, 400, 0, 4))
    agent.mutate(muts=1)
    print(agent.donate(0, 300, 20, 250, 0, 10, 400, 0, 4))