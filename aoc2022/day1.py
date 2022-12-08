from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, split_by_newline
from io import TextIOWrapper


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            solve(f)


def solve(f: TextIOWrapper):
    lines = f.readlines()
    groups = split_by_newline(lines)
    calories = [0]  # if this list is empty, max fails
    for group in groups:
        items = list(map(int, group))
        calories.append(sum(items))

    calories.sort(reverse=True)
    # top_one = calories[0]
    # print (top_one)

    top_three = calories[0:3]
    print(sum(top_three))


if __name__ == "__main__":
    main()
