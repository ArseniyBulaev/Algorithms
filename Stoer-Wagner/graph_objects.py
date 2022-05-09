class Node(object):
    def __init__(self, label, nodes):
        self.label = label
        self.weighted_adjacent_nodes = nodes
    
    def __repr__(self):
        return self.label

class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes