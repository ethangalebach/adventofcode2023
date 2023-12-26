import utils
import time
import numpy as np
from multiprocessing import Pool

input_path = utils.get_input_path(__file__)

def get_num_scratchcards(matches):
    num_scratchcards = np.array([1]*len(matches))
    for i, match in enumerate(matches):
        num_scratchcards[i+1:match+i+1] += num_scratchcards[i]
    return sum(num_scratchcards)


def get_num_matches(card) -> int:
    winners, mine = card
    return len(winners & mine)


def get_card(line:str) -> tuple:
    winners, mine = line.strip().split(': ')[1].split(' | ')
    return set(winners.split()), set(mine.split())


def parallel_apply(func, input_path:str) -> int:
    with open(input_path) as f:
        lines = [line for line in f if line.strip()]
    with Pool() as pool:
        results = pool.map(func, lines)
    return results


def get_answer(path, part:int):
    cards = parallel_apply(get_card, path)
    with Pool() as pool:
        matches = pool.map(get_num_matches, cards)
    if part == 1:
        points = [2**(num-1) if num > 0 else 0 for num in matches]
        return sum(points)
    if part == 2:
        return get_num_scratchcards(matches)


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
    run(part=1,test_expected=13)
    run(part=2,test_expected=30)