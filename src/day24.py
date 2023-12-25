import utils
import time
import numpy as np
import itertools
from scipy import optimize as opt

input_path = utils.get_input_path(__file__)

def get_hailstones(path:str) -> list:
    hailstones = []
    with open(path) as f:
        for line in f:
            if line.strip():
                p, v = line.strip().split('@')
                hailstones.append(list(map(int,p.split(',') + v.split(','))))
    return hailstones

def get_intersection_point(h1,h2):
    m1 = h1[4]/h1[3]
    m2 = h2[4]/h2[3]
    if m1 == m2:
        return None
    b1 = h1[1] - h1[0]*m1
    b2 = h2[1] - h2[0]*m2
    x = (b1 - b2)/(m2 - m1)
    y = m1*x + b1
    return x,y

def get_intersections_in_area(hailstones, area):
    intersections_in_area = 0
    for h1, h2 in itertools.combinations(hailstones,2):
        xy = get_intersection_point(h1, h2)
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

def equations(x, hailstones):
    h0,h1,h2,h3 = hailstones[-4:]
    if h0[0] > 1_000_000_000_000:
        h0[:3] = [d*10**-15 for d in h0[:3]]
        h1[:3] = [d*10**-15 for d in h1[:3]]
        h2[:3] = [d*10**-15 for d in h2[:3]]
        h3[:3] = [d*10**-15 for d in h3[:3]]

    return [
        x[0] + (x[3] - h0[3])*x[6] - h0[0],
        x[1] + (x[4] - h0[4])*x[6] - h0[1],
        x[2] + (x[5] - h0[5])*x[6] - h0[2],
        x[0] + (x[3] - h1[3])*x[7] - h1[0],
        x[1] + (x[4] - h1[4])*x[7] - h1[1],
        x[2] + (x[5] - h1[5])*x[7] - h1[2],
        x[0] + (x[3] - h2[3])*x[8] - h2[0],
        x[1] + (x[4] - h2[4])*x[8] - h2[1],
        x[2] + (x[5] - h2[5])*x[8] - h2[2],
        x[0] + (x[3] - h3[3])*x[9] - h3[0],
        x[1] + (x[4] - h3[4])*x[9] - h3[1],
        x[2] + (x[5] - h3[5])*x[9] - h3[2],
    ]

def get_answer(path, part:int):
    hailstones = get_hailstones(path)
    if part == 1:
        if path == utils.get_test_path(__file__, part):
            area = (7,27)
        else:
            area = (200_000_000_000_000,400_000_000_000_000)
        return get_intersections_in_area(hailstones, area)
    if part == 2:
        roots = opt.root(
            fun=equations,
            x0=[2]*10,
            args=(hailstones),
            method='lm',
        ).x
        if hailstones[0][0] > 1_000_000_000_000:
            roots[:3] = [d*10**15 for d in roots[:3]]
        x = roots[0] + roots[3]*roots[6]
        y = roots[1] + roots[4]*roots[6]
        z = roots[2] + roots[5]*roots[6]
        return round(x + y + z)


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
    run(part=2,test_expected=47)