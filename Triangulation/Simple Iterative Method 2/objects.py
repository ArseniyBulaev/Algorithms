# () - Node
# <> - Edge
# [] - Triangle
# -- -- - Triangulation 


class Node(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "({0},{1})".format(self.x, self.y)

	def __repr__(self):
		return "({0},{1})".format(self.x, self.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

class Edge(object):
	def __init__(self, first, second):
		self.first = first
		self.second = second

	def __str__(self):
		return "<{0},{1}>".format(self.first, self.second)

	def __repr__(self):
		return "<{0},{1}>".format(self.first, self.second)

	def __eq__(self, other):
		return  (
					(self.first == other.first and self.second == other.second)
					or
					(self.first == other.second and self.second == other.first)
				)

class Triangle(object):
	def __init__(self, nodes, triangles):
		self.nodes = nodes
		self.triangles = triangles

		center_x = (self.nodes[0].x + self.nodes[1].x + self.nodes[2].x) / 3
		center_y = (self.nodes[0].y + self.nodes[1].y + self.nodes[2].y) / 3

		self.center = Node(center_x, center_y)


	def __str__(self):
		return str(self.nodes)

	def __repr__(self):
		return str(self.nodes)


	def get_opposite_node(self, edge):
		if edge not in self.get_edges():
			return None, -1
		for node_index, node in enumerate(self.nodes):
			if node != edge.first and node != edge.second:
				return node, node_index

	def get_opposite_triangle(self, node):
		node_index = self.nodes.index(node)
		return self.triangles[node_index], node_index

	def get_edges(self):
		edges = [
			Edge(self.nodes[0], self.nodes[1]),
			Edge(self.nodes[1], self.nodes[2]),
			Edge(self.nodes[0], self.nodes[2])
		]

		return edges


class Triangulation(object):

	def __str__(self):
		return "--\n{0}\n--".format("\n".join([str(triangle) for triangle in self.triangles]))

	def __repr__(self):
		return "--\n{0}\n--".format("\n".join([str(triangle) for triangle in self.triangles]))

	def __init__(self, triangles = []):
		self.triangles = triangles

	def find_nearest_triangle(self, new_node):
		# Функция поиска ближайшего к данному узлу треугольника


		def signed_area(a, b, c):
			return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

		def is_split_by_edge(a, b, edge):
			# Проверка находятся ли узлы a и b
			# По разную сторону от ребра edge

			# Возможно сортировать не нужно
			sorted_nodes = [edge.first, edge.second]
			sorted_nodes.sort(key=lambda node: [node.x, node.y])
			sorted_edge = Edge(sorted_nodes[0], sorted_nodes[1])

			return (signed_area(sorted_edge.first, sorted_edge.second, a)
			* signed_area(sorted_edge.first, sorted_edge.second, b) <= 0)



		def find_nearest_recur(triangle):

			for edge in triangle.get_edges():
				# Смотрим разделены ли данным ребром
				# центральная точка треугольника и новый узел
				if is_split_by_edge(triangle.center, new_node, edge):

					# Если разделены, то
					# берем противоположную вершину к данному ребру
					# и находим по ней противоположный треугольник
					opposite_node, opposite_node_index = triangle.get_opposite_node(edge)
					opposite_triangle = triangle.triangles[opposite_node_index]

					# Если он существует
					if opposite_triangle is not None:
						# Переходим в него и продолжаем поиск
						return find_nearest_recur(opposite_triangle)
					else:
						# Иначе возвращаем текущий треугольник, так как
						# вэтом случае он будет самым ближним к данному узлу
						return triangle
			
			# Если дошли сюда, то
			# центральная точка треугольника и новый узел
			# лежат в одном треугольнике,
			# и мы его возвращаем
			return triangle

		# Начинаем поиск с первого треугольника триангуляции
		return find_nearest_recur(self.triangles[0])
