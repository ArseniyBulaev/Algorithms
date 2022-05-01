import matplotlib.pyplot as plt
from objects import Triangle, Edge, Node


def plot_triangle(triangle, color="green", plot_number=True, plot_nodes=False, lw=1):

    edges = triangle.get_edges()
    for edge in edges:
        plt.plot([edge.first.x, edge.second.x], [edge.first.y, edge.second.y], color=color, lw=lw)

    if triangle.number is not None and plot_number:
        triangle_center = triangle.get_center()
        plt.text(triangle_center.x, triangle_center.y, triangle.number)

    if plot_nodes:
        for node in triangle.nodes:
            plot_node(node, plot_text=True)


def plot_triangle_with_neighbors(triangle, plot_nodes=False):


    for sub_triangle in triangle.triangles:
        if sub_triangle is not None:
            plot_triangle(sub_triangle, color="orange", plot_number=False, plot_nodes=plot_nodes, lw=2)

    plot_triangle(triangle, color="red", plot_number=False, plot_nodes=plot_nodes)


def plot_triangulation(triangulation, plot_nodes=False):
    for triangle in triangulation.triangles:
        plot_triangle(triangle, plot_nodes=plot_nodes)


def plot_node(node, color="blue", plot_text=False):
    plt.plot([node.x], [node.y], "o", color=color)
    if plot_text:
        plt.text(node.x, node.y, str(node))


def show():
    plt.show()
