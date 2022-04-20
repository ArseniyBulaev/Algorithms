from triangulation_objects import Node, Triangle


def signed_area(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def find_nearest_triangle(current_triangle, new_node, came_from=None):

    for current_node_index, current_node in enumerate(current_triangle.nodes):
        # Ребро, которое лежит напротив данного узла
        opposite_edge = current_triangle.get_other_nodes(current_node)

        # Проверяем, что текущий и новый узел
        # лежат по разную сторону от данного ребра
        if signed_area(opposite_edge[0], opposite_edge[1], current_node)\
                * signed_area(opposite_edge[0], opposite_edge[1], new_node) <= 0:

            # Получаем треугольник, которые лежит напротив данного узла
            next_triangle = current_triangle.triangles[current_node_index]

            # Если следующий треугольник тот, из которого мы пришли, то возвращаем текщий треугольник
            if came_from is not None and next_triangle is came_from:
                return current_triangle

            if next_triangle is None:
                # Если такого нет, то ближайшим будет тот, который мы рассматриваем
                return current_triangle
            else:
                # Иначе запускаем рекурсивно для противолежащего треугольника
                return find_nearest_triangle(next_triangle, new_node, came_from=current_triangle)

    # Если дошли до сюда, то новая точка лежит в текущем треугольнике
    return current_triangle


def get_node_position_type(triangle, node):
    return ''


def position_based_action(node_position_type, triangulation, nearest_triangle):
    return []



def delaunay_check(triangle):
    return False, None


def flip(triangle, unsatisfying_node):
    pass



def simple_iterative_algorithm(nodes):
    # Строим первый треугольник
    triangulation = Triangle([nodes[0], nodes[1], nodes[2]])

    for node in nodes[3:]:
        # Ближайший к данному узлу треугольник
        nearest_triangle = find_nearest_triangle(triangulation, node, None)

        # Тип Позиции нового узла относительно найденного треугольника
        # 'edge' - на ребре
        # 'inside' - внутри
        # 'outside'- снаружи
        node_position_type = get_node_position_type(nearest_triangle, node)

        # Стрим новые треугольники
        triangles_to_check = position_based_action(node_position_type, triangulation, nearest_triangle)

        # Проверяем построенные треугольники
        for triangle in triangles_to_check:
            delaunay_is_done, unsatisfying_node = delaunay_check(triangle)
            if not delaunay_is_done:
                flip(triangle, unsatisfying_node)