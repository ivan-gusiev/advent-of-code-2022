from aoc2022.advent import set_day_from_filename
from aoc2022.gif import initialize_gif, request_frame, save_gif, Colors
from aoc2022.grid import Grid
from aoc2022.util import Input, Output, clean_lines
from dataclasses import dataclass
from functools import reduce
from io import TextIOWrapper
from operator import add
from typing import Tuple

WIDTH: int = 40
HEIGHT: int = 6
TOTAL_CELLS: int = WIDTH * HEIGHT
SCALE = 4
HMARGIN = 12


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            solve(f)


@dataclass
class Noop:
    cycles: int = 1


@dataclass
class Addx:
    amount: int
    cycles: int = 2


Instruction = Noop | Addx


def parse_instruction(line: str) -> Instruction:
    match line.split(" "):
        case ["noop"]:
            return Noop()
        case ["addx", amount]:
            return Addx(int(amount))
        case arr:
            raise Exception(f"cannot parse [{arr}] as an instruction")


def solve(f: TextIOWrapper):
    lines = clean_lines(f)
    solve_p1(lines)
    solve_p2(lines)


def state(cycle: int, rx: int) -> str:
    return f"cycle {cycle}, rx {rx}"


def increment_cycle(cycle: int, rx: int, samples: list[Tuple[int, int]]) -> int:
    cycle += 1
    if (cycle - 20) % 40 == 0:
        samples.append((cycle, rx))
    return cycle


def color_map(_x: int, _y: int, char: str) -> Tuple[int, int, int]:
    return Colors.HIGHLIGHT if char == "#" else Colors.BACKGROUND


def draw_display(display: Grid[str], display_frame: int):
    drw = display.img_draw(color_map, SCALE)
    if drw:
        drw.text((1, HEIGHT * SCALE + 1), str(display_frame), fill=Colors.GREEN)


def update_display(cycle: int, rx: int, display: Grid[str]):
    idx, pos = divmod(cycle - 1, TOTAL_CELLS)
    row, col = divmod(pos, WIDTH)

    if pos == 0:
        draw_display(display, idx)

    if rx - 1 <= col <= rx + 1:
        display[col, row] = "#"
    else:
        display[col, row] = "."


def solve_p1(lines: list[str]):
    instructions = [parse_instruction(line) for line in lines]
    rx = 1
    cycle = 1
    samples: list[Tuple[int, int]] = []

    for instruction in instructions:
        wait = instruction.cycles
        while wait >= 1:
            wait -= 1
            if wait == 0:
                match instruction:
                    case Addx(amount=n):
                        rx += n
            cycle = increment_cycle(cycle, rx, samples)

    print("p1", reduce(add, ([cycle * x for cycle, x in samples if 19 < cycle < 221])))


def solve_p2(lines: list[str]):
    instructions = [parse_instruction(line) for line in lines]
    rx = 1
    cycle = 1
    display = Grid[str](WIDTH, HEIGHT, ".")
    samples: list[Tuple[int, int]] = []
    initialize_gif(WIDTH * SCALE, HEIGHT * SCALE + HMARGIN)

    for instruction in instructions:
        wait = instruction.cycles
        while wait >= 1:
            update_display(cycle, rx, display)
            wait -= 1
            if wait == 0:
                match instruction:
                    case Addx(amount=n):
                        rx += n
            cycle = increment_cycle(cycle, rx, samples)

    draw_display(display, 1)
    save_gif(Output.create(name="display"))


if __name__ == "__main__":
    main()
