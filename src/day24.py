import utils
import time
import numpy as np
import itertools

input_path = utils.get_input_path(__file__)

def get_hailstones(path:str) -> list:
    hailstones = []
    with open(path) as f:
        for line in f:
            if line.strip():
                p, v = line.strip().split('@')
                hailstones.append(list(map(int,p.split(',') + v.split(','))))
    return hailstones

def get_intersection(h1,h2):
    m1 = h1[4]/h1[3]
    m2 = h2[4]/h2[3]
    if m1 == m2:
        return None
    b1 = h1[1] - h1[0]*m1
    b2 = h2[1] - h2[0]*m2
    x = (b1 - b2)/(m2 - m1)
    y = m1*x + b1
    return x,y

def get_answer(path, part:int):
    hailstones = get_hailstones(path)
    if path == utils.get_test_path(__file__, part):
        area = (7,27)
    else:
        area = (200_000_000_000_000,400_000_000_000_000)
    intersections_in_area = 0
    for h1, h2 in itertools.combinations(hailstones,2):
        if part == 1:
            xy = get_intersection(h1, h2)
            if xy == None:
                continue
            else:
                x,y = xy
            if (
                x>=area[0] and x<=area[1] and y>=area[0] and y<=area[1] and
                (x - h1[0])*h1[3]>0 and (x - h2[0])*h2[3]>0
            ):
                intersections_in_area += 1
    return intersections_in_area

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
    run(part=1,test_expected=2)
    # run(part=2,test_expected=71503)