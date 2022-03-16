import matplotlib.pyplot as plt
import helper.types as htypes
import numpy as np

def plot_segments(segments):
	for segment in segments:
		plt.plot([segment.start_point.x, segment.end_point.x], [segment.start_point.y, segment.end_point.y], 'r-')
	plt.show()

def generate_nodes(n):
	np_nodes = np.random.random(size=(n, 2))
	nodes = []

	for np_node in np_nodes:
		nodes.append(htypes.Node(np_node[0], np_node[1]))

	return nodes

def generate_segments(nodes):
	nodes_to_generate = nodes.copy()
	segments = []

	while len(nodes_to_generate) > 1:
		start_node = nodes_to_generate.pop(0)
		for node in nodes_to_generate:
			segments.append(htypes.Segment(start_node, node))

	return segments
