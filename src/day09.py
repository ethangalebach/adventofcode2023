import utils
import time
import numpy as np
from functools import partial

input_path = utils.get_input_path(__file__)


def get_next_value(line, part):
    seq = np.array(list(map(int,line.split())))
    hist_len = len(seq)
    hist = np.array([seq])
    while any(seq != 0):
        seq = seq[1:] - seq[:-1]
        #add zeroes to seq before appending
        hist = np.append(
            hist,
            [np.append((hist_len-len(seq))*[0],[seq])],
           axis=0)
    if part == 1:
        return sum(hist[:,-1])
    elif part == 2:
        return sum(v if i%2==0 else -v for i,v in enumerate(np.diag(hist)))


def get_answer(path, part:int):
    with open(path) as f:
        lines = [line for line in f if line.strip()]
    next_values = utils.parallel_apply(
        partial(get_next_value,part=part), lines)
    return sum(next_values)


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
    run(part=1,test_expected=114)
    run(part=2,test_expected=2)