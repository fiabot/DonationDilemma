from deap import gp
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy
import operator
import math
import random
import graphviz as gph

pset = gp.PrimitiveSet("main", 2)
pset.addPrimitive(max, 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addTerminal(3)

pset.renameArguments(ARG0="x")
pset.renameArguments(ARG1="y")

expr = gp.genFull(pset, min_=1, max_=3)
tree = gp.PrimitiveTree(expr)
str(tree)

function = gp.compile(tree, pset)
function(1,2)

expr1 = gp.genFull(pset, min_=2, max_=3)
expr2 = gp.genFull(pset, min_=2, max_=5)
tree1 = gp.PrimitiveTree(expr1)
tree2 = gp.PrimitiveTree(expr2)
print("Tree1 " + str(tree1))
#print("Tree2 " + str(tree2))

t = gp.mutNodeReplacement(tree1, pset)
print("Mutation 1 " + str(t[0]))

newTree1, newTree2 = gp.cxOnePoint(tree1, tree2)
print("CrossOver: " + str(newTree1))

nodes, edges, labels = gp.graph(tree1)
print(nodes,edges, labels)
