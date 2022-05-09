class Node(object):
    def __init__(self, label):
        # Метка вершины
        self.label = label
        # Смежные вершины
        self.weighted_adjacent_nodes = []

    # Добавление смежной вершины вместе с её стоимостью
    def add_adjacent_node(self, adjacent_node, weight):  
        self.weighted_adjacent_nodes.append((adjacent_node, weight))
   
    def __repr__(self):
        # В качестве текстового представления выводится метка
        return self.label

class Graph(object):
    def __init__(self, nodes):
        # Список узлов графа
        self.nodes = nodes

    # Метод связывания двух узлов.
    # Узлы должны быть в графе.
    # Если это не так, метод инициирует завершение программы 
    def connect_nodes(self, first_node, second_node, weight):
        error_message = "узел с меткой '{0}' не принадлежит графу"

        assert first_node in self.nodes, error_message.format(first_node.label)
        assert second_node in self.nodes, error_message.format(first_node.label)

        first_node.add_adjacent_node(second_node, weight)
        second_node.add_adjacent_node(first_node, weight)