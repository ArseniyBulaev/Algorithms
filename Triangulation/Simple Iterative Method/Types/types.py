
class Edge(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0},{0})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Triangle(object):
    def __init__(self, edges, triangles):
        self.edges = edges
        self.triangles = triangles

    def __repr__(self):
        return "({0}, {1}, {2})".format(*self.edges) + "\n"