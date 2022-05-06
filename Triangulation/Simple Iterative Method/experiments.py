from objects import Node, Edge, Triangle, Triangulation
from enum import Enum
import copy
import plot as my_plot


def delaunay_check(triangle):
    def is_in_circumscribed_circle(base_triangle, tested_node):

        def sign(number):
            if number > 0:
                return 1
            else:
                return -1

        node_1, node_2, node_3 = base_triangle.nodes

        x0, y0 = tested_node.x, tested_node.y
        x1, y1 = node_1.x, node_1.y
        x2, y2 = node_2.x, node_2.y
        x3, y3 = node_3.x, node_3.y

        a = x1*y2 + y1*x3 + y3*x2 - x3*y2 - y3*x1 - x2*y1

        b = (x2 ** 2 + y2 ** 2) * y3 - (x3 ** 2 + y3 ** 2) * y2 - (x1 ** 2 + y1 ** 2) * y3 \
            + (x3 ** 2 + y3 ** 2) * y1 + (x1 ** 2 + y1 ** 2) * y2 - (x2 ** 2 + y2 ** 2) * y1

        c = (x2 ** 2 + y2 ** 2) * x3 - (x3 ** 2 + y3 ** 2) * x2 - (x1 ** 2 + y1 ** 2) * x3 \
            + (x3 ** 2 + y3 ** 2) * x1 + (x1 ** 2 + y1 ** 2) * x2 - (x2 ** 2 + y2 ** 2) * x1

        d = y1 * ((x2 ** 2 + y2 ** 2) * x3 - (x3 ** 2 + y3 ** 2) * x2)\
            + y2 * (-(x1 ** 2 + y1 ** 2) * x3 + (x3 ** 2 + y3 ** 2) * x1)\
            + y3 * ((x1 ** 2 + y1 ** 2) * x2 - (x2 ** 2 + y2 ** 2) * x1)

        return (a*(x0**2 + y0**2) - b*x0 + c*y0 - d) * sign(a) < 0

    for node in triangle.nodes:
        opposite_edge = triangle.get_opposite_edge(node)
        opposite_triangle = triangle.get_opposite_triangle(node, return_index=False)
        if opposite_triangle is not None:
            node_to_check = opposite_triangle.get_opposite_node(opposite_edge, return_index=False)

            if is_in_circumscribed_circle(triangle, node_to_check):
                return opposite_edge, False

    return None, True


def inside_case(old_triangle, new_node):
    new_triangles = []

    # Создаём новые треугольники, проходя по всем рёбрам
    for edge in old_triangle.get_edges():
        new_triangle = create_triangle_base_on(old_triangle, edge, new_node)
        new_triangles.append(new_triangle)

    node_1, node_2, node_3 = old_triangle.nodes

    # Связываем вновь созданные треугольники
    for edge in [Edge(node_1, new_node), Edge(node_2, new_node), Edge(node_3, new_node)]:
        # Ищем смежные по данному ребру треугольники
        joint_triangles = get_joint_edge_pair(new_triangles, edge)
        tr1, tr2 = joint_triangles

        # Выполняем их связывание по ребру edge
        connect_along_edge(tr1, tr2, edge)

    # for new_triangle in new_triangles:
    #     my_plot.plot_triangle_with_neighbors(new_triangle, plot_nodes=False)
    #     my_plot.show()

    return new_triangles


def connect_along_edge(tr1, tr2, edge):
    # Соединяет треугольники по ребру
    tr_1_opp_node, tr_1_opp_node_index = tr1.get_opposite_node(edge)
    tr_2_opp_node, tr_2_opp_node_index = tr2.get_opposite_node(edge)

    # Вроде как не обязательное условие.
    # Не будет выполнено если edge не принадлежит tr1 или tr2
    if tr_1_opp_node is not None and tr_2_opp_node is not None:
        tr1.triangles[tr_1_opp_node_index] = tr2
        tr2.triangles[tr_2_opp_node_index] = tr1

        return True
    else:
        return False


def get_joint_edge_pair(triangles, edge):
    # Возвращает смежную по данному ребру пару треугольников
    # (Данные треугольники пока не связаны друг с другом)
    joint_pair = []

    for triangle in triangles:
        opp_node, opp_node_index = triangle.get_opposite_node(edge)
        if opp_node is not None:
            joint_pair.append(triangle)

        if len(joint_pair) == 2:
            return joint_pair

    return None


