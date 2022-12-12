from aoc2022.advent import set_day_from_filename
from aoc2022.coords import Coords, ARROW
from aoc2022.grid import Grid
from aoc2022.util import Input, Output, Raw, clean_lines
from dataclasses import dataclass
from functools import partial
import igraph as ig
from io import TextIOWrapper


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
class Cell:
    symbol: str
    elevation: int
    possible_directions: list[str]

    def __repr__(self) -> str:
        return self.symbol

    @classmethod
    def from_char(cls, char: str) -> "Cell":
        smb = char
        realchar = "a" if char == "S" else ("z" if char == "E" else char)
        elev = ord(realchar) - ord("a")
        return Cell(smb, elev, [])


def reachable(main: Cell, test: Cell) -> bool:
    return test.elevation <= main.elevation + 1


def all_reachable_neighbors(terrain: Grid[Cell], x: int, y: int) -> list[Coords]:
    cell = terrain[x, y]
    coords = Coords(x, y)
    result = []
    for nx, ny, n in terrain.enumerate_neighbors(x, y):
        ncoords = Coords(nx, ny)
        if ncoords.manhattan_distance(coords) == 1 and reachable(cell, n):
            result.append(ncoords)
    # print(f"{terrain.indexof(x, y)}: ({x},{y}): {[terrain.indexof(r.x, r.y) for r in result]}")
    return result


def visualize_path(terrain: Grid[Cell], path: list[int]):
    solution = terrain.map(lambda x: Raw("."))
    for f, t in zip(path, path[1:]):
        x, y, _ = terrain.indexed(f)
        tx, ty, _ = terrain.indexed(t)
        solution[x, y] = (
            Raw("*") if f == path[0] else Raw(ARROW[Coords(tx, ty) - Coords(x, y)])
        )
    print(solution)
    print()


def solve_p1(lines: list[str]):
    terrain = Grid.from_lines(lines).map(Cell.from_char)
    start = [
        Coords(x, y)
        for x, y, cell in terrain.enumerate_all_cells()
        if cell.symbol == "S"
    ][0]
    end = [
        Coords(x, y)
        for x, y, cell in terrain.enumerate_all_cells()
        if cell.symbol == "E"
    ][0]

    edges = [
        (terrain.indexof(x, y), terrain.indexof(n.x, n.y))
        for x, y, _ in terrain.enumerate_all_cells()
        for n in all_reachable_neighbors(terrain, x, y)
    ]

    g = ig.Graph(terrain.width * terrain.height, edges, directed=True)
    paths = g.get_shortest_paths(
        terrain.indexof(start.x, start.y), to=terrain.indexof(end.x, end.y), mode="out"
    )

    visualize_path(terrain, paths[0])

    print("p1", len(paths[0]) - 1)


def solve_p2(lines: list[str]):
    terrain = Grid.from_lines(lines).map(Cell.from_char)
    start = [
        Coords(x, y)
        for x, y, cell in terrain.enumerate_all_cells()
        if cell.symbol == "S"
    ][0]
    end = [
        Coords(x, y)
        for x, y, cell in terrain.enumerate_all_cells()
        if cell.symbol == "E"
    ][0]

    edges = [
        (terrain.indexof(x, y), terrain.indexof(n.x, n.y))
        for x, y, _ in terrain.enumerate_all_cells()
        for n in all_reachable_neighbors(terrain, x, y)
    ]

    g = ig.Graph(terrain.width * terrain.height, edges, directed=True)

    paths: list[list[int]] = g.get_shortest_paths(
        terrain.indexof(end.x, end.y), mode="in"
    )
    min_len = len(paths[0])
    for path in paths:
        path.reverse()
        if len(path) == 0:
            continue
        _, _, cell = terrain.indexed(path[0])
        if cell.elevation > 0:
            continue
        path_len = len(path) - 1
        if min_len > path_len:
            min_len = path_len

    print("p2", min_len)


if __name__ == "__main__":
    main()
