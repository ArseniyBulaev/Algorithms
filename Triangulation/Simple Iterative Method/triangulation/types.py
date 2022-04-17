class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)


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