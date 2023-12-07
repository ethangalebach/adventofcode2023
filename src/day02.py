import utils
import time
import numpy as np

input_path = utils.get_input_path(__file__)

def get_powers(games):
    powers = []
    for num, sets in games.items():
        game_mins = {}
        for st in sets:
            for cnt,clr in st:
                if not game_mins.get(clr):
                    game_mins[clr] = int(cnt)
                else:
                    game_mins[clr] = max([game_mins.get(clr), int(cnt)])
        power = np.prod(np.array(list(game_mins.values())))
        powers.append(power)
    return powers


def get_possible_nums(games, max_counts):
    possible_nums = []
    for num, sets in games.items():
        if all(max_counts[clr] >= int(cnt) for st in sets for cnt,clr in st):
            possible_nums.append(int(num))
    return possible_nums


def get_games(path:str) -> list:
    games = {}
    with open(path) as f:
        for line in f:
            if line.strip():
                game = line.strip()
                num, sets = game.split(':')
                games[num.split()[-1]] = [
                    [clrcnt.split() for clrcnt in st.split(',')]
                    for st in sets.split(';')
                ]
    return games

def get_answer(path, part:int):
    games = get_games(path)
    if part == 1:
        max_counts = {'red':12,'green':13,'blue':14}
        return sum(get_possible_nums(games, max_counts))
    elif part == 2:
        return sum(get_powers(games))
    else:
        raise Exception('not part 1 or 2')


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
    run(part=1,test_expected=107)
    run(part=2,test_expected=2286)