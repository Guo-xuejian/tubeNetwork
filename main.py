import networkx as nx
from networkx import simple_cycles, recursive_simple_cycles


def find_all_cycles(G, source=None, cycle_length_limit=None):
    """forked from networkx dfs_edges function. Assumes nodes are integers, or at least
    types which work with min() and > ."""
    if source is None:
        # produce edges for all components
        nodes = [i[0] for i in nx.connected_components(G)]
    else:
        # produce edges for components with source
        nodes = [source]
    # extra variables for cycle detection:
    cycle_stack = []
    output_cycles = set()

    def get_hashable_cycle(cycle):
        """cycle as a tuple in a deterministic order."""
        m = min(cycle)
        mi = cycle.index(m)
        mi_plus_1 = mi + 1 if mi < len(cycle) - 1 else 0
        if cycle[mi - 1] > cycle[mi_plus_1]:
            result = cycle[mi:] + cycle[:mi]
        else:
            result = list(reversed(cycle[:mi_plus_1])) + list(reversed(cycle[mi_plus_1:]))
        return tuple(result)

    for start in nodes:
        if start in cycle_stack:
            continue
        cycle_stack.append(start)

        stack = [(start, iter(G[start]))]
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)

                if child not in cycle_stack:
                    cycle_stack.append(child)
                    stack.append((child, iter(G[child])))
                else:
                    i = cycle_stack.index(child)
                    if i < len(cycle_stack) - 2:
                        output_cycles.add(get_hashable_cycle(cycle_stack[i:]))

            except StopIteration:
                stack.pop()
                cycle_stack.pop()

    return [list(i) for i in output_cycles]


G = nx.Graph()

G.add_node(1)

G.add_nodes_from([2, 3])

G.add_nodes_from([
    (4, {"color": "res"}),
    (5, {"color": "green"}),
])
H = nx.path_graph(10)
G.add_nodes_from(H)
G.add_node(H)

# G can also be grown by adding one edge at a time,
G.add_edge(1, 2)
e = (2, 3)
# by adding a list of edges,
G.add_edge(*e)
nx.has_path(G, 1, 2)
G.clear()

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")  # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

DG = nx.DiGraph()
DG.add_edge(2, 1)  # adds the nodes in order 2, 1
DG.add_edge(1, 3)
DG.add_edge(2, 4)
DG.add_edge(1, 2)
assert list(DG.successors(2)) == [1, 4]
assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]

print(list(G.nodes))

print(list(G.edges))

print(list(G.adj[1]))  # or list(G.neighbors(1))

print(G.degree[1])  # the number of edges incident to 1

print(G.edges([2, 'm']))

print(G.degree([2, 3]))

G.remove_node(2)
G.remove_nodes_from("spam")
print(list(G.nodes))

G.remove_edge(1, 3)

print("create a DiGraph using the connections from G")
G.add_edge(1, 2)
H = nx.DiGraph(G)  # create a DiGraph using the connections from G
print(list(H.edges()))

edge_list = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edge_list)  # create a graph from an edge list
print(list(H.edges()))

adjacency_dict = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
H = nx.Graph(adjacency_dict)  # create a Graph dict mapping nodes to nbrs
print(list(H.edges()))

DG = nx.DiGraph()
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75), (1, 4, 0.6), (2, 3, 0.3), (4, 2, 0.7), (2, 1, 0.2)])
# DG.out_degree(1, weight='weight')

DG.degree(1, weight='weight')

print(list(DG.successors(1)))

print(list(DG.neighbors(1)))

print(list(simple_cycles(DG)))
print("===")
print(list(recursive_simple_cycles(DG)))

print(list(nx.cycle_basis(DG.to_undirected())))
print(list(nx.find_cycle(DG.to_undirected())))

print(find_all_cycles(DG))
