from event_queue import *
from population_graph import *
from graph_node import *

#HOMOGENEOUS TREES
def build_tree(infect_rate, cure_rate, degree, gens):
    tree = PopulationGraph(infect_rate,cure_rate)
    root = tree.add_node(GraphNode(None))
    counter = 0

    __tree_helper(tree,root,degree,gens,counter)
    return tree, root

#Recursive tree builder 
def __tree_helper(tree,node,degree,gens,counter):
    if counter < gens:
        for i in range(degree):
            end = tree.add_node(GraphNode(None))
            tree.add_connection(node,end)
            __tree_helper(tree, end, degree, gens, counter+1)



#INTEGER LATTICES

#A cubic lattice
def build_integer_lattice(infect_rate, cure_rate, side_lengths):
    tree = PopulationGraph(infect_rate,cure_rate)
    sides = [int(element) for element in side_lengths]
    dims = len(sides)
    