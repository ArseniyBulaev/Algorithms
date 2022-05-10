class Node(object):
    def __init__(self, label):
        # Метка вершины
        self.label = label
        # Смежные вершины c весами
        self.weighted_adjacent_nodes = dict()
    
   # Проверка того, что вершина находится в списке смежности текущей вершины
    def is_in_adjacent_nodes(self, adjacent_node):
        return adjacent_node in self.weighted_adjacent_nodes.keys()


    # Добавление смежной вершины вместе со стоимостью соединяющего ребра
    def add_adjacent_node(self, adjacent_node, weight):
        self.weighted_adjacent_nodes[adjacent_node] = weight


    # Удаление смежной вершины
    def remove_adjacent_node(self, node_to_remove):
        error_message = "вершина '{0}' не принадлежит списку смежности {1}"
        assert self.is_in_adjacent_nodes(node_to_remove), error_message.format(node_to_remove, self)
        
        # Удаление вершины
        self.weighted_adjacent_nodes.pop(node_to_remove)

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

        for adjacent_node in node_to_remove.weighted_adjacent_nodes.keys():
            
            # Удаление node_to_remove из смежных вершин adjacent_node
            adjacent_node.remove_adjacent_node(node_to_remove)
        
        # Удаление вершины из графа
        self.nodes.remove(node_to_remove)

    # Добавление связи двух вершин
    def connect_nodes(self, first_node, second_node, weight):
        
        error_message = "вершина с меткой '{0}' не принадлежит графу"
        assert self.is_in_nodes(first_node), error_message.format(first_node.label)
        assert self.is_in_nodes(second_node), error_message.format(first_node.label)

        first_node.add_adjacent_node(second_node, weight)
        second_node.add_adjacent_node(first_node, weight)

    # Удаление связи двух вершин
    def disconnect_nodes(self, first_node, second_node):
        error_message = "вершина с меткой '{0}' не принадлежит графу"
        assert self.is_in_nodes(first_node), error_message.format(first_node.label)
        assert self.is_in_nodes(second_node), error_message.format(first_node.label)

        first_node.remove_adjacent_node(second_node)
        second_node.remove_adjacent_node(first_node)
    
    # Объединение вершин
    def merge_nodes(self, first, second):

        error_message = "вершина с меткой '{0}' не принадлежит графу"
        assert self.is_in_nodes(first), error_message.format(first.label)
        assert self.is_in_nodes(second), error_message.format(first.label)
        
        local_cut = 0
        global_cut = local_cut
        
        # Проход по всем смежным вершинам second
        for adjacent_node in second.weighted_adjacent_nodes.keys():

            # Сохранение веса смежной вершины
            local_cut = second.weighted_adjacent_nodes[adjacent_node]
           
            # Если эта вершина находится в смежных вершинах first
            if adjacent_node in first.weighted_adjacent_nodes.keys():

               # Суммирование веса этой вершины со смежной вершиной в first
               first.weighted_adjacent_nodes[adjacent_node] += local_cut
               adjacent_node.weighted_adjacent_nodes[first] += local_cut
            
            # Сохранение величины глобального разреза
            global_cut += local_cut

        # Отсоединение second от всех смежных вершин
        for adjacent_node in list(second.weighted_adjacent_nodes.keys()):
            self.disconnect_nodes(adjacent_node, second)
        
        # Удаление second
        self.remove_node(second)
        first.label = "{0} , {1}".format(first.label, second.label) 

        # Возвращение величины глобального разреза
        return global_cut