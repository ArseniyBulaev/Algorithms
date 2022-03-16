from model.types import *


def area(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def add_node(node, triangulation):
    pass


def find_path_to_node(node, triangle):
    a, b, c = triangle.nodes[0], triangle.nodes[1], triangle.nodes[2]



def iterative_triangulation(nodes):
    triangulation = None
    if len(nodes) < 3:
        return triangulation
    else:
        triangulation = Triangle(nodes[:3], [None, None, None])


    for i in range(3, len(nodes), 1):
        pass

    return triangulation
