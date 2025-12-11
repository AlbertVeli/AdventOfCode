#!/usr/bin/env python3

import sys
import networkx as nx

def parse_graph():
    G = nx.DiGraph()
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
    for line in lines:
        name, rhs = line.strip().split(':')
        name = name.strip()
        targets = rhs.strip().split()
        #print(f'{name} -> {targets}')
        for t in targets:
            G.add_edge(name, t)
    return G

def count_paths_between(G, topo, src, dst):
    """
    Count simple directed paths in a DAG using DP
    over a topological order.
    """
    if src not in G or dst not in G:
        return 0

    ways = {node: 0 for node in G.nodes}
    ways[src] = 1

    for u in topo:
        if ways[u] == 0:
            continue
        for v in G.successors(u):
            ways[v] += ways[u]

    return ways[dst]

def count_paths_with_both(G, start, end, a, b):
    """
    Count paths start -> end that visit both a and b in any order.
    """
    topo = list(nx.topological_sort(G))

    # Compute all segment path counts
    p_start_a = count_paths_between(G, topo, start, a)
    p_start_b = count_paths_between(G, topo, start, b)
    p_a_b      = count_paths_between(G, topo, a, b)
    p_b_a      = count_paths_between(G, topo, b, a)
    p_a_end    = count_paths_between(G, topo, a, end)
    p_b_end    = count_paths_between(G, topo, b, end)

    # Two possible orders through the DAG:
    via_b_then_a = p_start_b * p_b_a * p_a_end
    via_a_then_b = p_start_a * p_a_b * p_b_end

    return via_b_then_a + via_a_then_b


G = parse_graph()
print('Part 2:', count_paths_with_both(G, 'svr', 'out', 'dac', 'fft'))
