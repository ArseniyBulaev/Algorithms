from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot



def flip_test():
    plot_nodes = True

    triangle1 = Triangle([Node(0, 0), Node(10, 0), Node(5, 10)], [None, None, None])
    triangle2 = Triangle([Node(10, 0), Node(5, 10), Node(10, 10)], [None, None, None])
    triangle3 = Triangle([Node(5, 10), Node(10, 10), Node(7, 15)], [None, None, None])
    triangle4 = Triangle([Node(10, 10), Node(10, 0), Node(12, 5)], [None, None, None])
    triangle5 = Triangle([Node(0, 0), Node(10, 0), Node(5, -5)], [None, None, None])
    triangle6 = Triangle([Node(0, 0), Node(5, 10), Node(-5, 5)], [None, None, None])

    triangulation = Triangulation(triangles=[
        triangle1,
        triangle2,
        triangle3,
        triangle4,
        triangle5,
        triangle6,
    ])

    triang_m.connect_along_edge(triangle1, triangle2, Edge(Node(10, 0), Node(5, 10)))
    triang_m.connect_along_edge(triangle1, triangle5, Edge(Node(0, 0), Node(10, 0)))
    triang_m.connect_along_edge(triangle1, triangle6, Edge(Node(0, 0), Node(5, 10)))
    triang_m.connect_along_edge(triangle2, triangle3, Edge(Node(5, 10), Node(10, 10)))
    triang_m.connect_along_edge(triangle2, triangle4, Edge(Node(10, 10), Node(10, 0)))


    test_triangle1 = triangle2
    test_triangle2 = triangle3
    flip_edge = Edge(Node(5, 10), Node(10, 10))


    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(test_triangle1, triangulation)
    my_plot.show()

    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(test_triangle2, triangulation)
    my_plot.show()

    triang_m.flip(test_triangle1, flip_edge)



    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(test_triangle1, triangulation)
    my_plot.show()

    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(test_triangle2, triangulation)
    my_plot.show()

    print("SOSEDI 1")

    for triangle in test_triangle1.triangles:
        my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
        if triangle is not None:
            my_plot.plot_triangle_with_neighbors(triangle)
        my_plot.show()

    print("SOSEDI 2")

    for triangle in test_triangle2.triangles:
         my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
         if triangle is not None:
             my_plot.plot_triangle_with_neighbors(triangle)
         my_plot.show()


if __name__ == "__main__":
    flip_test()