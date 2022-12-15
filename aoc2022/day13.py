from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, Output, clean_lines, split_by_newline
from dataclasses import dataclass
from functools import cmp_to_key, reduce
from io import TextIOWrapper
from itertools import zip_longest
from operator import mul
from typing import Any

import json


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            solve(f)


def solve(f: TextIOWrapper):
    lines = clean_lines(f)
    solve_p1(lines)
    solve_p2(lines)


@dataclass
class Const:
    val: int

    def __repr__(self) -> str:
        return str(self.val)


@dataclass
class Seq:
    items: list["Data"]

    def __repr__(self) -> str:
        return repr(self.items)


Data = Const | Seq


def parse_json(js: Any) -> Data:
    if isinstance(js, list):
        return Seq(list(map(parse_json, js)))
    else:
        return Const(int(js))


def parse_data(text: str) -> Data:
    js = json.loads(text)
    return parse_json(js)


def compare(lhs: Data, rhs: Data) -> int:
    match lhs, rhs:
        case Const(ln), Const(rn):
            return rn - ln
        case Const(_num), Seq(_vals):
            return compare(Seq([lhs]), rhs)
        case Seq(_vals), Const(_num):
            return compare(lhs, Seq([rhs]))
        case Seq(ls), Seq(rs):
            for l, r in zip_longest(ls, rs):
                match l, r:
                    case None, r:
                        return 1
                    case l, None:
                        return -1
                    case l, r:
                        comparison = compare(l, r)
                        if comparison == 0:
                            continue
                        return comparison
                return 0
    return 0


def solve_p1(lines: list[str]):
    pairs = split_by_newline(lines)
    indices = []
    for i, pair in enumerate(pairs):
        lhs = parse_data(pair[0])
        rhs = parse_data(pair[1])
        if compare(lhs, rhs) > 0:
            indices.append(i + 1)

    print("p1", indices, sum(indices))


def solve_p2(lines: list[str]):
    packets = [parse_data(line) for line in lines if line]
    dividers = [parse_data(divider) for divider in ["[[2]]", "[[6]]"]]
    packets.extend(dividers)
    packets.sort(key=cmp_to_key(compare), reverse=True)

    indices = []
    for i, p in enumerate(packets):
        if p in dividers:
            indices.append(i + 1)

    print("p2", indices, reduce(mul, indices))


if __name__ == "__main__":
    main()
