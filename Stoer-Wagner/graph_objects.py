class Node(object):
    def __init__(self, label):
        # Метка вершины
        self.label = label
        # Смежные вершины
        self.weighted_adjacent_nodes = []
    
    def add_adjacent_node(self, adjacent_node, weight):  
        # Добавление смежной вершины вместе с её стоимостью
        self.weighted_adjacent_nodes.append((adjacent_node, weight))

    
    def __repr__(self):
        return self.label

class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def connect_nodes(self, first_node, second_node, weight):
        error_message = "узел с меткой '{0}' не принадлежит графу"

        assert first_node in self.nodes, error_message.format(first_node.label)
        assert second_node in self.nodes, error_message.format(first_node.label)

        first_node.add_adjacent_node(second_node, weight)
        second_node.add_adjacent_node(first_node, weight)