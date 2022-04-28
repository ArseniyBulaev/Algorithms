from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot

def main():
	nodes = [Node(0,0), Node(5,10), Node(0,10)]
	new_node = Node(2, 8)
	base_triangle = Triangle(nodes, [None, None, None])
	edges = base_triangle.get_edges()
	triangulation = Triangulation()
	triangulation.add_triangle(base_triangle)

	my_plot.plot_triangulation(triangulation)
	my_plot.show()

	new_triangles = triang_m.inside_case(base_triangle, new_node)

	triangulation.remove_triangle(base_triangle)


	for new_triangle in new_triangles:
		triangulation.add_triangle(new_triangle)


	my_plot.plot_triangulation(triangulation)

	test_nodes = [Node(1, 6), Node(2, 5), Node(3, 9)]

	for node in test_nodes:
		my_plot.plot_node(node)
		nearest_triangle = triangulation.find_nearest_triangle(node)
		my_plot.plot_triangulation(triangulation)
		my_plot.plot_triangle(nearest_triangle, color="red")
		my_plot.show()


	

if __name__ == "__main__":
	main()