from aoc2022.util import Input, clean_lines
from io import TextIOWrapper
from typing import Tuple

def main():
    input = Input(__file__)
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

def solve(f: TextIOWrapper):
    line = f.read()
    solve_p1(line)
    solve_p2(line)

def solve_p1(line: str):
    print("p1", get_message_start(4, line))

def solve_p2(line: str):
    print("p2", get_message_start(14, line))

def get_message_start(chunk_size: int, line: str) -> int:
    result = -1
    for i in range(len(line)):
        l, r = chunk_range(i, chunk_size)
        chunk = line[l:r]
        if len(set(chunk)) == chunk_size:
            result = i
            break
    return result

def chunk_range(i: int, size: int) -> Tuple[int, int]:
    return max(0, i-size), i

if __name__ == '__main__':
    main()