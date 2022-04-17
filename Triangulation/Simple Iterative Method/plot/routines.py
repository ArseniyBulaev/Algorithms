from triangulation.types import *
import matplotlib.pyplot as plt

min_x = 0
max_x = 10
max_y = 0
min_y = 10




def plot_triangle(triangle):


    nodes = triangle.nodes




    plt.plot([nodes[0].x, nodes[1].x], [nodes[0].y, nodes[1].y], "r-")
    plt.plot([nodes[1].x, nodes[2].x], [nodes[1].y, nodes[2].y], "r-")
    plt.plot([nodes[2].x, nodes[0].x], [nodes[2].y, nodes[0].y], "r-")


    triangle_center = triangle.center()
    triangle_center.x
    triangle_center.y

    plt.text(triangle_center.x, triangle_center.y, triangle.number)

    plt.xlim([min_x, max_x])
    plt.ylim([min_y, max_y])


def show():
    plt.show()
