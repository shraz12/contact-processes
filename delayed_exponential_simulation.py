from event_queue import *
from population_graph import *
from graph_node import *
from graph_structures import *
import numpy as np
import matplotlib.pyplot as plt            


def run_simulation(tree, root, delay_time, queue, max_iterations):
    current_time = 0
    num_iterations = 0

    queue.insert(current_time, Event(1,None,root))

    while(not(queue.is_empty()) and num_iterations <= max_iterations):
        num_iterations += 1
        current_time, event = queue.pop_event()


        if event.state == 0:
            tree.cure(event.outgoing)
            event.outgoing.add_cure_time(current_time)


        if event.state == 1:
            if event.outgoing != None:
                temp_infect = tree.infect_distribution_sample(None,'exponential',use_default=True)

                #DIFFERS FROM FULL MARKOVIAN HERE
                if temp_infect + current_time < event.outgoing.recover_time + delay_time:
                    queue.insert(current_time + temp_infect, Event(1,event.incoming,event.outgoing))

            if event.incoming.infected_state == 0:
                tree.infect(event.incoming)
                event.incoming.add_infection_time(current_time)

                temp_recover = tree.cure_distribution_sample(None,'exponential',use_default=True)
                event.incoming.recover_time = current_time + temp_recover
                queue.insert(event.incoming.recover_time, Event(0,event.incoming, None))

                for node in event.incoming.get_neighbors():
                    temp_infect = tree.infect_distribution_sample(None,'exponential',use_default=True)
                    
                    #DIFFERS FROM FULL MARKOVIAN HERE
                    if temp_infect + current_time < event.incoming.recover_time + delay_time:
                        queue.insert(temp_infect+current_time,Event(1,event.incoming,node))

        print(str(current_time) + " | " + str(len(tree.infected_nodes)) + " | " + str(num_iterations))

    return current_time


infect_param = .5 #aka lambda
cure_rate = 1
degree = 4
gens = 7
max_iterations = 5e6
num_simulations=50

#Positive: 
delay_time = 0

finish_times = []
root_hits = []


for i in range(num_simulations):
    tree, root = build_tree(infect_param,cure_rate,degree,gens)
    queue = EventQueue(tree)
    finish_time = run_simulation(tree,root,delay_time,queue,max_iterations)
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