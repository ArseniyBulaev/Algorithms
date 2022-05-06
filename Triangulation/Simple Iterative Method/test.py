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


def inside_case_test():
    plot_nodes = True

    nodes = [Node(-2, 5), Node(2, 5), Node(6, 5), Node(0, 0), Node(5, 0), Node(2, -5)]
    edges = [Edge(Node(0, 0), Node(2, 5)), Edge(Node(2, 5), Node(5, 0)), Edge(Node(0, 0), Node(5, 0))]
    triangles = [
        Triangle([nodes[0], nodes[1], nodes[3]], [None, None, None]),
        Triangle([nodes[1], nodes[3], nodes[4]], [None, None, None]),
        Triangle([nodes[1], nodes[2], nodes[4]], [None, None, None]),
        Triangle([nodes[3], nodes[4], nodes[5]], [None, None, None]),
    ]

    triang_m.connect_along_edge(triangles[0], triangles[1], edges[0])
    triang_m.connect_along_edge(triangles[1], triangles[2], edges[1])
    triang_m.connect_along_edge(triangles[1], triangles[3], edges[2])

    triangulation = Triangulation(triangles=triangles)

    test_nodes = [Node(1, 2)]

    triang_m.simple_iterative_method(test_nodes, triangulation=triangulation)
    for triangle in triangulation.triangles:
        my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
        my_plot.plot_triangle_with_neighbors(triangle)
        my_plot.show()

    print(len(triangulation.triangles))



if __name__ == "__main__":
    inside_case_test()
    #flip_test()