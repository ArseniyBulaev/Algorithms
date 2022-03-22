from triangulation.types import *
from plot import routines as pr


def main():



    nodes = [
        Node(0, 0),
        Node(1, 1),
        Node(-1, 1),
        Node(1, 0),
        Node(-1, 0),
        Node(0, 2)
    ]

    triangles = [
        Triangle([nodes[0], nodes[1], nodes[2]], None, 0),
        Triangle([nodes[0], nodes[1], nodes[3]], None, 1),
        Triangle([nodes[0], nodes[2], nodes[4]], None, 2),
        Triangle([nodes[1], nodes[2], nodes[5]], None, 3),
    ]

    for triangle in triangles:
        pr.plot_triangle(triangle)
    pr.show()




if __name__ == "__main__":
    main()