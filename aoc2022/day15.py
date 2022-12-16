from aoc2022.advent import set_day_from_filename
from aoc2022.coords import Coords
from aoc2022.util import Input, Output, clean_lines
from dataclasses import dataclass
from typing import Tuple


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            lines = clean_lines(f)
            solve_p1(lines)
            solve_p2(lines)


@dataclass
class Span:
    lo: int
    hi: int

    def __contains__(self, i: int) -> bool:
        return self.lo <= i < self.hi

    @classmethod
    def centered(cls, i: int, half_dist: int) -> "Span":
        return Span(i - half_dist, i + half_dist + 1)

    @classmethod
    def total_len(cls, spans: list["Span"]) -> int:
        spans = list(spans)
        spans.sort(key=lambda s: s.lo)
        highest = spans[0].lo - 1
        len = 0
        for span in spans:
            start = max(span.lo, highest)
            end = span.hi
            span_len = end - start
            len += max(0, span_len)
            highest = max(highest, end)
        return len

    @classmethod
    def total_len_bounded(cls, spans: list["Span"], lo: int, hi: int) -> int:
        spans = list(spans)
        spans.sort(key=lambda s: s.lo)
        highest = lo
        len = 0
        for span in spans:
            start = max(span.lo, highest)
            end = min(hi, span.hi)
            span_len = end - start
            len += max(0, span_len)
            highest = max(highest, end)
            if span.hi >= hi:
                break
        return len

    @classmethod
    def find_gap(cls, spans: list["Span"]) -> set[int]:
        all = set(range(4_000_000))
        impossible = set()
        for span in spans:
            spanset = set(range(span.lo, span.hi))
            impossible.update(spanset)
            print(span, len(spanset), len(impossible))
        return all - impossible


@dataclass
class Reading:
    sensor: Coords
    beacon: Coords
    distance: int

    def vert_span(self) -> Span:
        return Span.centered(self.sensor.y, self.distance)

    def hor_span(self, y: int) -> Span:
        hor_dist = max(0, self.distance - abs(self.sensor.y - y))
        if hor_dist < 0:
            return Span(0, 0)
        return Span.centered(self.sensor.x, hor_dist)

    @classmethod
    def create(cls, sensor: Coords, beacon: Coords) -> "Reading":
        return Reading(sensor, beacon, sensor.manhattan_distance(beacon))


def parse_line(line: str) -> Reading:
    template = (
        line.replace("Sensor at x=", "")
        .replace(" y=", "")
        .replace(": closest beacon is at x=", ",")
    )
    parts = list(map(int, template.split(",")))
    return Reading.create(Coords(parts[0], parts[1]), Coords(parts[2], parts[3]))


def solve_p1(lines: list[str]):
    readings = [parse_line(line) for line in lines]
    target_y = 10 if len(lines) < 15 else 2_000_000

    hor_spans = [reading.hor_span(target_y) for reading in readings]

    print("p1", Span.total_len(hor_spans) - 1)


def solve_p2(lines: list[str]):
    readings = [parse_line(line) for line in lines]
    target_y = 20 if len(lines) < 15 else 4_000_000

    # for y in range(target_y):
    #     hor_spans = [reading.hor_span(y) for reading in readings]
    #     total = Span.total_len_bounded(hor_spans, 0, 4_000_000)
    #     if y % 100_000 == 0:
    #         print(f"{y/4_000_000}%")
    #     if total != 4_000_000:
    #         print(y, total)

    y = 3411840
    hor_spans = [reading.hor_span(y) for reading in readings]
    x = list(Span.find_gap(hor_spans))[0]


    print("p2", x * 4_000_000 + y)


if __name__ == "__main__":
    main()
