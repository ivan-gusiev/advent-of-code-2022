from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, split_by_newline
from io import TextIOWrapper
from typing import Dict, Final, Tuple


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            solve(f)


LOSS: Final[int] = 0
TIE: Final[int] = 3
WIN: Final[int] = 6

letter_scores: Dict[str, int] = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

fights: Dict[str, Dict[str, int]] = {
    "A": {
        "X": TIE,
        "Y": WIN,
        "Z": LOSS,
    },
    "B": {
        "X": LOSS,
        "Y": TIE,
        "Z": WIN,
    },
    "C": {
        "X": WIN,
        "Y": LOSS,
        "Z": TIE,
    },
}

strat_to_shape: Dict[str, Dict[str, str]] = {
    "A": {
        "X": "Z",
        "Y": "X",
        "Z": "Y",
    },
    "B": {
        "X": "X",
        "Y": "Y",
        "Z": "Z",
    },
    "C": {
        "X": "Y",
        "Y": "Z",
        "Z": "X",
    },
}


def calc_score(enemy: str, you: str) -> int:
    return letter_scores[you] + fights[enemy][you]


def decode(line: str) -> Tuple[str, ...]:
    return tuple(map(str.rstrip, line.split(" ")))


def solve(f: TextIOWrapper):
    lines = f.readlines()
    # solve_p1(lines)
    solve_p2(lines)


def solve_p1(lines: list[str]):
    scores: list[int] = []
    for line in lines:
        enemy, you = decode(line)
        score = calc_score(enemy, you)
        scores.append(score)
    print(sum(scores))


def solve_p2(lines: list[str]):
    scores: list[int] = []
    for line in lines:
        enemy, your_strat = decode(line)
        you = strat_to_shape[enemy][your_strat]
        score = calc_score(enemy, you)
        scores.append(score)
    print(sum(scores))


if __name__ == "__main__":
    main()
