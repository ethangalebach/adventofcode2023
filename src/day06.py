import utils
import time
import numpy as np

input_path = utils.get_input_path(__file__)

def get_races(path:str, part:int) -> list:
    races = []
    with open(path) as f:
        for line in f:
            if line.strip():
                digits = line.strip().split(':')[1].split()
                if part == 1:
                    races.append(list(map(int, digits)))
                if part == 2:
                    digits = "".join(digits)
                    races.append(int(digits))
    if part == 1:
        return list(zip(races[0], races[1]))
    if part == 2:
        return [races]


def get_answer(path, part:int):
    races = get_races(path, part)
    win_arr = np.array([])
    for time,record in races:
        wins = 0
        for charge in range(time):
            if charge*(time-charge) > record:
                wins += 1
        win_arr = np.append(win_arr, wins)
    return np.prod(win_arr)


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
    run(part=1,test_expected=288)
    run(part=2,test_expected=71503)