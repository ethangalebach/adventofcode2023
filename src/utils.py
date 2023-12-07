import os
from multiprocessing import Pool

def get_input_path(file):
    filename = os.path.basename(file)
    filename = filename.removesuffix('.py') + '.txt'
    file_dir = os.path.dirname(os.path.dirname(file))
    return os.path.join(file_dir, f'input/{filename}')

def get_test_path(file, part):
    filename = os.path.basename(file)
    filename = filename.removesuffix('.py') + f'_pt{part}.txt'
    file_dir = os.path.dirname(os.path.dirname(file))
    return os.path.join(file_dir, f'tests/test_{filename}')

def parallel_apply(func, lines) -> list:
    with Pool() as pool:
        results = pool.map(func, lines)
    return results