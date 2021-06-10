import Agent
import Graph
import deap.gp as gp

agent1 = Agent.Agent(1, 3)
agent2 = Agent.Agent(1, 3)

#Orginal Graphs
Graph.graphAgent(agent1, "Orignal Agent 1", save = True)
Graph.graphAgent(agent2, "Orignal Agent 2", save = True)

#Cross Over
cros1 , cros2 = Agent.mate(agent1, agent2)
Graph.graphAgent(cros1, "Crossed Agent 1", save = True)
Graph.graphAgent(cros2, "Crossed Agent 2", save = True)

#Mutation
def expr(pset, type_):
    return gp.genFull(pset,  type_ = type_, min_ = 0, max_ = 5)
Agent.mutate(agent1, expr)
Graph.graphAgent(agent1, "Mutated Agent 1", save = True)
