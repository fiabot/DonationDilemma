from deap import gp
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import operator
import math
import random
#from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt
import Agent as a

def graphAgent(agent, title = "Title", save = False):
    """
    an agent with the purpose of
    producing graphs of selected evolved
    donations dilemma agents
    :param agent: the chosen DD agent
    :param title: the name of the graph showing the agent
    """
    tree = agent.tree
    nodes, edges, labels = gp.graph(tree)

    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    pos = nx.planar_layout(g, center=edges[0])
    #node_colors = range(len(g))
    M = g.number_of_edges()

    plt.figure(figsize=(15, 15), facecolor=None)
    #nodes = nx.draw_networkx_nodes(g, pos, node_size=600, node_color=node_colors,cmap=plt.cm.Reds)
    nodes = nx.draw_networkx_nodes(g, pos, node_size=3500)

    edges = nx.draw_networkx_edges(g, pos, arrowstyle='->', arrowsize=50, edge_color='black')

    nx.draw_networkx_labels(g, pos, labels=labels, font_size=22, font_family='sans-serif')
    # ax = nx.draw_networkx(g, pos = pos, labels = labels, node_size = 3000, )
    # And plot it

    ax = plt.gca()
    ax.set_axis_off()
    plt.title(title)
    if save:
        plt.savefig(title + ".png")
    else:
        plt.show()

if __name__ == "__main__":
    agent = a.Agent(1,3)
    graphAgent(agent, "This Agent")
