import os

def get_input_path(file):
    filename = os.path.basename(file)
    filename = filename.removesuffix('.py') + '.txt'
    file_dir = os.path.dirname(os.path.dirname(file))
    return os.path.join(file_dir, f'input/{filename}')

def get_test_path(file):
    filename = os.path.basename(file)
    filename = filename.removesuffix('.py') + '.txt'
    file_dir = os.path.dirname(os.path.dirname(file))
    return os.path.join(file_dir, f'tests/test_{filename}')