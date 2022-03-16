
class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Triangle(object):
    def __init__(self, nodes, triangles):
        self.nodes = nodes
        self.triangles = triangles

    def __repr__(self):
        return "\n({0}, {1}, {2})\n".format(*self.nodes)