from fheap import *

class EventQueue():
    def __init__(self,graph):
        self.graph = graph
        self.queue = FibonacciHeap()
        self.size = 0

    def insert(self,key,event):
        self.size += 1
        return self.queue.insert(key,event)

    def pop_event(self):
        if self.size <= 0:
            raise Exception("Queue is empty")

        self.size -= 1
        wrapper = self.queue.extract_min()
        return wrapper.key, wrapper.value

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

class Event():
    def __init__(self, state, outgoing_node, incoming_node):
        self.state = state
        self.outgoing = outgoing_node
        self.incoming = incoming_node
