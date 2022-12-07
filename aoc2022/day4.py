from aoc2022.advent import set_day_from_filename
from aoc2022.gif import is_drawing
from aoc2022.util import Input, Output, clean_lines
from io import TextIOWrapper
from typing import Tuple
from PIL import Image

def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

class Range:
    l: int
    r: int

    def __init__(self, l, r):
        l, r = min(l, r), max(l, r)
        self.l = l
        self.r = r
    
    def __str__(self) -> str:
        return f"{self.l}-{self.r}"

    def __repr__(self) -> str:
        return f"{self.l}-{self.r}"
    
    def contains_range(self, other: 'Range') -> bool:
        return self.l <= other.l and self.r >= other.r
    
    def contains(self, id: int) -> bool:
        return self.l <= id <= self.r

    @classmethod
    def parse(cls, text: str) -> 'Range':
        ids = list(map(int, text.split('-')))
        return Range(ids[0], ids[1])

    @classmethod
    def contains_symmetrical(cls, lhs: 'Range', rhs: 'Range') -> bool:
        return lhs.contains_range(rhs) or rhs.contains_range(lhs)

    @classmethod
    def overlaps(cls, lhs: 'Range', rhs: 'Range') -> bool:
        return lhs.contains(rhs.l) or lhs.contains(rhs.l) or rhs.contains(lhs.l) or rhs.contains(lhs.r)


def line_to_ranges(line: str) -> Tuple[Range, Range]:
    chunks = line.split(',')
    ranges = list(map(Range.parse, chunks))
    return ranges[0], ranges[1]

def solve(f: TextIOWrapper):
    lines = clean_lines(f)
    solve_p1(lines)
    solve_p2(lines)
    if is_drawing():
        solve_image(lines)

def solve_p1(lines: list[str]):
    result = 0
    for line in lines:
        l, r = line_to_ranges(line)
        if Range.contains_symmetrical(l, r):
            result += 1
    print("p1", result)

def solve_p2(lines: list[str]):
    result = 0
    for line in lines:
        l, r = line_to_ranges(line)
        if Range.overlaps(l, r):
            result += 1
    print("p1", result)

def solve_image(lines: list[str]):
    ranges = list(map(line_to_ranges, lines))
    width = 10 if len(ranges) < 10 else 100
    img = Image.new( 'RGB', (width, len(lines)), "black")
    pixels = img.load() # type: ignore
    for y, therange in enumerate(ranges):
        l, r = therange
        for x in range(0, width):
            red = int(r.contains(x)) * 255
            green = int(l.contains(x)) * 255
            pixels[x, y] = (red, green, 100)
    img.save(Output.create(name="sections", extension="png").request_path())

if __name__ == '__main__':
    main()