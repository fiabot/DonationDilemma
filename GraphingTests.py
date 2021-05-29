from deap import gp
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import operator
import math
import random
from graphviz import Digraph
import  networkx as nx
import matplotlib.pyplot as plt
#from networkx.drawing.nx_agraph import write_dot, graphviz_layout


pset = gp.PrimitiveSet("main", 2)
pset.addPrimitive(max, 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addTerminal(3)

pset.renameArguments(ARG0="x")
pset.renameArguments(ARG1="y")

expr1 = gp.genFull(pset, min_=2, max_=3)
tree1 = gp.PrimitiveTree(expr1)

nodes, edges, labels = gp.graph(tree1)
print(nodes,edges, labels)


g = nx.DiGraph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)

for node in g.nodes:
    g.nodes[node]["label"] = labels[node]
print(g.nodes.data())

#write_dot(g,'test.dot')
#pos =graphviz_layout(g, prog='dot')
pos = nx.planar_layout(g,center = edges[0])
node_colors = range(len(g))
M = g.number_of_edges()

plt.figure(figsize = (15, 15), facecolor = None)
nodes = nx.draw_networkx_nodes(g, pos, node_size = 3000, node_color=node_colors, cmap=plt.cm.Reds)

edges = nx.draw_networkx_edges(g, pos, arrowstyle='->', arrowsize=50, edge_color='black')

nx.draw_networkx_labels(g, pos, labels = labels, font_size=18, font_family='sans-serif')
#ax = nx.draw_networkx(g, pos = pos, labels = labels, node_size = 3000, )
# And plot it

ax = plt.gca()
ax.set_axis_off()
plt.title('Genetic Program')

plt.show()
