from objects import Node, Edge, Triangle, Triangulation
from enum import Enum
import plot as my_plot
import copy
from scipy.spatial import ConvexHull, convex_hull_plot_2d


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

        # Связываем opp_triangle с base_triangle
        opp_triangle.triangles[opp_node_index] = new_triangle

    return new_triangle


def check_on_point_case(triangle, new_node, info):
    for node in triangle.nodes:
        if node == new_node:
            info["position"] = 1
            return True

    return False


def check_on_edge_case(triangle, new_node, info):
    def signed_area(a, b, c):
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    for edge in triangle.get_edges():
        if signed_area(edge.first, edge.second, new_node) == 0:
            info["position"] = 2
            info["occupied edge"] = edge
            return True

    return False


def check_inside_case(triangle, new_node, info):

    def triangle_area(n1, n2, n3):
        s = 1 / 2 * (n1.x * (n2.y - n3.y) + n2.x * (n3.y - n1.y) + n3.x * (n1.y - n2.y))
        return s

    def is_inside_case():
        nodes = triangle.nodes

        base_triangle_area = triangle_area(nodes[0], nodes[1], nodes[2])
        sub_triangle1_area = triangle_area(new_node, nodes[1], nodes[2])
        if sub_triangle1_area < 0:
            print("AAA")
        sub_triangle2_area = triangle_area(nodes[0], new_node, nodes[2])
        if sub_triangle2_area < 0:
            print("AAA")
        sub_triangle3_area = triangle_area(nodes[0], nodes[1], new_node)
        if sub_triangle3_area < 0:
            print("AAA")

        if base_triangle_area == (sub_triangle1_area + sub_triangle2_area + sub_triangle3_area):
            return True
        else:
            return False

    if is_inside_case():
         info["position"] = 3
         return True
    else:
        return False


def check_node_position_relative_triangle(triangle, new_node):
    info = dict()
    info["position"] = -1  # Позиция узла ещё не известна

    n_1, n_2, n_3 = triangle.nodes

    a = (n_1.x - new_node.x) * (n_2.y - n_1.y) - (n_2.x - n_1.x) * (n_1.y - new_node.y)
    b = (n_2.x - new_node.x) * (n_3.y - n_2.y) - (n_3.x - n_2.x) * (n_2.y - new_node.y)
    c = (n_3.x - new_node.x) * (n_1.y - n_3.y) - (n_1.x - n_3.x) * (n_3.y - new_node.y)

    if new_node == n_1 or new_node == n_2 or new_node == n_3:
        info["position"] = 1
    elif a == 0 or b == 0 or c == 0:
        info["position"] = 2
        if a == 0:
            info["occupied edge"] = Edge(n_1, n_2)
        elif b == 0:
            info["occupied edge"] = Edge(n_2, n_3)
        elif c == 0:
            info["occupied edge"] = Edge(n_1, n_3)

    elif (a > 0 and b > 0 and c > 0) or (a < 0 and b < 0 and c < 0):
        info["position"] = 3
    else:
        info["position"] = 4

    return info


def outside_case(triangulation, nodes, new_node):
    new_triangles = []

    nodes.insert(0, new_node)
    generators = [[node.x, node.y] for node in nodes]
    hull = ConvexHull(points=generators, qhull_options='QG0')

    for visible_facet in hull.simplices[hull.good]:
        scipy_edge = hull.points[visible_facet]
        visible_node_1 = Node(int(scipy_edge[0][0]), int(scipy_edge[0][1]))
        visible_node_2 = Node(int(scipy_edge[1][0]), int(scipy_edge[1][1]))
        visible_edge = Edge(visible_node_1, visible_node_2)

        joint_triangle = triangulation.find_triangle_by_edge(visible_edge)
        new_triangle = Triangle([visible_node_1, visible_node_2, new_node], [None, None, None])

        # Выполняем их связывание по ребру visible_edge
        connect_along_edge(joint_triangle, new_triangle, visible_edge)

        if len(new_triangles) > 0:
            adjacent_triangle = new_triangles[-1]
            for possible_adjacent_edge in new_triangle.get_edges():
                if possible_adjacent_edge != visible_edge:
                    if get_joint_edge_pair([adjacent_triangle, new_triangle], possible_adjacent_edge) is not None:
                        connect_along_edge(adjacent_triangle, new_triangle, possible_adjacent_edge)

        new_triangles.append(new_triangle)

    return new_triangles


