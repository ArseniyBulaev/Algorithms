from model.types import *


def area(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def iterative_triangulation(edges):
    triangulation = []
    if len(edges) < 3:
        return triangulation
    else:
        triangulation.append(Triangle(edges[:3], [None, None, None]))


    for i in range(3, len(edges), 1):
        pass

    return triangulation
