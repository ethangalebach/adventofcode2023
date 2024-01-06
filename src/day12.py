import utils
import time
from functools import lru_cache

input_path = utils.get_input_path(__file__)


@lru_cache(maxsize=None)
def cnt_arr(spring_str, size_tuple, hash_buffer=0):
    cnt = 0
    sz = size_tuple[0]
    if spring_str == '':
        if len(size_tuple) == 1 and sz == hash_buffer:
            return 1
        else:
            return 0
    spring = spring_str[0]
    if hash_buffer == 0:
        if spring in ('.','?'):
            cnt += cnt_arr(spring_str[1:], size_tuple)
        if spring in ('#','?'):
            cnt += cnt_arr(spring_str[1:], size_tuple,1)
    else:
        if spring in ('.','?') and hash_buffer == sz:
            if len(size_tuple) == 1:
                if '#' not in spring_str:
                    return 1
                else:
                    return 0
            else:
                cnt += cnt_arr(spring_str[1:], size_tuple[1:],0)
        if spring in ('#','?') and hash_buffer < sz:
            cnt += cnt_arr(spring_str[1:], size_tuple, hash_buffer+1)
    return cnt


def get_records(path,part):
    with open(path) as f:
        if part == 1:
            return [line.strip() for line in f if line.strip()]
        elif part == 2:
            lines = []
            for line in f:
                if line.strip():
                    spring_str, size_str = line.strip().split(' ')
                    lines.append(
                        4*(spring_str+'?')+spring_str+' '+ \
                        4*(size_str+',')+size_str)
            return lines


def get_answer(path, part:int):
    records = get_records(path, part)
    cnts = []
    for record in records:
        spring_str, size_str = record.split(' ')
        cnts.append(cnt_arr(spring_str, tuple(map(int,size_str.split(',')))))
    return sum(cnts)


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
    run(part=1,test_expected=21)
    run(part=2,test_expected=525152)