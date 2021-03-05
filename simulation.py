from event_queue import *
from population_graph import *
from graph_node import *
import numpy as np
import matplotlib.pyplot as plt

def build_tree(infect_rate,cure_rate,degree, gens):
    tree = PopulationGraph(infect_rate,cure_rate)
    root = tree.add_node(GraphNode(None))
    counter = 0

    tree_helper(tree,root,degree,gens,counter)
    temp_node = tree.add_node(GraphNode(None))

    return tree, root, temp_node

def tree_helper(tree,node,degree,gens,counter):
    if counter < gens:
        for i in range(degree):
            end = tree.add_node(GraphNode(None))
            tree.add_connection(node,end)
            tree_helper(tree, end, degree, gens, counter+1)


def run_simulation(tree, root, temp_node, queue, max_iterations):
    current_time = 0
    num_iterations = 0

    queue.insert(current_time, Event(1,temp_node,root))

    while(not(queue.is_empty()) and num_iterations <= max_iterations):
        num_iterations += 1
        current_time, event = queue.pop_event()


        if event.state == 0:
            tree.cure(event.outgoing)
            event.outgoing.add_cure_time(current_time)


        if event.state == 1:
            if event.outgoing != temp_node:
                temp_infect = tree.infect_distribution_sample(None,'exponential',use_default=True)

                if temp_infect + current_time < event.outgoing.recover_time:
                    queue.insert(current_time + temp_infect, Event(1,event.incoming,event.outgoing))

            if event.incoming.infected_state == 0:
                tree.infect(event.incoming)
                event.incoming.add_infection_time(current_time)

                temp_recover = tree.cure_distribution_sample(None,'exponential',use_default=True)
                event.incoming.recover_time = current_time + temp_recover
                queue.insert(event.incoming.recover_time, Event(0,event.incoming,temp_node))

                for node in event.incoming.get_neighbors():
                    temp_infect = tree.infect_distribution_sample(None,'exponential',use_default=True)
                    if temp_infect + current_time < event.incoming.recover_time:
                        queue.insert(temp_infect+current_time,Event(1,event.incoming,node))

        print(str(current_time) + " | " + str(len(tree.infected_nodes)) + " | " + str(num_iterations))

    return current_time


infect_param = 1.25 #aka lambda
cure_rate = 1
degree = 4
gens = 7
max_iterations = 5e6
num_simulations=25

finish_times = []
root_hits = []


for i in range(num_simulations):
    tree, root, temp_node = build_tree(infect_param,cure_rate,degree,gens)
    queue = EventQueue(tree)
    finish_time = run_simulation(tree,root,temp_node,queue,max_iterations)
    finish_times.append(finish_time)
    root_hits.append(len(root.infection_times))

print(finish_times)
print(root_hits)

plt.figure(1)
plt.hist(finish_times)
plt.title("Infection Survival Times")
plt.plot()

plt.figure(2)
plt.hist(root_hits)
plt.title("Number of Root Hits")
plt.plot()