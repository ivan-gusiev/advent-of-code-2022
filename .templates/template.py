from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, Output, clean_lines
from io import TextIOWrapper

def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

def solve(f: TextIOWrapper):
    lines = clean_lines(f)
    solve_p1(lines)
    solve_p2(lines)

def solve_p1(lines: list[str]):
    print("p1", len(lines))

def solve_p2(lines: list[str]):
    print("p2", sum(map(len, lines)))

if __name__ == '__main__':
    main()