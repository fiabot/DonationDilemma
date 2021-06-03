import pickle
import Graph
import Agent

trees = pickle.load(open("LastGeneration.p", "rb"))
agents = [Agent.Agent(tree = tree) for tree in trees]
for t in agents[:5]:
    Graph.graphAgent(t)