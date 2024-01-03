import utils
import time
import numpy as np
import itertools

input_path = utils.get_input_path(__file__)


def expand(universe, mult=2):
    xs,ys = universe
    xcur, ycur = max(xs)-1, max(ys)-1
    while ycur>=0:
        if ycur not in ys:
            ys = [y + mult - 1 if y > ycur else y for y in ys]
        ycur-=1
    while xcur>=0:
        if xcur not in xs:
            xs = [x + mult - 1 if x > xcur else x for x in xs]
        xcur-=1
    return list(zip(xs,ys))


def get_universe(path):
    xs,ys = [],[]
    with open(path) as f:
        for y, line in enumerate(f):
            cur_xs = [x for x, c in enumerate(line) if c == '#']
            xs += cur_xs
            ys += [y]*len(cur_xs)
    return xs, ys


def get_answer(path, part:int):
    universe = get_universe(path)
    if part == 1:
        eu = expand(universe)
    elif part == 2:
        if path == utils.get_test_path(__file__, 2):
            eu = expand(universe, 100)
        else:
            eu = expand(universe, 1_000_000)
    dist = 0
    ln = 0
    for (y1,x1),(y2,x2) in itertools.combinations(eu,2):
        dist += np.abs(y1-y2) + np.abs(x1-x2)
    return dist


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
    run(part=1,test_expected=374)
    run(part=2,test_expected=8410)