from triangulation.types import *
import triangulation.routines as tr
from plot import routines as pr


def main():
    center_x = 5
    center_y = 5

    nodes = [
        Node(0, 0),
        Node(1, 1),
        Node(-1, 1),
        Node(1, 0),
        Node(-1, 0),
        Node(0, 2)
    ]

    nodes = [Node(node.x + center_x, node.y + center_y) for node in nodes]

    triangles = [
        Triangle([nodes[0], nodes[1], nodes[2]], [None, None, None], 0),
        Triangle([nodes[0], nodes[1], nodes[3]], [None, None, None], 3),
        Triangle([nodes[0], nodes[2], nodes[4]], [None, None, None], 2),
        Triangle([nodes[1], nodes[2], nodes[5]], [None, None, None], 1),
    ]

    main_triangle = triangles[0]

    main_triangle.triangles = [triangles[3], triangles[2], triangles[1]]
    triangles[0].triangles = [None,main_triangle, None]
    triangles[1].triangles = [None, main_triangle, None]
    triangles[2].triangles = [None, main_triangle, None]


    for triangle in triangles:
        pr.plot_triangle(triangle)
    pr.show()

    #nearest_triangle = tr.find_nearest_triangle(triangles[0], Node(2, 2))
    #print(nearest_triangle.number)
    nearest_triangle = tr.find_nearest_triangle(triangles[1], Node(2, 2))
    print(nearest_triangle.number)
    #nearest_triangle = tr.find_nearest_triangle(triangles[2], Node(2, 2))
    #print(nearest_triangle.number)
    #nearest_triangle = tr.find_nearest_triangle(triangles[3], Node(2, 2))
    #print(nearest_triangle.number)


if __name__ == "__main__":
    main()