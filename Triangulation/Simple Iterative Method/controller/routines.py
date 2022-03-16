from model.types import *


def area(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def add_edge(edge, triangulation):
    pass


def find_path_to_edge(edge, triangle):
    a, b, c = triangle.edges[0], triangle.edges[1], triangle.edges[2]



def iterative_triangulation(nodes):
    triangulation = None
    if len(nodes) < 3:
        return triangulation
    else:
        triangulation = Triangle(nodes[:3], [None, None, None])


    for i in range(3, len(nodes), 1):
        pass

    return triangulation
