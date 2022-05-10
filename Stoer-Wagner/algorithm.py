import operator
import random
from graph_objects import Graph
from copy import deepcopy
import graphviz_support as gviz_s

# Поиск минимального разреза в графе методом Штор-Вагнера
# G - граф
# a - вершина, из которой начинается поиск
def minimum_cut(G_input):
    
    G = deepcopy(G_input)
    minimum_cut = 100000
    N = G.nodes
    
    # Для отладки
    i = 1

    # Пока множество вершин имеет болеше одной вершины
    while len(N) > 1:

        # Индекс случайной вершины, с которой начинается фаза разреза
        start_index = random.randint(0, len(N) - 1)

        # Выполненение фазы поиска минимального разреза в графе
        cut_of_the_phase = minimum_cut_phase(G, N[start_index])

        # Если текущий минимальный разрез больше найденного на текущей фазе
        if minimum_cut > cut_of_the_phase:

            # Обновление текущего минимального разреза
            minimum_cut = cut_of_the_phase
        
        # Для отладки
        gviz_graph = gviz_s.graph_object_to_graphviz_object(G, graph_name=str(i))
        gviz_s.render_graph(gviz_graph)
        i += 1
    
    # Возвращение глобального минимального разреза
    return minimum_cut

# Фаза поиска минимального разреза в графе
def minimum_cut_phase(G, a):
    # Инициализация начальной вершиной подмножества A (Исследованные вершины)
    A = [a] 

    # Пока множество вершин не совпадает с исходным множеством вершин графа
    while len(A) != len(G.nodes):

        # Нахождение наиболее связной вершины
        most_connected_node = get_most_connected_node(A)

        # Добавление в A наиболее связной вершины
        A.append(most_connected_node)

    # Уменьшение G путём слияния двух вершин, добавленных последними
    # и запоминание цены разреза на этой фазе
    cut_of_the_phase = G.merge_nodes(A[-2], A[-1])
    
    # Возвращение найденного на текущей фазе минимального разреза
    return cut_of_the_phase

# Функия получения наиболее связной с множеством A вершины
def get_most_connected_node(A):

    # Словарь, в котором ключи - это достижимые вершины,
    # а значения - это связность данных вершин
    node_connectivity = dict()

    # Проход по всем вершинам из A
    for a in A:
        # Проход по всем смежным вершинам a 
        for adjacent_node in a.weighted_adjacent_nodes.keys():
            # Если смежная вершина не находится в A
            if adjacent_node not in A:
                # Добавление её в словарь достижимых вершин

                # Если она еще не в словаре
                if adjacent_node not in node_connectivity:
                    # Инициализация элемента словоря весом текущей вершины
                    node_connectivity[adjacent_node] = a.weighted_adjacent_nodes[adjacent_node]
                # Иначе
                else:
                    # Cуммирование с предыдущим значением
                    node_connectivity[adjacent_node] += a.weighted_adjacent_nodes[adjacent_node]


    # Возращение вершины с максимальной связностью
    return max(node_connectivity.items(), key=operator.itemgetter(1))[0]
