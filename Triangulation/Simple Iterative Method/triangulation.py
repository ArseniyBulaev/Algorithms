class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Triangle(object):
    def __init__(self, nodes, triangles, number=None):
        self.number = number
        self.nodes = nodes
        self.triangles = triangles

    def __repr__(self):
        return "{0}".format(self.nodes)

    def center(self):
        x = (self.nodes[0].x + self.nodes[1].x + self.nodes[2].x) / 3
        y = (self.nodes[0].y + self.nodes[1].y + self.nodes[2].y) / 3
        return Node(x, y)

    def get_other_nodes(self, node):
        other_nodes = self.nodes.copy()
        other_nodes.remove(node)
        return other_nodes


def find_nearest_triangle(current_triangle, new_node, came_from=None):
    def signed_area(a, b, c):
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    for node_index, node in enumerate(current_triangle.nodes):
        # Ребро, которое лежит напротив данного узла
        edge = current_triangle.get_other_nodes(node)
        # Узлы ребра, которое лежит напротив проверяемого узла
        node_1, node_2 = edge
        # Проверяем, что текущий и новый узел
        # лежат по разную сторону от данного ребра
        if signed_area(node_1, node_2, node) * signed_area(node_1, node_2, new_node) <= 0:
            # Получаем треугольник, которые лежит напротив данного узла
            next_triangle = current_triangle.triangles[node_index]

            # Предотвращаем зацикливание
            if came_from is not None:
                if next_triangle is came_from:
                    return current_triangle

            if next_triangle is None:
                # Если такого нет, то ближайшим будет тот, который мы рассматриваем
                return current_triangle
            else:
                # Иначе запускаем рекурсивно для противолежащего треугольника
                return find_nearest_triangle(next_triangle, new_node, came_from=current_triangle)

    # Если дошли до сюда, то новая точка лежит в текущем треугольнике
    return current_triangle
