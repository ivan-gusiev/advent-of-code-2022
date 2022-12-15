from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(eq=True, frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coords") -> "Coords":
        return Coords(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def abs(self) -> "Coords":
        return Coords(abs(self.x), abs(self.y))

    def manhattan_distance(self, other: "Coords") -> int:
        diff = (other - self).abs()
        return diff.x + diff.y

    def rect_normalize(self) -> "Coords":
        abs = self.abs()
        return Coords(self.x // (abs.x or 1), self.y // (abs.y or 1))

    def rect_distance(self, other: "Coords") -> int:
        diff = (other - self).abs()
        return max(diff.x, diff.y)

    @classmethod
    def parse(cls, text: str) -> "Coords":
        xs, ys = text.split(",")
        return Coords(int(xs), int(ys))


COMMAND_CARD: Dict[str, Coords] = {
    "L": Coords(-1, 0),
    "R": Coords(1, 0),
    "U": Coords(0, -1),
    "D": Coords(0, 1),
}

UN_COMMAND_CARD: Dict[Coords, str] = {
    Coords(-1, 0): "L",
    Coords(1, 0): "R",
    Coords(0, -1): "U",
    Coords(0, 1): "D",
}

ARROW: Dict[Coords, str] = {
    Coords(-1, 0): "←",
    Coords(1, 0): "→",
    Coords(0, -1): "↑",
    Coords(0, 1): "↓",
}
