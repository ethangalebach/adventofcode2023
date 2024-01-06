import utils
import time
import numpy as np
import itertools
from functools import lru_cache
from pprint import pprint
import math

input_path = utils.get_input_path(__file__)

def distribute_items(total_items, bin_capacities):
    def _distribute(remaining_items, bin_index, current_distribution):
        if bin_index == len(bin_capacities):
            if remaining_items == 0:
                yield current_distribution
        else:
            max_items_this_bin = min(
                remaining_items, bin_capacities[bin_index])
            for i in range(max_items_this_bin+1):
                yield from _distribute(
                    remaining_items-i,
                    bin_index+1,
                    current_distribution+(i,))
    yield from _distribute(total_items, 0, ())

@lru_cache(maxsize=None)
def _get_prs(hashes, cap):
    prs = []
    if hashes == 0:
        return [[tuple(cap*['.']),1]]
    elif 2*hashes-1 < cap:
        for p in unique_prototypes(hashes):
            hgrps = len(list(filter(None,''.join(p).split('.'))))
            "closed-open"
            prs.append([p+('.',)*(cap-len(p)),math.comb(cap-hashes-1,hgrps-1)])
            "open-open"
            prs.append([('.',)+p+('.',)*(cap-len(p)-1),math.comb(cap-hashes-1,hgrps)])
            "open-closed"
            prs.append([('.',)*(cap-len(p))+p,math.comb(cap-hashes-1,hgrps-1)])
            "closed-closed"
            if hgrps >= 2:
                dot_idx = p.index('.')
                prs.append([p[:dot_idx]+('.',)*(cap-len(p))+p[dot_idx:],math.comb(cap-hashes-1,hgrps-2)])
        return prs
    else:
        for p in unique_permutations(cap,hashes):
            prs.append([p,1])
        return prs


def unique_permutations(cap, hashes):
    for positions in itertools.combinations(range(cap), hashes):
        p = ['.'] * cap
        for pos in positions:
            p[pos] = '#'
        yield tuple(p)


def unique_prototypes(hashes):
    p = '#' * hashes
    for subset in power_set(len(p)-1):
        tmp = p
        for idx in subset:
            tmp = tmp[:idx] + '.' + tmp[idx:]
        yield tuple(tmp)


def power_set(n):
    for i in range(2**n):
        subset = {j+1 for j in range(n) if i & (1<<j)}
        yield sorted(tuple(subset),reverse=True)


class CountArrangements:
    def get_prototypes_and_replicas(self, qgrp, hashes):
        cap = self.capacities[qgrp]
        return _get_prs(hashes, cap)

    def get_dist_arrangements(self,dist):
        combined_prototypes = []
        arrangements = 0
        for qgrp,hashes in enumerate(dist):
            prs = self.get_prototypes_and_replicas(qgrp, hashes)
            combined_prototypes.append(prs
        for comb in itertools.product(*combined_prototypes):
            candidate = list(self.spring_str)
            r = np.prod([r for _,r in comb])
            for i, (p,_) in enumerate(comb):
                start,end = self.q_idx_grps[i]
                candidate[start:end] = p
            if tuple(map(len,filter(None,''.join(candidate).split('.')))) == self.size_tuple
                arrangements += r
        return arrangements

    def __call__(self, record):
        arrangements = 0
        self.spring_str, self.size_str = record.split(' ')
        self.size_tuple = tuple(map(int,self.size_str.split(',')))
        self.known_d = self.spring_str.count('#')
        self.total_d = sum(self.size_tuple)
        self.unknown_d = self.total_d - self.known_d
        self.q_idx_grps, q_start = [], None
        for i,c in enumerate(self.spring_str):
            if c == '?':
                if q_start == None:
                    q_start = i
            else:
                if q_start != None:
                    self.q_idx_grps.append((q_start,i))
                    q_start = None
        if q_start != None:
            self.q_idx_grps.append((q_start,len(self.spring_str)))
        self.capacities = tuple(end-start for start,end in self.q_idx_grps)
        for dist in distribute_items(self.unknown_d,self.capacities):
            arrangements += self.get_dist_arrangements(dist)
        return arrangements


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

def simple_count(record):
    arrangements = 0
    spring_str, size_str = record.split(' ')
    size_tuple = tuple(map(int,size_str.split(',')))
    known_d = spring_str.count('#')
    total_d = sum(size_tuple)
    unknown_d = total_d - known_d
    q_idxs = [i for i,c in enumerate(spring_str) if c == '?']
    for positions in itertools.combinations(range(len(q_idxs)), unknown_d):
        candidate = list(spring_str)
        for p in positions:
            candidate[q_idxs[p]] = '#'
        candidate = [c if c != '?' else '.' for c in candidate]
        if size_tuple == tuple(map(len,filter(None,''.join(candidate).split('.')))):
            arrangements += 1
    return arrangements


def get_answer(path, part:int):
    records = get_records(path, part)
    count_arr = CountArrangements()
    if part == 2:
        print(records)
        num_arrangements = 0
        for i,r in enumerate(records):
            rec_arr = count_arr(r)
            num_arrangements += rec_arr
            if i % 10 == 0:
                print(i)
            print(i, rec_arr)
        return num_arrangements
    if part == 1:
        num_arrangements = utils.parallel_apply(count_arr,records)
        return sum(num_arrangements)


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
    # run(part=2,test_expected=525152)