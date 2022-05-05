from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt
import experiments as ex


def main():
	plot_nodes = False
	nodes = [
		Node(5, 10),
		Node(0, 10),
		Node(0, 0),
		Node(2, 6),
		Node(1, 6),
		Node(1, 4),
		Node(2, 8),
		Node(1.5, 6.5),
		Node(3, 6.5),
		Node(3, 7),
		Node(0.5, 6),
		Node(0.4, 6),
		Node(0, 5),
		Node(5, 0),
		Node(5, 0),
		Node(2, 2)
	]
	triangulation = triang_m.simple_iterative_method(nodes)

	my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
	my_plot.show()

	for triangle in triangulation.triangles:
		print(triang_m.delaunay_check(triangle))


if __name__ == "__main__":
	main()
