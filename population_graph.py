from graph_node import *
import numpy as np
from random import sample

class PopulationGraph():
    def __init__(self, infect_param, cure_param, is_tree = False, name = None):
        self.is_tree = is_tree
        self.infect_param = infect_param
        self.cure_param = cure_param

        self.nodes = set()
        self.num_nodes = 0

        self.infected_nodes = set()
        self.cured_nodes = set()


    def add_connection(self, node1, node2):
        if (node1 is None) or (node2 is None):
            raise Exception("Nodes cannot be None type")
        if node1 in node2.neighbors:
            raise Exception("Connection already exists")

        node1.neighbors.add(node2)
        node1.num_neighbors += 1

        node2.neighbors.add(node1)
        node2.num_neighbors += 1

    def delete_connection(self,node1,node2):
        if (node1 is None) or (node2 is None):
            raise Exception("Nodes cannot be None type")
        if not(node1 in node2.neighbors):
            raise Exception("No such connection exists")

        node1.neighbors.remove(node2)
        node1.num_neighbors -= 1

        node2.neighbors.remove(node1)
        node2.num_neighbors -= 1

    def add_node(self,node):
        if node is None:
            raise Exception("Node cannot be None type")
        if node in self.nodes:
            raise Exception("Node already in graph")

        self.nodes.add(node)
        self.cured_nodes.add(node)
        self.num_nodes += 1

        return node

    def delete_node(self,node):
        if node is None:
            raise Exception("Node cannot be None type")
        if not(node in self.nodes):
            raise Exception("Node not in graph")

        for neighbor in node.neighbors:
            self.delete_connection(node,neighbor)
        self.nodes.remove(node)
        self.num_nodes -= 1

    def adjacent_nodes(self,node):
        return node.neighbors

    #infect = 1, cure = 0
    def set_state(self,node,state):
        if state != 0 and state != 1:
            raise Exception("Infection state must be 0 or 1")

        if state == 0:
            node.cure()
            self.cured_nodes.add(node)
            self.infected_nodes.remove(node)

        if state == 1:
            node.infect()
            self.cured_nodes.remove(node)
            self.infected_nodes.add(node)

    def infect(self,node):
        self.set_state(node,1)

    def cure(self,node):
        self.set_state(node,0)

    def random_sample(self,num_nodes):
        return sample(nodes,num_nodes)

    def cure_distribution_sample(self, param, distribution_type, use_default = False):
        if use_default:
            lambda_param = self.cure_param
        else:
            lambda_param = param

        if distribution_type == 'exponential':
            return np.random.exponential(1/lambda_param)

    def infect_distribution_sample(self, param, distribution_type, use_default = False):
        if use_default:
            lambda_param = self.infect_param
        else:
            lambda_param = param

        if distribution_type == 'exponential':
            return np.random.exponential(1/lambda_param)
