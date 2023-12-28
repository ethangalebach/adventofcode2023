import utils
import time
import numpy as np
from multiprocessing import Pool
from collections import Counter
from functools import partial

input_path = utils.get_input_path(__file__)

TYPE_ORDER = [
    'Five of a kind', 'Four of a kind', 'Full house', 'Three of a kind',
    'Two pair', 'One pair', 'High card']

CARD_ORDER= {
    1: ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
    2: ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1', 'J']}

def cmp_hand_type(hand_type_bid, part):
    type_rank = TYPE_ORDER.index(hand_type_bid[1])
    card_ranks = tuple(
        CARD_ORDER[part].index(card) for card in hand_type_bid[0])
    return type_rank, *card_ranks


def parallel_apply(func, input_path:str) -> int:
    with open(input_path) as f:
        lines = [line for line in f if line.strip()]
    with Pool() as pool:
        results = pool.map(func, lines)
    return results


def get_type(hand, part):
    type = 'High card'
    counter = Counter(hand)
    if part == 2 and counter.get('J'):
        most_common = counter.most_common(1)[0]
        if most_common[1] < 5:
            if most_common[0] == 'J':
                most_common = counter.most_common(2)[1]
            hand = hand.replace('J', most_common[0])
    for card, cnt in Counter(hand).items():
        if cnt == 5:
            return 'Five of a kind'
        if cnt == 4:
            return 'Four of a kind'
        if cnt == 3:
            if type == 'High card':
                type = 'Three of a kind'
            elif type == 'One pair':
                return 'Full house'
            else:
                raise ValueError('impossible hand')
        if cnt == 2:
            if type == 'High card':
                type = 'One pair'
            elif type == 'Three of a kind':
                return 'Full house'
            elif type == 'One pair':
                return 'Two pair'
            else:
                raise ValueError('impossible hand')
    return type


def get_hand_type_bid(line:str, part:int) -> tuple:
    hand, bid = line.strip().split()
    type = get_type(hand, part)
    return hand, type, int(bid)


def get_winning(bid, rank):
    return bid*rank


def get_answer(path, part:int):
    hand_type_bids = parallel_apply(partial(get_hand_type_bid,part=part), path)
    num_hands = len(hand_type_bids)
    sorted_hand_type_bids = sorted(
        hand_type_bids,
        key=partial(cmp_hand_type,part=part)
    )
    with Pool() as pool:
        results = pool.starmap(
            get_winning,
            ((htb[2], num_hands-i) for i, htb in enumerate(sorted_hand_type_bids)))
    return sum(results)


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
    run(part=1,test_expected=6440)
    run(part=2,test_expected=5905)