from objects import Node, Edge, Triangle, Triangulation
import copy


def get_joint_edge_pair(triangles, edge):
	# Возвращает смежную по данному ребру пару треугольников
	joint_pair = []

	for triangle in triangles:
		opp_node, opp_node_index = triangle.get_opposite_node(edge)
		if opp_node is not None:
			joint_pair.append(triangle)

	return joint_pair

def add_inner_node(triangle, new_node):
	new_triangles = []

	# Создаём новые треугольники, проходя по всем рёбрам
	for edge in triangle.get_edges():

		# Для каждого ребра получаем противоположную вершину
		opp_node, opp_node_index = triangle.get_opposite_node(edge)
		
		# Создаём новый треугольник из исходного
		new_triangle = copy.deepcopy(triangle)
		new_triangle.triangles = [None, None, None]
		# Меняем в новом треугольнике противолежащую вершину для данного ребра
		# на новую вершину
		new_triangle.nodes[opp_node_index] = new_node

		# Если для старого треугольника 
		# существует смежный по данному ребру треугольник, то
		# связываем его с новым

		opp_triangle = triangle.triangles[opp_node_index]

		if opp_triangle is not None:
			# Связь новый -> старый
			new_triangle.triangles[opp_node_index] = opp_triangle
			opp_node, opp_node_index = opp_triangle.get_opposite_node(edge)
			# Связь старый -> новый
			opp_triangle.triangles[opp_node_index] = new_triangle


		new_triangles.append(new_triangle)

	node_1, node_2, node_3 = triangle.nodes

	# Связываем вновь созданные треугольники
	for edge in [Edge(node_1, new_node), Edge(node_2, new_node), Edge(node_3, new_node)]:

		# Ищем смежные по данному ребру треугольники
		joint_triangles = get_joint_edge_pair(new_triangles, edge)

		# Если таких два, то связываем их
		# (Так-то if не нужен, но пусть будет)
		if  len(joint_triangles) == 2:
			triangle1, triangle2 = joint_triangles

			n_1, n_i_1 = triangle1.get_opposite_node(edge)
			n_2, n_i_2 = triangle2.get_opposite_node(edge)

			triangle2.triangles[n_i_2] = triangle1
			triangle1.triangles[n_i_1] = triangle2


	return new_triangles