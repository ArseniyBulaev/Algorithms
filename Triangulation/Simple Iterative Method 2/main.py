from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot

from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt


def main():
	nodes = [Node(5, 10), Node(0, 10), Node(0, 0), Node(2, 8), Node(1, 6)]
	triang_m.simple_iterative_method(nodes)


if __name__ == "__main__":
	main()
