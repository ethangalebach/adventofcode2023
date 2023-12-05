import utils
import time
import numpy as np
import itertools
from collections.abc import Iterator
from collections import defaultdict

input_path = utils.get_input_path(__file__)

digit_chars = ['0','1','2','3','4','5','6','7','8','9']


def get_matrix(path:str) -> int:
    with open(path) as f:
        mtrx = np.array([list(line.strip()) for line in f if line.strip()])
    return mtrx


def get_answer(path, part:int):
    mtrx = get_matrix(path)
    parts = get_parts(mtrx)
    if part == 1:
        return sum([num for (num, _) in parts])
    elif part == 2:
        gear_ratios = get_gear_ratios(parts)
        return sum(gear_ratios)
    else:
        raise Exception('not part 1 or 2')


def run(part:int, test_expected):
    test_path = utils.get_test_path(__file__, part)
    test_answer = get_answer(test_path, part=part)
    assert test_answer ==  test_expected, (
        f"got calibration sum of {test_answer}, should be {test_expected}"
    )
    start_time = time.time()
    answer = get_answer(input_path, part=part)
    end_time = time.time()
    duration = 1000*(end_time - start_time)
    print(f"Part {part} Answer: {answer}, in {duration} ms")


if __name__ == "__main__":
    run(part=1,test_expected=4361)
    run(part=2,test_expected=467835)