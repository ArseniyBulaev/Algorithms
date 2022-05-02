from objects import Node, Edge, Triangle, Triangulation
import triangulation as triang_m
import plot as my_plot

triangulation = None






if __name__ == "__main__":
    pass






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