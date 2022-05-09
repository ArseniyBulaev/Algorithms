class Node(object):
    def __init__(self, label):
        # Метка вершины
        self.label = label
        # Смежные вершины
        self.adjacent_nodes = []
        # Веса рёбер к смежным вершинам
        self.weights_of_adjacent_nodes = []
    
   # Проверка того, что вершина находится в списке смежности текущей вершины
    def is_in_adjacent_nodes(self, adjacent_node):
        return adjacent_node in self.adjacent_nodes


    # Добавление смежной вершины вместе со стоимостью соединяющего ребра
    def add_adjacent_node(self, adjacent_node, weight):
        self.weights_of_adjacent_nodes.append(weight)
        self.adjacent_nodes.append(adjacent_node)


    # Удаление смежной вершины
    def remove_adjacent_node(self, node_to_remove):
        error_message = "вершина '{0}' не принадлежит списку смежности {1}"
        assert self.is_in_adjacent_nodes(node_to_remove), error_message.format(node_to_remove, self)
        
        # Получение индекса удаляемой вершины
        remove_index = self.adjacent_nodes.index(node_to_remove)

        # Удаление самой вершины
        self.adjacent_nodes.pop(remove_index)
        # и её веса
        self.weights_of_adjacent_nodes.pop(remove_index)

    def __repr__(self):
        # В качестве текстового представления выводится метка
        return self.label

class Graph(object):
    def __init__(self, nodes):
        # Список вершин графа
        self.nodes = nodes

    # Проверка принадлежности вершины графу
    def is_in_nodes(self, node):
        return node in self.nodes
    
    # Добавление вершины в граф
    def add_node(self, node):
        self.nodes.append(node)

    # Удаление вершины из графа
    def remove_node(self, node_to_remove):

        not_in_graph_error_message = "вершина '{0}' не принадлежит графу"
        assert self.is_in_nodes(node_to_remove), not_in_graph_error_message.format(node_to_remove)

        for adjacent_node_index in range(len(node_to_remove.adjacent_nodes)):
            # Смежная вершина
            adjacent_node = node_to_remove.adjacent_nodes[adjacent_node_index]

            # Удаление node_to_remove из смежных вершин adjacent_node
            adjacent_node.remove_adjacent_node(node_to_remove)
        
        # Удаление вершины из графа
        self.nodes.remove(node_to_remove)

    # Добавление связи двух вершин
    def connect_nodes(self, first_node, second_node, weight):
        
        error_message = "узел с меткой '{0}' не принадлежит графу"
        assert self.is_in_nodes(first_node), error_message.format(first_node.label)
        assert self.is_in_nodes(second_node), error_message.format(first_node.label)

        first_node.add_adjacent_node(second_node, weight)
        second_node.add_adjacent_node(first_node, weight)

    # Удаление связи двух вершин
    def disconnect_nodes(self, first_node, second_node):
        error_message = "узел с меткой '{0}' не принадлежит графу"
        assert self.is_in_nodes(first_node), error_message.format(first_node.label)
        assert self.is_in_nodes(second_node), error_message.format(first_node.label)

        first_node.remove_adjacent_node(second_node)
        second_node.remove_adjacent_node(first_node)