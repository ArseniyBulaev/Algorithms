import graphviz
from graph_objects import Graph


def graph_object_to_graphviz_object(graph, graph_name="graph"):

    graph_graphviz = graphviz.Graph(graph_name, strict=True)


    for node in graph.nodes:
        graph_graphviz.node(node.label)
        for adjacent_node in node.weighted_adjacent_nodes.keys():
            graph_graphviz.edge(node.label,
                                adjacent_node.label,
                                label=str(node.weighted_adjacent_nodes[adjacent_node]))

    return graph_graphviz

def render_graph(graph, view=False):
    graph.render(directory='doctest-output', view=view).replace('\\', '/')

