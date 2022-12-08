from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, split_to_chunks
from io import TextIOWrapper
from typing import Tuple


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            solve(f)


def solve(f: TextIOWrapper):
    lines = list(map(str.rstrip, f.readlines()))
    solve_p1(lines)
    solve_p2(lines)


def line_to_sections(line: str) -> Tuple[str, str]:
    half = int(len(line) / 2)
    return line[0:half], line[half:]


def priority(item: str) -> int:
    lower = ord(item) - ord("a") + 1
    if lower > 0:
        return lower

    return ord(item) - ord("A") + 27


def common_item(lhs: str, rhs: str) -> str:
    return common_item_of_list([lhs, rhs])


def common_item_of_list(lst: list[str]) -> str:
    sets = [set(s) for s in lst]
    intersection = set.intersection(*sets)
    return list(intersection)[0]


def solve_p1(lines: list[str]):
    results = []
    for first, second in map(line_to_sections, lines):
        item = common_item(first, second)
        results.append(priority(item))
    print("p1", sum(results))


def solve_p2(lines: list[str]):
    groups = split_to_chunks(lines, 3)
    badges = map(common_item_of_list, groups)
    priorities = map(priority, badges)
    print("p2", sum(priorities))


if __name__ == "__main__":
    main()
