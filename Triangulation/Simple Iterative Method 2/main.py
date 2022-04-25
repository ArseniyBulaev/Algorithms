from objects import Node, Edge, Triangle, Triangulation



def main():
	nodes1 = [Node(0,0), Node(10,10), Node(0,10)]
	nodes2 = [Node(0,0), Node(10,0), Node(10,10)]
	edge = Edge(Node(0,0), Node(10,10))

	triangle1 = Triangle(nodes1, [None, None, None])
	triangle2 = Triangle(nodes2, [None, None, None])

	

	

	n_1, n_i_1 = triangle1.get_opposite_node(edge)
	n_2, n_i_2 = triangle2.get_opposite_node(edge)


	triangle2.triangles[n_i_2] = triangle1
	triangle1.triangles[n_i_1] = triangle2

	print(triangle1.triangles)
	print(triangle2.triangles)




	triangulation = Triangulation([triangle1, triangle2])



	nearest_1 = triangulation.find_nearest_triangle(Node(2, 5))
	nearest_2 = triangulation.find_nearest_triangle(Node(5, 2))

	print(nearest_1)
	print(nearest_2)
	




	


if __name__ == "__main__":
	main()