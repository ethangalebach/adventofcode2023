import utils
import time
from multiprocessing import Pool
import numpy as np
import itertools

digit_chars = ['0','1','2','3','4','5','6','7','8','9']

def has_symbol_neighbor(mtrx, i, j):
    for (offset_y, offset_x) in itertools.product([-1,0,1],repeat=2):
        if i+offset_y > mtrx.shape[0]-1 or j+offset_x > mtrx.shape[0]-1 or \
           i+offset_y < 0 or j+offset_x<0:
            continue
        if mtrx[i+offset_y,j+offset_x] not in digit_chars + ['.']:
            return True
    return False

def get_part_numbers(mtrx) -> int:
    part_nums = []
    for i, vec in enumerate(mtrx):
        sym_adj = False
        num = ''
        for j, char in enumerate(vec):
            if char in digit_chars:
                num += char
                sym_adj = sym_adj or has_symbol_neighbor(mtrx, i, j)
                if j == len(vec) - 1 and sym_adj:
                    part_nums.append(int(num))
            else:
                if sym_adj:
                    part_nums.append(int(num))
                num = ''
                sym_adj = False
    return part_nums

def get_matrix(input_path:str) -> int:
    with open(input_path) as f:
        mtrx = np.array([list(line.strip()) for line in f if line.strip()])
    return mtrx

def get_answer(input_path: str, part: int) -> int:
    mtrx = get_matrix(input_path)
    if part == 1:
        part_nums = get_part_numbers(mtrx)
        return sum(part_nums)
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    pt1_test_path = utils.get_test_path(__file__, 1)
    pt1_test_answer = get_answer(pt1_test_path, part=1)
    assert pt1_test_answer ==  4361, (
        f"got calibration sum of {pt1_test_answer}, should be 4361"
    )
    pt1_start_time = time.time()
    part1_answer = get_answer(input_path, part=1)
    pt1_end_time = time.time()
    pt1_duration = 1000*(pt1_end_time - pt1_start_time)
    print(f"Part 1 Answer: {part1_answer}, in {pt1_duration} ms")

    # pt2_test_path = utils.get_test_path(__file__, 2)
    # pt2_test_answer = get_answer(pt2_test_path, part=2)
    # assert pt2_test_answer == 281, (
    #     f"got calibration sum of {pt2_test_answer}, should be 281"
    # )
    # pt2_start_time = time.time()
    # part2_answer = get_answer(input_path, part=2)
    # pt2_end_time = time.time()
    # pt2_duration = 1000*(pt2_end_time - pt2_start_time)
    # print(f"Part 2 Answer: {part2_answer}, in {pt2_duration} ms")