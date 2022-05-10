from graph_objects import Node, Graph
import algorithm as alg
import graphviz_support as gviz_s

def main():
    nodes = [
        Node("1"),
        Node("2"),
        Node("3"),
        Node("4"),
        Node("5"),
        Node("6"),
        Node("7"),
        Node("8"),
        ]
    
    graph = Graph(nodes)

    graph.connect_nodes(nodes[0], nodes[1], 2)
    graph.connect_nodes(nodes[0], nodes[4], 3)

    graph.connect_nodes(nodes[1], nodes[2], 3)
    graph.connect_nodes(nodes[1], nodes[5], 2)
    graph.connect_nodes(nodes[1], nodes[4], 2)

    graph.connect_nodes(nodes[2], nodes[6], 2)
    graph.connect_nodes(nodes[2], nodes[3], 4)

    graph.connect_nodes(nodes[3], nodes[6], 2)
    graph.connect_nodes(nodes[3], nodes[7], 2)

    graph.connect_nodes(nodes[4], nodes[5], 3)

    graph.connect_nodes(nodes[5], nodes[6], 1)

    graph.connect_nodes(nodes[6], nodes[7], 3)

    gviz_graph = gviz_s.graph_object_to_graphviz_object(graph, graph_name="0")
    gviz_s.render_graph(gviz_graph)
    
    #print(graph.merge_nodes(nodes[4], nodes[0]))
    print(alg.minimum_cut(graph))
    #print(graph.nodes)
    #print(graph.nodes)

    


if __name__ == "__main__":
    main()