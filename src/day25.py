import utils
import time
import numpy as np
import networkx as nx
import itertools

input_path = utils.get_input_path(__file__)

def parse_graph(path:str):
    G = nx.Graph()
    with open(path) as f:
        for line in f:
            if line.strip():
                left_node, right_nodes = line.strip().split(': ')
                right_nodes = right_nodes.split(' ')
                for right_node in right_nodes:
                    G.add_edge(left_node, right_node)
    return G


def divide_graph(G):
    centrality = nx.edge_betweenness_centrality(G)
    sorted_items = sorted(centrality.items(), key=lambda item: item[1],reverse=True)
    for (e1,_),(e2,_),(e3,_) in itertools.combinations(sorted_items,3):
        H = G.copy()
        H.remove_edges_from([e1,e2,e3])
        components = list(nx.connected_components(H))
        if len(components) == 2:
            return [G.subgraph(c).copy() for c in components]


def get_answer(path, part:int):
    G = parse_graph(path)
    if part == 1:
        group1, group2 = divide_graph(G)
        return group1.number_of_nodes() * group2.number_of_nodes()


def run(part:int, test_expected):
    test_path = utils.get_test_path(__file__, part)
    test_answer = get_answer(test_path, part=part)
    assert test_answer ==  test_expected, (
        f"got {test_answer}, should be {test_expected}"
    )
    start_time = time.time()
    answer = get_answer(input_path, part=part)
    end_time = time.time()
    duration = 1000*(end_time - start_time)
    print(f"Part {part} Answer: {answer}, in {duration} ms")


if __name__ == "__main__":
    run(part=1,test_expected=54)