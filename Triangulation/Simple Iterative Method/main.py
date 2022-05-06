from objects import Node
import triangulation as triang_m
import plot as my_plot
import random
import time


def main():
	plot_nodes = False
	nodes_count = 1000
	a, b = 0, 10000
	# nodes = [
	# 	Node(5, 10),
	# 	Node(0, 10),
	# 	Node(0, 0),
	# 	Node(2, 6),
	# 	Node(1, 6),
	# 	Node(1, 4),
	# 	Node(2, 8),
	# 	Node(1.5, 6.5),
	# 	Node(3, 6.5),
	# 	Node(3, 7),
	# 	Node(0.5, 6),
	# 	Node(0.4, 6),
	# 	Node(0, 5),
	# 	Node(5, 0),
	# 	Node(5, 0),
	# 	Node(2, 2),
	# 	Node(5, 0),
	# 	Node(5, 0),
	# 	Node(5, 0),
	# 	Node(5, 4),
	# 	Node(5, 6)
	# ]

	nodes = [Node(random.randint(a, b), random.randint(a, b)) for i in range(nodes_count)]

	start = time.perf_counter()
	triangulation = triang_m.simple_iterative_method(nodes)
	end = time.perf_counter()

	print("Calculation time: ", end - start)

	my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
	my_plot.show()

	# for triangle in triangulation.triangles:
	# 	print(triang_m.delaunay_check(triangle))


if __name__ == "__main__":
	main()
