from aoc2022.util import Input, split_by_newline
from io import TextIOWrapper

def main():
    input = Input(__file__)
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

def solve(f: TextIOWrapper):
    lines = f.readlines()
    solve_p1(lines)
    solve_p2(lines)

def solve_p1(lines: list[str]):
    print(sum(map(int, lines)))

def solve_p2(lines: list[str]):
    print(max(map(int, lines)))

if __name__ == '__main__':
    main()