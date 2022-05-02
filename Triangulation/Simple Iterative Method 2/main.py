from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt



def main():
	nodes = [Node(5, 10), Node(0, 10), Node(0, 0), Node(2, 6), Node(2, 6)]
	triangulation = triang_m.simple_iterative_method(nodes)
	my_plot.plot_triangulation(triangulation, plot_nodes=True)
	my_plot.show()
	for triangle in triangulation.triangles:
		print(triang_m.delaunay_check(triangle)[1])



if __name__ == "__main__":
	main()
