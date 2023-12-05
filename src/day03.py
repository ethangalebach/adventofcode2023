import utils
import time
import numpy as np
import itertools
from collections.abc import Iterator
from collections import defaultdict

input_path = utils.get_input_path(__file__)

digit_chars = ['0','1','2','3','4','5','6','7','8','9']


def get_neighbors(mtrx, i, j) -> dict:
    nhbrs = {}
    for (offset_y, offset_x) in itertools.product([-1,0,1],repeat=2):
        if i+offset_y > mtrx.shape[0]-1 or j+offset_x > mtrx.shape[0]-1 or \
           i+offset_y < 0 or j+offset_x<0:
            continue
        if mtrx[i+offset_y,j+offset_x] not in digit_chars + ['.']:
            nhbrs[(i+offset_y,j+offset_x)] = mtrx[i+offset_y,j+offset_x]
    return nhbrs


def get_parts(mtrx) -> int:
    parts = []
    for i, vec in enumerate(mtrx):
        num = ''
        nhbrs = {}
        sym_adj = False
        for j, char in enumerate(vec):
            if char in digit_chars:
                num += char
                nhbrs |= get_neighbors(mtrx, i, j)
                sym_adj = sym_adj or bool(nhbrs)
                if j == len(vec) - 1 and sym_adj:
                    parts.append((int(num), nhbrs))
            else:
                if sym_adj:
                    parts.append((int(num), nhbrs))
                num = ''
                nhbrs = {}
                sym_adj = False
    return parts


def get_gear_ratios(parts) -> list[tuple[int,int]]:
    starred_nums = defaultdict(list)
    for num,nhbrs in parts:
        for coords,sym in nhbrs.items():
            if sym == '*':
                starred_nums[coords].append(num)
    gears = [v for k,v in starred_nums.items() if len(v) == 2]
    return [a*b for a,b in gears]


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