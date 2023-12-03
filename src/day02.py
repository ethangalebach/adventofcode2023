import utils
import time
from multiprocessing import Pool
from math import inf

def get_pt1_calibration_value(line:str) -> int:
    first_digit = int(next(c for c in line if c.isdigit()))
    last_digit = int(next(c for c in line[::-1] if c.isdigit()))
    return first_digit*10 + last_digit

def get_pt2_calibration_value(line:str) -> int:
    digit_words = ['zero','one','two','three','four','five','six','seven','eight','nine']
    digit_chars = ['0','1','2','3','4','5','6','7','8','9']
    first_digit = last_digit = None
    first_idx = last_idx = inf
    for i, s in enumerate(digit_words + digit_chars):
        if s in line:
            if line.index(s) < first_idx:
                first_idx = line.index(s)
                first_digit = i % 10
            if line[::-1].index(s[::-1]) < last_idx:
                last_idx = line[::-1].index(s[::-1])
                last_digit = i % 10
    return first_digit*10 + last_digit

def parallel_apply(func, input_path:str) -> int:
    with open(input_path) as f:
        lines = [line for line in f if line.strip()]
    with Pool() as pool:
        results = pool.map(func, lines)
    return sum(results)

def get_answer(input_path: str, part: int) -> int:
    if part == 1:
        return parallel_apply(get_pt1_calibration_value, input_path)
    elif part == 2:
        return parallel_apply(get_pt2_calibration_value, input_path)
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    pt1_test_path = utils.get_test_path(__file__, 1)
    pt1_test_answer = get_answer(pt1_test_path, part=1)
    assert pt1_test_answer ==  0, (
        f"got calibration sum of {pt1_test_answer}, should be "
    )
    pt1_start_time = time.time()
    part1_answer = get_answer(input_path, part=1)
    pt1_end_time = time.time()
    pt1_duration = 1000*(pt1_end_time - pt1_start_time)
    print(f"Part 1 Answer: {part1_answer}, in {pt1_duration} ms")

    pt2_test_path = utils.get_test_path(__file__, 2)
    pt2_test_answer = get_answer(pt2_test_path, part=2)
    assert pt2_test_answer == , (
        f"got calibration sum of {pt2_test_answer}, should be "
    )
    pt2_start_time = time.time()
    part2_answer = get_answer(input_path, part=2)
    pt2_end_time = time.time()
    pt2_duration = 1000*(pt2_end_time - pt2_start_time)
    print(f"Part 2 Answer: {part2_answer}, in {pt2_duration} ms")