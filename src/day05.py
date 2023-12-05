import utils
import time

input_path = utils.get_input_path(__file__)


def traverse(num:int, source:str, almanac) -> int:
    dest_num = None
    for dest, mp in almanac.get(source).items():
        for k,v in mp.items():
            if num >= k[0] and num <= k[1]:
                dest_num = num+v
        dest_num = dest_num or num
        if dest == 'location':
            return dest_num
        else:
            return traverse(dest_num, dest, almanac)


def get_lowest_loc(almanac) -> int:
    locations = []
    for seed in almanac.get('seeds'):
        locations.append(traverse(int(seed), 'seed',almanac))
    return min(locations)


def get_almanac(path:str) -> int:
    source = dest = mp = None
    almanac = {}
    with open(path) as f:
        for line in f:
            if line.strip().startswith('seeds:'):
                seeds = line.strip().split(': ')[-1].split(' ')
                almanac['seeds'] = seeds
            elif not line.strip():
                if source:
                    almanac[source] = {dest: mp}
            elif line.strip().endswith('map:'):
                source,dest = line.strip().split(' ')[0].split('-to-')
                mp = {}
            else:
                dest_start, source_start, lngth = line.strip().split(' ')
                mp |= {(
                    int(source_start),
                    int(lngth)+int(source_start)-1
                ): int(dest_start) - int(source_start)}
    if source:
        almanac[source] = {dest: mp}
    return almanac


def get_answer(path, part:int):
    almanac = get_almanac(path)
    if part == 1:
        return get_lowest_loc(almanac)
    elif part == 2:
        pass
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
    run(part=1,test_expected=35)
    # run(part=2,test_expected=467835)