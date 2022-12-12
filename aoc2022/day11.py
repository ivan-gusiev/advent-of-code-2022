from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, Output, clean_lines, split_by_newline
from dataclasses import dataclass
from functools import reduce
from io import TextIOWrapper
from operator import mul

import sys

DEBUG = False
INFO = False
SUMMARY = True


sys.set_int_max_str_digits(100000)

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
class EOld:
    def eval(self, old: int) -> int:
        return old

    def __repr__(self) -> str:
        return "old"


@dataclass
class EConst:
    value: int

    def eval(self, _: int) -> int:
        return self.value

    def __repr__(self) -> str:
        return str(self.value)


@dataclass
class EAdd:
    lhs: "Expr"
    rhs: "Expr"

    def eval(self, old: int) -> int:
        return self.lhs.eval(old) + self.rhs.eval(old)

    def __repr__(self) -> str:
        return f"{self.lhs} + {self.rhs}"


@dataclass
class EMul:
    lhs: "Expr"
    rhs: "Expr"

    def eval(self, old: int) -> int:
        return self.lhs.eval(old) * self.rhs.eval(old)

    def __repr__(self) -> str:
        return f"{self.lhs} * {self.rhs}"


Expr = EOld | EConst | EAdd | EMul


def parse_expr(expr: str) -> Expr:
    def parse_sub(expr: str) -> Expr:
        match expr.strip():
            case "old":
                return EOld()
            case x:
                return EConst(int(x))

    subs = expr.replace("new = ", "").strip().split(" ")
    lhs = parse_sub(subs[0])
    rhs = parse_sub(subs[2])
    match subs[1]:
        case "*":
            return EMul(lhs, rhs)
        case "+":
            return EAdd(lhs, rhs)
    assert False, "no more expresssions known"


@dataclass
class Monkey:
    id: int
    items: list[int]
    op: Expr
    test_num: int
    true_monkey: int
    false_monkey: int
    total_inspected: int

    def __repr__(self) -> str:
        return f"""Monkey {self.id}:
  Starting items: {self.items}
  Operation: {self.op}
  Test: divisible by {self.test_num}
    If true: throw to monkey {self.true_monkey}
    If false: throw to monkey {self.false_monkey}"""

    @classmethod
    def parse(cls, line: list[str]) -> "Monkey":
        id = int(line[0].replace("Monkey ", "").replace(":", "").strip())
        items = [
            int(itm.strip())
            for itm in line[1].replace("Starting items:", "").split(",")
        ]
        op = parse_expr(line[2].replace("Operation: ", "".strip()))
        test_num = int(line[3].replace("Test: divisible by", "").strip())
        tmonkey = int(line[4].replace("If true: throw to monkey", "").strip())
        fmonkey = int(line[5].replace("If false: throw to monkey", "").strip())
        return Monkey(id, items, op, test_num, tmonkey, fmonkey, 0)


def dbg(indent: int, text: str):
    print(" " * indent + text) if DEBUG else None


def inf(indent: int, text: str):
    print(" " * indent + text) if INFO else None


def smr(indent: int, text: str):
    print(" " * indent + text) if SUMMARY else None


def solve_p1(lines: list[str]):
    monkeys = list(map(Monkey.parse, split_by_newline(lines)))

    for round in range(1, 21):
        inf(0, f"-------- ROUND {round} --------")
        for monkey in monkeys:
            dbg(0, f"Monkey {monkey.id}")
            for item in monkey.items:
                dbg(2, f"Monkey inspects an item with a worry level of {item}.")
                new_worry = monkey.op.eval(item)
                dbg(4, f"Worry level is updated to {new_worry}.")
                after_exam = new_worry // 3
                dbg(
                    4,
                    f"Monkey gets bored with item. Worry level is divided by 3 to {after_exam}.",
                )
                is_divisible = after_exam % monkey.test_num == 0
                dbg(
                    4,
                    f"Current worry level is {'' if is_divisible else 'not '}divisible by {monkey.test_num}.",
                )
                target_id = monkey.true_monkey if is_divisible else monkey.false_monkey
                dbg(
                    4,
                    f"Item with worry level {after_exam} is thrown to monkey {target_id}.",
                )
                monkeys[target_id].items.append(after_exam)
                monkey.total_inspected += 1
            monkey.items = []
        inf(
            0,
            f"After round {round}, the monkeys are holding items with these worry levels:",
        )
        for monkey in monkeys:
            inf(0, f"Monkey {monkey.id}: {', '.join(map(str, monkey.items))}")

    busiest_monkeys = [
        monkey.id
        for monkey in sorted(monkeys, key=lambda m: m.total_inspected, reverse=True)[
            0:2
        ]
    ]
    for monkey in monkeys:
        smr(
            0,
            f"Monkey {monkey.id} inspected items {monkey.total_inspected} times. {'*' if monkey.id in busiest_monkeys else ''}",
        )
    monkey_business = reduce(mul, [monkeys[i].total_inspected for i in busiest_monkeys])
    smr(0, f"monkey business: {monkey_business}")

    print("p1", monkey_business)


def solve_p2(lines: list[str]):
    monkeys = list(map(Monkey.parse, split_by_newline(lines)))
    super_mod: int = reduce(mul, [monkey.test_num for monkey in monkeys])

    for round in range(1, 10001):
        inf(0, f"-------- ROUND {round} --------")
        for monkey in monkeys:
            dbg(0, f"Monkey {monkey.id}")
            for item in monkey.items:
                dbg(2, f"Monkey inspects an item with a worry level of {item}.")
                new_worry = monkey.op.eval(item)
                dbg(4, f"Worry level is updated to {new_worry}.")
                is_divisible = new_worry % monkey.test_num == 0
                dbg(
                    4,
                    f"Current worry level is {'' if is_divisible else 'not '}divisible by {monkey.test_num}.",
                )
                target_id = monkey.true_monkey if is_divisible else monkey.false_monkey
                dbg(
                    4,
                    f"Item with worry level {new_worry} is thrown to monkey {target_id}.",
                )
                monkeys[target_id].items.append(new_worry % super_mod)
                monkey.total_inspected += 1
            monkey.items = []
        inf(
            0,
            f"After round {round}, the monkeys are holding items with these worry levels:",
        )
        for monkey in monkeys:
            inf(0, f"Monkey {monkey.id}: {', '.join(map(str, monkey.items))}")

    busiest_monkeys = [
        monkey.id
        for monkey in sorted(monkeys, key=lambda m: m.total_inspected, reverse=True)[
            0:2
        ]
    ]
    for monkey in monkeys:
        smr(
            0,
            f"Monkey {monkey.id} inspected items {monkey.total_inspected} times. {'*' if monkey.id in busiest_monkeys else ''}",
        )
    monkey_business = reduce(mul, [monkeys[i].total_inspected for i in busiest_monkeys])
    smr(0, f"monkey business: {monkey_business}")

    print("p2", monkey_business)


if __name__ == "__main__":
    main()
