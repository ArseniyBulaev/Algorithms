import matplotlib.pyplot as plt
from triangulation import Triangle
from triangulation import Node


def plot_triangle(triangle, color="green"):
    age1 = (triangle.nodes[0], triangle.nodes[1])
    age2 = (triangle.nodes[1], triangle.nodes[2])
    age3 = (triangle.nodes[2], triangle.nodes[0])

    ages = [age1, age2, age3]

    for age in ages:
        plt.plot([age[0].x, age[1].x], [age[0].y, age[1].y], color=color)

    triangle_center = triangle.center()

    if triangle.number is not None:
        plt.text(triangle_center.x, triangle_center.y, triangle.number)


def plot_triangles_recursive(triangle, came_from=None):
    if triangle is None:
        return

    plot_triangle(triangle)

    for sub_triangle in triangle.triangles:
        if sub_triangle is not came_from:
            plot_triangles_recursive(sub_triangle, came_from=triangle)


def plot_node(node, color="blue"):
    plt.plot([node.x], [node.y], "o", color=color)



def show():
    plt.show()