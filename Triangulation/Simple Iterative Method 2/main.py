from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt



def main():
	nodes = [Node(5, 10), Node(0, 10), Node(0, 0), Node(10, 5)]
	triangulation = triang_m.simple_iterative_method(nodes)
	triangle = triangulation.triangles[-2]
	my_plot.plot_triangulation(triangulation, plot_nodes=True)
	#my_plot.plot_triangle_with_neighbors(triangle)
	my_plot.show()
	triang_m.flip(triangle, Edge(Node(5, 10), Node(0, 0)))
	my_plot.plot_triangulation(triangulation)
	#my_plot.plot_triangle_with_neighbors(triangle)
	my_plot.show()


if __name__ == "__main__":
	main()
