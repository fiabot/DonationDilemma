import pickle
import Graph
import Agent

trees = pickle.load(open("Ten10Gens.p", "rb"))
print(len(trees))
agents = [Agent.Agent(tree = tree) for tree in trees]
for t in agents[:5]:
    Graph.graphAgent(t)