def create_triangle_base_on(base_triangle, base_edge, new_node):
    # Создаёт новый треугольник внутри base_triangle c
    # основанием base_edge и дополнитеоьной вершиной new_node

    # Получаем вершину противоположную ребру base_edge в base_triangle
    opp_node, opp_node_index = base_triangle.get_opposite_node(base_edge)

    # Получаем треугольник, лежащий напротив вершины opp_node
    opp_triangle = base_triangle.triangles[opp_node_index]

    # Создаём новый треугольник на основе старого
    new_triangle = copy.deepcopy(base_triangle)

    # Меняем противоположную к ребру base_edge вершину на new_node
    new_triangle.nodes[opp_node_index] = new_node
    new_triangle.triangles[opp_node_index] = opp_triangle

    # Если opp_triangle существует
    if opp_triangle is not None:
        # Получаем вершину противоположную ребру base_edge в opp_triangle
        opp_node, opp_node_index = opp_triangle.get_opposite_node(base_edge)

        # Связываем opp_triangle с new_triangle
        opp_triangle.triangles[opp_node_index] = new_triangle

    return new_triangle


def flip(target, flipping_edge):
    # target - треугольник, который инициирует переворот ребра
    # flipping_edge - ребро, которое нужно перевернуть

    # Получаем соседа с котором нужно осуществить переворот
    opp_node_in_target, neighbor_index = target.get_opposite_node(flipping_edge)
    neighbor = target.triangles[neighbor_index]
    opp_node_in_neighbor, target_index = neighbor.get_opposite_node(flipping_edge)

    # Получаем индексы узлов
    # flip_target_node_index - индекс узла для флипа в target
    # relink_target_node_index - индекс узла, по которому можно получить треугольник, переподвязываемый на neighbor
    flip_target_node_index = target.nodes.index(flipping_edge.first)
    relink_target_node_index = target.nodes.index(flipping_edge.second)

    # Получаем индексы узлов
    # flip_neighbor_node_index - индекс узла для флипа в neighbor
    # relink_neighbor_node_index - индекс узла, по которому можно получить треугольник, переподвязываемый на target
    flip_neighbor_node_index = neighbor.nodes.index(flipping_edge.second)
    relink_neighbor_node_index = neighbor.nodes.index(flipping_edge.first)

    # Получаем треугольник который нужно связать с neighbor
    relink_target_node = target.nodes[relink_target_node_index]
    relink_target_edge = target.get_opposite_edge(relink_target_node)
    relink_target_triangle = target.get_opposite_triangle(relink_target_node, return_index=False)

    # Получаем треугольник который нужно связать с target
    relink_neighbor_node = neighbor.nodes[relink_neighbor_node_index]
    relink_neighbor_edge = neighbor.get_opposite_edge(relink_neighbor_node)
    relink_neighbor_triangle = neighbor.get_opposite_triangle(relink_neighbor_node, return_index=False)

    # Осуществляем переворот ребра
    target.nodes[flip_target_node_index] = opp_node_in_neighbor
    neighbor.nodes[flip_neighbor_node_index] = opp_node_in_target
    # Связываем треугольники по правильному ребру
    connect_along_edge(target, neighbor, Edge(opp_node_in_target, opp_node_in_neighbor))

    # Переподвязываем старый треугольник в target
    if relink_neighbor_triangle is not None:
        connect_along_edge(target, relink_neighbor_triangle, relink_neighbor_edge)
    else:
        target.triangles[neighbor_index] = None
    # Переподвязываем старый треугольник в neighbor
    if relink_target_triangle is not None:
        connect_along_edge(neighbor, relink_target_triangle, relink_target_edge)
    else:
        neighbor.triangles[target_index] = None


def simple_iterative_method(nodes):

    triangulation = Triangulation()
    triangulation.add_triangle(Triangle(nodes[:3], [None, None, None]))

    # my_plot.plot_triangulation(triangulation)
    # my_plot.show()

    for i in range(3, len(nodes)):

        node = nodes[i]

        my_plot.plot_triangulation(triangulation, plot_nodes=True)
        my_plot.plot_node(node)
        my_plot.show()

        nearest_triangle = triangulation.find_nearest_triangle(node)
        is_in_triangle = nearest_triangle.node_position(node)

        if is_in_triangle:
            new_triangles = inside_case(nearest_triangle, node)
            triangulation.remove_triangle(nearest_triangle)
        else:
            print("IS NOT MY PROBLEM")

        for new_triangle in new_triangles:
            triangulation.add_triangle(new_triangle)

        for new_triangle in new_triangles:
            flipping_edge, is_correct = delaunay_check(new_triangle)
            if not is_correct:
                flip(new_triangle, flipping_edge)

    my_plot.plot_triangulation(triangulation, plot_nodes=True)
    my_plot.plot_node(node)
    my_plot.show()

    return triangulation
