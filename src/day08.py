import utils
import time
import networkx as nx
import itertools
import math

input_path = utils.get_input_path(__file__)

def get_num_steps(instructions, G, part):
    steps = 0
    if part == 1:
        starting_nodes = ['AAA']
        current_nodes = starting_nodes.copy()
        terminating_suffix = 'ZZZ'
    elif part == 2:
        starting_nodes = [node for node in G.nodes() if node.endswith('A')]
        current_nodes = starting_nodes.copy()
        terminating_suffix = 'Z'
    z_steps = {}
    for instruction in itertools.cycle(instructions):
        steps += 1
        new_nodes = []
        for i, node in enumerate(current_nodes):
            for _, child, attributes in G.edges(node, data=True):
                if attributes.get(instruction):
                    new_nodes.append(child)
                    if (child.endswith(terminating_suffix) and
                        steps % len(instructions) == 0
                    ):
                        z_steps[starting_nodes[i]] = steps
        if set(z_steps.keys()) == set(starting_nodes):
            return math.lcm(*z_steps.values())
        current_nodes = new_nodes


def parse_graph(path:str) -> list:
    G = nx.DiGraph()
    instruction_line = True
    with open(path) as f:
        for line in f:
            if instruction_line:
                instructions = line.strip()
                instruction_line = False
            elif line.strip():
                parent, children = line.strip().split(' = ')
                left_child, right_child = children[1:-1].split(', ')
                G.add_edge(parent, left_child, L=True)
                G.add_edge(parent, right_child, R=True)
    return instructions, G


def get_answer(path, part:int):
    instructions, G = parse_graph(path)
    return get_num_steps(instructions, G, part)


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
    run(part=1,test_expected=6)
    run(part=2,test_expected=6)