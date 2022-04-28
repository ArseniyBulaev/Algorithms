from objects import Node, Edge, Triangle, Triangulation
from enum import Enum
import copy




def add_inner_node(triangle, new_node):
	# OLD 
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

	#Если opp_triangle существует
	if opp_triangle is not None:

		# Получаем вершину противоположную ребру base_edge в opp_triangle
		opp_node, opp_node_index = opp_triangle.get_opposite_node(base_edge)

		# Связываем opp_triangle с base_triangle
		opp_triangle[opp_node_index] = new_triangle

	return new_triangle

def check_node_possition_relative_triangle(triangle, node):
	pass


def outside_case(triangulation, nearest_triangle, new_node):
	pass

def on_edge_case(triangle, new_node, occupied_edge):
	pass

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

		# Выполняем из связывание по ребру edge
		connect_along_edge(tr1, tr2, edge)

	return new_triangles


def delonoy_check(triangle):
	pass

def flip(triangle, node):
	pass


def simple_iterative_method(nodes, triangulation=None):

	class NodePos(Enum):
		OUTSIDE_TRIANGLE = 0
		ON_POINT = 1
		ON_EDGE = 2
		INSIDE_TRIANGLE = 3


	if triangulation is None:
		triangulation = Triangulation()

	triangulation.add_triangle(Triangle(nodes[0], nodes[1], nodes[2]))

	for node in nodes[3:]:
		nearest_triangle = find_nearest_triangle(node)

		info = check_node_possition_relative_triangle(nearest_triangle, node)

		if NodePos(info["possition"]) == NodePos.OUTSIDE_TRIANGLE:
			new_triangles = outside_case(triangulation, nearest_triangle, node)
		elif NodePos(info["possition"]) == NodePos.ON_POINT:
			continue
		elif NodePos(info["possition"]) == NodePos.ON_EDGE:
			new_triangles = on_edge_case(triangle, node, info["occupied edge"])
		elif NodePos(info["possition"]) == NodePos.INSIDE_TRIANGLE:
			new_triangles = inside_case(triangle, node)

		for new_triangle in new_triangles:
			node, is_node_correct = delonoy_check(new_triangle)

			if not is_node_correct:
				flip(new_triangle, bad_node)

	return triangulation