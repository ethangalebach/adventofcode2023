import utils

def get_calibration_value(line:str) -> int:
    for c in line:
        if c.isdigit():
            first_digit = int(c)
            break
    for c in reversed(line):
        if c.isdigit():
            return first_digit*10 + int(c)

def get_calibration_sum(input_path:str) -> int:
    cal_sum = 0
    with open(input_path) as f:
        for line in f:
            if line.strip():
                cal_sum += get_calibration_value(line)
    return cal_sum

def get_answer(input_path: str, part: int) -> int:
    if part == 1:
        return get_calibration_sum(input_path)
    elif part == 2:
        return (len(map.get_path_with_ideal_trailhead()))
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_answer = get_answer(test_path, part=1)
    assert test_answer == 142, (
        f"got calibration sum of {test_answer}, should be 142"
    )
    part1_answer = get_answer(input_path, part=1)
    # part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        # f"Part 2 Answer: {part2_answer}"
    )