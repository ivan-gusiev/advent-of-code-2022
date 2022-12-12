from aoc2022.advent import set_day_from_filename
from aoc2022.coords import Coords, COMMAND_CARD
from aoc2022.gif import initialize_gif, request_frame, save_gif, Colors
from aoc2022.util import Input, Output, clean_lines
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Dict, Tuple


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


def solve_p1(lines: list[str]):
    commands = "".join(
        [parts[0] * int(parts[1]) for parts in [line.split(" ") for line in lines]]
    )
    head = tail = Coords(0, 0)
    tail_history = []

    for cmd in commands:
        tail_history.append(tail)

        head += COMMAND_CARD[cmd]

        if head.rect_distance(tail) > 1:
            tail += (head - tail).rect_normalize()

    draw_final_positions("p1", tail_history)
    print("p1", head, tail, len(set(tail_history)))


def solve_p2(lines: list[str]):
    commands = "".join(
        [parts[0] * int(parts[1]) for parts in [line.split(" ") for line in lines]]
    )

    rope = [Coords(0, 0) for _ in range(10)]
    tail_history = []

    for cmd in commands:
        tail_history.append(rope[-1])

        rope[0] += COMMAND_CARD[cmd]

        for i, (hd, tl) in enumerate(zip(rope, rope[1:])):
            if hd.rect_distance(tl) > 1:
                rope[1 + i] += (hd - tl).rect_normalize()

    draw_final_positions("p2", tail_history)
    print("p2", len(set(tail_history)))


def output_map(points: list[Tuple[str, Coords]], size: Tuple[Coords, Coords]):
    c0, c1 = size
    for y in range(min(c0.y, c1.y), max(c0.y, c1.y) + 1):
        row = ""
        for x in range(min(c0.x, c1.x), max(c0.x, c1.x) + 1):
            c = Coords(x, y)
            letter = "."
            if c == Coords(0, 0):
                letter = "s"
            for label, target in points:
                if c == target:
                    letter = label
            row += letter
        print(row)
    print()


def output_final_positions(history: list[Coords]):
    positions = set(history)
    for y in range(min([t.y for t in history]), max([t.y for t in history]) + 1):
        row = ""
        for x in range(min([t.x for t in history]), max([t.x for t in history]) + 1):
            row += "#" if Coords(x, y) in positions else "."
        print(row)
    print()


def draw_final_positions(part: str, history: list[Coords]):
    l, r = min([t.x for t in history]), max([t.x for t in history])
    u, d = min([t.y for t in history]), max([t.y for t in history])
    width = r - l + 1
    height = d - u + 1
    initialize_gif(width, height)

    frame = request_frame()
    if not frame:
        return

    positions = set(history)
    img = frame.image
    pixels = img.load()  # type: ignore
    for y in range(img.height):
        for x in range(img.width):
            sx, sy = x + l, y + u
            pixels[x, y] = (
                Colors.GREEN if Coords(sx, sy) in positions else Colors.BACKGROUND
            )
            if Coords(sx, sy).rect_distance(Coords(0, 0)) < 2:
                pixels[x, y] = Colors.HIGHLIGHT

    save_gif(Output.create(name=f"{part}_tail"))


if __name__ == "__main__":
    main()
