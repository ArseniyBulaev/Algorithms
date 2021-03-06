import random

# () - Node
# <> - Edge
# [] - Triangle
# -- -- - Triangulation 


class Node(object):
    __output_string__ = "({0},{1})"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.__output_string__.format(self.x, self.y)

    def __repr__(self):
        return self.__output_string__.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Edge(object):
    __output_string__ = "<{0},{1}>"

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return self.__output_string__.format(self.first, self.second)

    def __repr__(self):
        return self.__output_string__.format(self.first, self.second)

    def __eq__(self, other):
        return ((self.first == other.first and self.second == other.second)
                or
                (self.first == other.second and self.second == other.first))


class Triangle(object):
    def __init__(self, nodes, triangles, number=None):
        self.nodes = nodes
        self.triangles = triangles
        self.number = number

    def __str__(self):
        return str(self.nodes)

    def __repr__(self):
        return str(self.nodes)

    def get_center(self):
        center_x = (self.nodes[0].x + self.nodes[1].x + self.nodes[2].x) / 3
        center_y = (self.nodes[0].y + self.nodes[1].y + self.nodes[2].y) / 3
        return Node(center_x, center_y)

    def get_opposite_node(self, edge, return_index=True):
        if edge not in self.get_edges():
            if return_index:
                return None, -1
            else:
                return None
        for node_index, node in enumerate(self.nodes):
            if node != edge.first and node != edge.second:
                if return_index:
                    return node, node_index
                else:
                    return node

    def get_opposite_triangle(self, node, return_index=True):
        node_index = self.nodes.index(node)
        if return_index:
            return self.triangles[node_index], node_index
        else:
            return self.triangles[node_index]

    def get_opposite_edge(self, node):
        nodes_copy = self.nodes.copy()
        nodes_copy.remove(node)
        first, second = nodes_copy
        return Edge(first, second)

    def get_edges(self):
        edges = [
            Edge(self.nodes[0], self.nodes[1]),
            Edge(self.nodes[1], self.nodes[2]),
            Edge(self.nodes[2], self.nodes[0])
        ]
        return edges


class Triangulation(object):

    def __str__(self):
        return "--\n{0}\n--".format("\n".join([str(triangle) for triangle in self.triangles]))

    def __repr__(self):
        return "--\n{0}\n--".format("\n".join([str(triangle) for triangle in self.triangles]))

    def __init__(self, triangles=[]):
        self.triangles = triangles
        self.triangles_count = len(triangles)

    def add_triangle(self, triangle):
        triangle.number = self.triangles_count
        self.triangles.append(triangle)
        self.triangles_count += 1

    def remove_triangle(self, triangle):
        self.triangles.remove(triangle)
        self.triangles_count -= 1

    def find_triangle_by_edge(self, edge):
        for triangle in self.triangles:
            edges = triangle.get_edges()
            if edge in edges:
                return triangle
        return None

    def find_nearest_triangle(self, new_node):
        # ?????????????? ???????????? ???????????????????? ?? ?????????????? ???????? ????????????????????????

        def signed_area(a, b, c):
            return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

        def is_split_by_edge(a, b, edge):
            # ???????????????? ?????????????????? ???? ???????? a ?? b
            # ???? ???????????? ?????????????? ???? ?????????? edge
            return signed_area(edge.first, edge.second, a) * signed_area(edge.first, edge.second, b) < 0

        def recursive_search(triangle):

            for edge in triangle.get_edges():
                # ?????????????? ?????????????????? ???? ???????????? ????????????
                # ?????????????????????? ?????????? ???????????????????????? ?? ?????????? ????????
                if is_split_by_edge(triangle.get_center(), new_node, edge):

                    # ???????? ??????????????????, ????
                    # ?????????? ?????????????????????????????? ?????????????? ?? ?????????????? ??????????
                    # ?? ?????????????? ???? ?????? ?????????????????????????????? ??????????????????????
                    opposite_node, opposite_node_index = triangle.get_opposite_node(edge)
                    opposite_triangle = triangle.triangles[opposite_node_index]

                    # ???????? ???? ????????????????????
                    if opposite_triangle is not None:
                        # ?????????????????? ?? ???????? ?? ???????????????????? ??????????
                        return recursive_search(opposite_triangle)
                    else:
                        # ?????????? ???????????????????? ?????????????? ??????????????????????, ?????? ??????
                        # ?? ???????? ???????????? ???? ?????????? ?????????? ?????????????? ?? ?????????????? ????????
                        return triangle

            # ???????? ?????????? ????????, ????
            # ?????????????????????? ?????????? ???????????????????????? ?? ?????????? ????????
            # ?????????? ?? ?????????? ????????????????????????,
            # ?? ???? ?????? ????????????????????
            return triangle

        # ???????????????? ?????????? ???? ???????????????????? ???????????????????????? ????????????????????????
        # ???????????? ???????????????????? ???????????????????????? ???? ????????????????????????
        rand_index = random.randint(0, len(self.triangles) - 1)

        return recursive_search(self.triangles[rand_index])
