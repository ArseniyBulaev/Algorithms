class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
    	return "({0} {1})".format(round(self.x, 2), round(self.y, 2))

class Segment(object):
	def __init__(self, start_point, end_point):
		self.start_point = start_point
		self.end_point = end_point

	def __repr__(self):
		return "{0}".format(self.length()) + "\n"

	def length(self):
		return ((self.start_point.x - self.end_point.x)**2 + (self.start_point.y - self.end_point.y)**2)**0.5
			
	
# Nodes and triangles structure
	
class Triangle(object):
	def __init__(self, nodes, triangles):
		self.nodes = nodes
		self.triangles = triangles
	
	def __repr__(self):
		return "({0}, {1}, {2})".format(*self.nodes) + "\n"