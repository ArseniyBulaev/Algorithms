import matplotlib.pyplot as plt
from objects import Triangle, Edge, Node


def plot_triangle(triangle, color="green"):
    
    edges = triangle.get_edges()

    for edge in edges:
        plt.plot([edge.first.x, edge.second.x], [edge.first.y, edge.second.y], color=color)

    triangle_center = triangle.get_center() 

    if triangle.number is not None:
        plt.text(triangle_center.x, triangle_center.y, triangle.number)

def plot_triangulation(triangulation):
	for triangle in triangulation.triangles:
		plot_triangle(triangle)

def plot_node(node, color="blue"):
    plt.plot([node.x], [node.y], "o", color=color)



def show():
	plt.show()