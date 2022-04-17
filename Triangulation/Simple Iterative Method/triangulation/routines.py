from triangulation.types import *


def find_nearest_triangle(start, node):

    def signed_area(a, b, c):
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    def delete_node(node_index, nodes):
        # TO DO : Придумать нормальное название
        nodes_copy = nodes.copy()
        deleted_node = nodes_copy.pop(node_index)
        return deleted_node, nodes_copy


    for node_index in range(len(start.nodes)):
        a, edge = delete_node(node_index, start.nodes)
        b, c = edge

        q = Node(b.x - 5, b.y - 5)
        v = Node(c.x - 5, c.y - 5)
        z = Node(a.x - 5, a.y - 5)
        print("Выбранное ребро:", q, v)
        print("Противоположная вершина:", z)

        if signed_area(b, c, a) * signed_area(b, c, node) <= 0:
            if start.triangles[node_index] is None:
                return start
            else:

                return find_nearest_triangle(start.triangles[node_index], node)

    return start
