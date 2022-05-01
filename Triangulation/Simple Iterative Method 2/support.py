from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot

triangulation = None


def flip(target, flipping_edge):
    # target - треугольник, который инициирует переворот ребра
    # flipping_edge - ребро, которое нужно перевернуть

    # Получаем соседа с котором нужно осуществить переворот
    opp_node_in_target, neighbor_index = target.get_opposite_node(flipping_edge)
    neighbor = target.triangles[neighbor_index]
    opp_node_in_neighbor, target_index = neighbor.get_opposite_node(flipping_edge)

    # Получаем индексы узлов
    # flip_target_node_index - индекс узла для флипа в target
    # relink_target_node_index - индекс узла, по которому можно получить треугольник, переподвязываемый на neighbor
    flip_target_node_index = target.nodes.index(flipping_edge.first)
    relink_target_node_index = target.nodes.index(flipping_edge.second)

    # Получаем индексы узлов
    # flip_neighbor_node_index - индекс узла для флипа в neighbor
    # relink_neighbor_node_index - индекс узла, по которому можно получить треугольник, переподвязываемый на target
    flip_neighbor_node_index = neighbor.nodes.index(flipping_edge.second)
    relink_neighbor_node_index = neighbor.nodes.index(flipping_edge.first)

    # Получаем треугольник который нужно связать с neighbor
    relink_target_node = target.nodes[relink_target_node_index]
    relink_target_edge = target.get_opposite_edge(relink_target_node)
    relink_target_triangle = target.get_opposite_triangle(relink_target_node, return_index=False)

    # Получаем треугольник который нужно связать с target
    relink_neighbor_node = neighbor.nodes[relink_neighbor_node_index]
    relink_neighbor_edge = neighbor.get_opposite_edge(relink_neighbor_node)
    relink_neighbor_triangle = neighbor.get_opposite_triangle(relink_neighbor_node, return_index=False)

    # Осуществляем переворот ребра
    target.nodes[flip_target_node_index] = opp_node_in_neighbor
    neighbor.nodes[flip_neighbor_node_index] = opp_node_in_target
    # Связываем треугольники по правильному ребру
    triang_m.connect_along_edge(target, neighbor, Edge(opp_node_in_target, opp_node_in_neighbor))
    # Переподвязываем старый треугольник в target
    triang_m.connect_along_edge(target, relink_neighbor_triangle, relink_neighbor_edge)
    # Переподвязываем старый треугольник в neighbor
    triang_m.connect_along_edge(neighbor, relink_target_triangle, relink_target_edge)



if __name__ == "__main__":

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


    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(triangle1, triangulation)
    my_plot.show()

    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(triangle2, triangulation)
    my_plot.show()

    flip(triangle1, Edge(Node(10, 0), Node(5, 10)))

    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(triangle1, triangulation)
    my_plot.show()

    my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
    my_plot.plot_triangle_with_neighbors(triangle2, triangulation)
    my_plot.show()

    for triangle in triangle1.triangles:
        my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
        my_plot.plot_triangle_with_neighbors(triangle)
        my_plot.show()


    for triangle in triangle2.triangles:
        my_plot.plot_triangulation(triangulation, plot_nodes=plot_nodes)
        my_plot.plot_triangle_with_neighbors(triangle)
        my_plot.show()





"""
generators = [[node.x, node.y] for node in nodes]
	hull = ConvexHull(points=generators, qhull_options='QG0')

	print(hull.simplices)
	print(hull.good)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	print()
	for visible_facet in hull.simplices[hull.good]:

		print(hull.points[visible_facet])
		ax.plot(hull.points[visible_facet, 0],
				hull.points[visible_facet, 1],
				color='violet',
				lw=6)

	convex_hull_plot_2d(hull, ax=ax)
	plt.show()
"""