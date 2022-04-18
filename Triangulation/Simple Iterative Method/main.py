import plot as my_plt
import random
from triangulation import Triangle
from triangulation import Node
from triangulation import find_nearest_triangle


def test_find_nearest_triangle(test_node):
    triangle = Triangle(
        [Node(4, 5), Node(5, 3), Node(3, 3)],
        [
            Triangle([Node(3, 3), Node(5, 3), Node(4, 1)], [None, None, []], number=2),
            Triangle([Node(3, 5), Node(4, 5), Node(3, 3)], [[], None, None], number=3),
            Triangle([Node(4, 5), Node(5, 5), Node(5, 3)], [None, [], None], number=4),

        ],
        number=1)

    triangle.triangles[0].triangles[2] = triangle
    triangle.triangles[1].triangles[0] = triangle
    triangle.triangles[2].triangles[1] = triangle

    my_plt.plot_triangles_recursive(triangle)

    found_triangle = find_nearest_triangle(triangle, test_node)
    my_plt.plot_triangle(found_triangle, color="red")

    my_plt.plot_node(test_node)
    my_plt.show()


def main():
    test_nodes = [Node(random.uniform(3, 6), random.uniform(3, 6)) for i in range(20)]
    for test_node in test_nodes:
        test_find_nearest_triangle(test_node)


if __name__ == "__main__":
    main()