def on_edge_case(base_triangle, new_node, occupied_edge, triangulation):
    def split_triangle(triangle):

        local_new_triangles = []

        # Создаём новые треугольники проходом по всем рёбрам кроме того, на котором находится точка
        for edge in triangle.get_edges():
            if edge == occupied_edge:
                continue
            new_triangle = create_triangle_base_on(triangle, edge, new_node)
            local_new_triangles.append(new_triangle)

        node_1, node_2, node_3 = triangle.nodes

        # Получаем совместное ребро
        opp_node_l, opp_node_index_l = triangle.get_opposite_node(occupied_edge)
        joint_edge = Edge(opp_node_l, new_node)

        # Ищем смежные по данному ребру треугольники
        local_joint_triangles = get_joint_edge_pair(local_new_triangles, joint_edge)

        tr1_l, tr2_l = local_joint_triangles

        # Выполняем их связывание по ребру edge
        connect_along_edge(tr1_l, tr2_l, joint_edge)

        return local_new_triangles

    opp_node, opp_node_index = base_triangle.get_opposite_node(occupied_edge)
    adjacent_triangle = base_triangle.triangles[opp_node_index]

    new_triangles = split_triangle(base_triangle)
    if adjacent_triangle is not None:
        new_triangles += split_triangle(adjacent_triangle)

    first_part_of_occupied_edge = Edge(occupied_edge.first, new_node)
    second_part_of_occupied_edge = Edge(new_node, occupied_edge.second)

    triangles_to_join = new_triangles.copy()

    for edge in [first_part_of_occupied_edge, second_part_of_occupied_edge]:
        # Ищем смежные по данному ребру треугольники
        joint_triangles = get_joint_edge_pair(triangles_to_join, edge)

        if joint_triangles is not None:
            tr1, tr2 = joint_triangles

            # Выполняем их связывание по ребру edge
            connect_along_edge(tr1, tr2, edge)

            triangles_to_join.remove(tr1)
            triangles_to_join.remove(tr2)

    return new_triangles


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

    return new_triangles


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

    # # Осуществляем переворот ребра
    target.nodes[flip_target_node_index] = opp_node_in_neighbor
    neighbor.nodes[flip_neighbor_node_index] = opp_node_in_target
    # Связываем треугольники по правильному ребру
    connect_along_edge(target, neighbor, Edge(opp_node_in_target, opp_node_in_neighbor))

    # Переподвязываем старый треугольник в target
    if relink_neighbor_triangle is not None:
        connect_along_edge(target, relink_neighbor_triangle, relink_neighbor_edge)
    else:
        target.nodes[neighbor_index]
        target.triangles[neighbor_index] = None
    # Переподвязываем старый треугольник в neighbor
    if relink_target_triangle is not None:
        connect_along_edge(neighbor, relink_target_triangle, relink_target_edge)
    else:
        neighbor.triangles[target_index] = None


def simple_iterative_method(nodes, triangulation=None):
    class NodePos(Enum):
        ON_POINT = 1
        ON_EDGE = 2
        INSIDE_TRIANGLE = 3
        OUTSIDE_TRIANGLE = 4

    triangulation = Triangulation()
    triangulation.add_triangle(Triangle(nodes[:3], [None, None, None]))

    for i in range(3, len(nodes)):
        node = nodes[i]

        nearest_triangle = triangulation.find_nearest_triangle(node)
        info = check_node_position_relative_triangle(nearest_triangle, node)

        print(NodePos(info["position"]))

        if NodePos(info["position"]) == NodePos.OUTSIDE_TRIANGLE:
            new_triangles = outside_case(triangulation, nodes[:i], node)

        elif NodePos(info["position"]) == NodePos.ON_POINT:
            continue

        elif NodePos(info["position"]) == NodePos.ON_EDGE:
            new_triangles = on_edge_case(nearest_triangle, node, info["occupied edge"], triangulation)
            opp_node, opp_node_index = nearest_triangle.get_opposite_node(info["occupied edge"])
            adjacent_triangle = nearest_triangle.triangles[opp_node_index]

            triangulation.remove_triangle(nearest_triangle)
            if adjacent_triangle is not None:
                triangulation.remove_triangle(adjacent_triangle)

        elif NodePos(info["position"]) == NodePos.INSIDE_TRIANGLE:
            new_triangles = inside_case(nearest_triangle, node)
            triangulation.remove_triangle(nearest_triangle)

        for new_triangle in new_triangles:
            triangulation.add_triangle(new_triangle)

        for new_triangle in new_triangles:
            flipping_edge, is_correct = delaunay_check(new_triangle)
            if not is_correct:
                flip(new_triangle, flipping_edge)

        for triangle in triangulation.triangles:
            flipping_edge, is_correct = delaunay_check(triangle)
            if not is_correct:
                flip(triangle, flipping_edge)

        # something_wrong = True
        #
        # while something_wrong:
        #     something_wrong = False
        #     for triangle in triangulation.triangles:
        #         flipping_edge, is_correct = delaunay_check(triangle)
        #         if not is_correct:
        #             something_wrong = True
        #             flip(triangle, flipping_edge)

    return triangulation
