
from aoc2022.gif import request_frame
from PIL import ImageDraw
from typing import Any, Callable, Generator, Generic, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class Grid(Generic[T]):
    cells: list[list[T]]
    width: int
    height: int

    def __init__(self, width: int, height: int, zero: T):
        self.width = width
        self.height = height
        self.cells = [[zero for _ in range(width)] for _ in range(height)]

    def __getitem__(self, coord: Tuple[int, int]):
        x, y = coord
        return self.cells[y][x]

    def __setitem__(self, coord: Tuple[int, int], value: T):
        x, y = coord
        self.cells[y][x] = value

    def __repr__(self) -> str:
        return "\n".join(
            [
                "".join([repr(self[x, y]) for x in range(self.width)])
                for y in range(self.height)
            ]
        )

    def row(self, y: int) -> list[T]:
        return self.cells[y]

    def col(self, x: int) -> list[T]:
        return [self[x, y] for y in range(self.height)]

    def all_cells(self) -> list[T]:
        return [value for _, _, value in self.enumerate_all_cells()]
    
    def enumerate_all_cells(self) -> Generator[Tuple[int, int, T], None, None]:
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, self[x, y])

    def map(self, mapper: Callable[[T], U]) -> 'Grid[U]':
        new_grid = Grid[U](self.width, self.height, mapper(self[0, 0]))
        for x, y, value in self.enumerate_all_cells():
            new_grid[x, y] = mapper(value)
        return new_grid
    
    def img_get_size(self, scale: int = 1) -> Tuple[int, int]:
        return self.width * scale, self.height * scale

    def img_draw(self, color_map: Callable[[int, int, T], Any], scale: int = 1):
        frame_info = request_frame()
        if not frame_info:
            return
        
        img = frame_info.image
        draw = ImageDraw.Draw(img)
        for x, y, val in self.enumerate_all_cells():
            coords = (x * scale, y * scale), (x * scale + scale, y * scale + scale)
            draw.rectangle(coords, fill=color_map(x, y, val))

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Grid[str]":
        assert len(lines) > 0

        height = len(lines)
        width = len(lines[0])
        grid = Grid(width, height, "")

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                grid[x, y] = char

        return grid
