

class GraphNode():
    def __init__(self,data,depth = None, name = None):
        self.data = data
        self.name = name
        self.neighbors = set()
        self.num_neighbors = 0
        
        self.depth = depth

        self.infected_state = 0

        self.infection_times = []
        self.cure_times = []
        self.num_infections = 0

        self.recover_time = float('inf')


    def get_data(self):
        return self.data

    def get_neighbors(self):
        return self.neighbors

    def get_state(self):
        return self.infected_state

    def infect(self):
        if self.infected_state == 1:
            raise Exception("Node already infected")
        self.infected_state = 1
        self.num_infections += 1

    def cure(self):
        if self.infected_state == 0:
            raise Exception("Node already cured")
        self.infected_state = 0

    def add_infection_time(self,time):
        self.infection_times.append(time)

    def add_cure_time(self,time):
        self.cure_times.append(time)
