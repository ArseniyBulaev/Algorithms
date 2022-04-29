from objects import Node, Edge, Triangle, Triangulation
from enum import Enum
import plot as my_plot
import copy
from scipy.spatial import ConvexHull, convex_hull_plot_2d


def connect_along_edge(tr1, tr2, edge):
	# Соединяет треугольники по ребру
	tr_1_opp_node, tr_1_opp_node_index = tr1.get_opposite_node(edge)
	tr_2_opp_node, tr_2_opp_node_index = tr2.get_opposite_node(edge)

	# Вроде как не обязательное условие.
	# Не будет выполнено если edge не принадлежит tr1 или tr2
	if tr_1_opp_node is not None and tr_2_opp_node is not None:
		tr1.triangles[tr_1_opp_node_index] = tr2
		tr2.triangles[tr_2_opp_node_index] = tr1

		return True
	else:
		return False


def get_joint_edge_pair(triangles, edge):
	# Возвращает смежную по данному ребру пару треугольников
	# (Данные треугольники пока не связаны друг с другом)
	joint_pair = []

	for triangle in triangles:
		opp_node, opp_node_index = triangle.get_opposite_node(edge)
		if opp_node is not None:
			joint_pair.append(triangle)

		if len(joint_pair) == 2:
			return joint_pair

	return None


def create_triangle_base_on(base_triangle, base_edge, new_node):
	# Создаёт новый треугольник внутри base_triangle c
	# основанием base_edge и дополнитеоьной вершиной new_node
	
	# Получаем вершину противоположную ребру base_edge в base_triangle
	opp_node, opp_node_index = base_triangle.get_opposite_node(base_edge)

	# Получаем треугольник, лежащий напротив вершины opp_node
	opp_triangle = base_triangle.triangles[opp_node_index]
	
	# Создаём новый треугольник на основе старого 
	new_triangle = copy.deepcopy(base_triangle)

	# Меняем противоположную к ребру base_edge вершину на new_node
	new_triangle.nodes[opp_node_index] = new_node

	# Если opp_triangle существует
	if opp_triangle is not None:

		# Получаем вершину противоположную ребру base_edge в opp_triangle
		opp_node, opp_node_index = opp_triangle.get_opposite_node(base_edge)

		# Связываем opp_triangle с base_triangle
		opp_triangle.triangles[opp_node_index] = new_triangle

	return new_triangle


def check_on_point_case(triangle, new_node, info):
	for node in triangle.nodes:
		if node == new_node:
			info["position"] = 0
			return True

	return False


def check_on_edge_case(triangle, new_node, info):
	def signed_area(a, b, c):
		return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

	for edge in triangle.get_edges():
		if signed_area(edge.first, edge.second, new_node) == 0:
			info["position"] = 2
			info["occupied edge"] = edge
			return True

	return False


def check_inside_case(triangle, new_node, info):
	def signed_area(a, b, c):
		return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

	def counter_clockwise(a, b, c):
		return signed_area(a, b, c) > 0

	sorted_nodes = triangle.nodes.copy()
	sorted_nodes.sort(key=lambda n: [n.x, n.y])
	is_left_triple = counter_clockwise(sorted_nodes[0], sorted_nodes[1], sorted_nodes[2])

	if is_left_triple:
		sorted_nodes.sort(key=lambda n: [n.x, -n.y])
	sorted_triangle = Triangle(sorted_nodes, [None, None, None])

	for edge in sorted_triangle.get_edges():
		if not counter_clockwise(edge.first, new_node, edge.second):
			return False

	info["position"] = 3
	return True


def check_node_position_relative_triangle(triangle, new_node):
	info = dict()
	info["position"] = -1  # Позиция узла ещё не известна

	# Случай 1 (new_node совпадает с уже существующим узлом)
	if check_on_point_case(triangle, new_node, info):
		return info

	# Случай 2 (new_node лежит на ребре треугольника)
	if check_on_edge_case(triangle, new_node, info):
		return info

	# Случай 3 (new_node лежит внутри треугольника)
	if check_inside_case(triangle, new_node, info):
		return info

	# Случай 4 (new_node лежит снаружи треугольника)
	info["position"] = 4

	return info


def outside_case(triangulation, nodes, new_node):

	new_triangles = []

	nodes.insert(0, new_node)
	generators = [[node.x, node.y] for node in nodes]
	hull = ConvexHull(points=generators, qhull_options='QG0')

	for visible_facet in hull.simplices[hull.good]:
		scipy_edge = hull.points[visible_facet]
		visible_node_1 = Node(int(scipy_edge[0][0]), int(scipy_edge[0][1]))
		visible_node_2 = Node(int(scipy_edge[1][0]), int(scipy_edge[1][1]))
		visible_edge = Edge(visible_node_1, visible_node_2)

		joint_triangle = triangulation.find_triangle_by_edge(visible_edge)
		new_triangle = Triangle([visible_node_1, visible_node_2, new_node], [None, None, None])

		# Выполняем их связывание по ребру visible_edge
		connect_along_edge(joint_triangle, new_triangle, visible_edge)

		if len(new_triangles) > 0:
			adjacent_triangle = new_triangles[-1]
			for possible_adjacent_edge in new_triangle.get_edges():
				if possible_adjacent_edge != visible_edge:
					if get_joint_edge_pair([adjacent_triangle, new_triangle], possible_adjacent_edge) is not None:
						connect_along_edge(adjacent_triangle, new_triangle, possible_adjacent_edge)

		new_triangles.append(new_triangle)

	return new_triangles


def on_edge_case(base_triangle, new_node, occupied_edge, triangulation):

	def split_triangle(triangle):

		local_new_triangles = []

		# Создаём новые треугольники проходом по всем рёбрам кроме того, на котором находится точка
		for edge in triangle.get_edges():
			if edge == occupied_edge:
				continue
			new_triangle = create_triangle_base_on(triangle, edge, new_node)
			local_new_triangles.append(new_triangle)

		node_1, node_2, node_3 = triangle.nodes

		# Получаем совместное ребро
		opp_node_l, opp_node_index_l = triangle.get_opposite_node(occupied_edge)
		joint_edge = Edge(opp_node_l, new_node)

		# Ищем смежные по данному ребру треугольники
		local_joint_triangles = get_joint_edge_pair(local_new_triangles, joint_edge)

		tr1_l, tr2_l = local_joint_triangles

		# Выполняем их связывание по ребру edge
		connect_along_edge(tr1_l, tr2_l, joint_edge)

		return local_new_triangles

	opp_node, opp_node_index = base_triangle.get_opposite_node(occupied_edge)
	adjacent_triangle = base_triangle.triangles[opp_node_index]

	new_triangles = split_triangle(base_triangle)
	new_triangles += split_triangle(adjacent_triangle)

	first_part_of_occupied_edge = Edge(occupied_edge.first, new_node)
	second_part_of_occupied_edge = Edge(new_node, occupied_edge.second)

	triangles_to_join = new_triangles.copy()

	for edge in [first_part_of_occupied_edge, second_part_of_occupied_edge]:
		# Ищем смежные по данному ребру треугольники
		joint_triangles = get_joint_edge_pair(triangles_to_join, edge)

		tr1, tr2 = joint_triangles

		# Выполняем их связывание по ребру edge
		connect_along_edge(tr1, tr2, edge)

		triangles_to_join.remove(tr1)
		triangles_to_join.remove(tr2)

	#for local_triangle in new_triangles:
		# my_plot.plot_triangulation(triangulation)
		# my_plot.plot_triangle_with_neighbors(local_triangle, triangulation)
		# my_plot.show()

	return new_triangles


def inside_case(old_triangle, new_node):
	new_triangles = []

	# Создаём новые треугольники, проходя по всем рёбрам
	for edge in old_triangle.get_edges():
		new_triangle = create_triangle_base_on(old_triangle, edge, new_node)
		new_triangles.append(new_triangle)

	node_1, node_2, node_3 = old_triangle.nodes

	# Связываем вновь созданные треугольники
	for edge in [Edge(node_1, new_node), Edge(node_2, new_node), Edge(node_3, new_node)]:

		# Ищем смежные по данному ребру треугольники
		joint_triangles = get_joint_edge_pair(new_triangles, edge)
		tr1, tr2 = joint_triangles

		# Выполняем их связывание по ребру edge
		connect_along_edge(tr1, tr2, edge)

	return new_triangles


def delaunay_check(triangle):
	return 2, True


def flip(triangle, node):
	pass


def simple_iterative_method(nodes, triangulation=None):

	class NodePos(Enum):
		ON_POINT = 1
		ON_EDGE = 2
		INSIDE_TRIANGLE = 3
		OUTSIDE_TRIANGLE = 4

	if triangulation is None:
		triangulation = Triangulation()

	triangulation.add_triangle(Triangle(nodes[:3], [None, None, None]))

	# my_plot.plot_triangulation(triangulation)
	# my_plot.show()

	for i in range(3, len(nodes)):
		node = nodes[i]

		my_plot.plot_node(node)
		my_plot.plot_triangulation(triangulation)
		my_plot.show()

		nearest_triangle = triangulation.find_nearest_triangle(node)
		info = check_node_position_relative_triangle(nearest_triangle, node)

		if NodePos(info["position"]) == NodePos.OUTSIDE_TRIANGLE:
			new_triangles = outside_case(triangulation, nodes[:i], node)

		elif NodePos(info["position"]) == NodePos.ON_POINT:
			continue

		elif NodePos(info["position"]) == NodePos.ON_EDGE:
			new_triangles = on_edge_case(nearest_triangle, node, info["occupied edge"], triangulation)
			opp_node, opp_node_index = nearest_triangle.get_opposite_node(info["occupied edge"])
			adjacent_triangle = nearest_triangle.triangles[opp_node_index]

			triangulation.remove_triangle(nearest_triangle)
			triangulation.remove_triangle(adjacent_triangle)

		elif NodePos(info["position"]) == NodePos.INSIDE_TRIANGLE:
			new_triangles = inside_case(nearest_triangle, node)
			triangulation.remove_triangle(nearest_triangle)

		for new_triangle in new_triangles:
			triangulation.add_triangle(new_triangle)
			node, is_node_correct = delaunay_check(new_triangle)

			if not is_node_correct:
				flip(new_triangle, node)

		my_plot.plot_triangulation(triangulation)
		my_plot.show()

	return triangulation
