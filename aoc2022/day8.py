from aoc2022.advent import set_day_from_filename
from aoc2022.gif import initialize_gif, save_gif
from aoc2022.grid import Grid
from aoc2022.util import Input, Output, clean_lines
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Any, Iterable, Tuple

def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

def solve(f: TextIOWrapper):
    lines = clean_lines(f)
    solve_p1(lines)
    solve_p2(lines)

SCALE = 8

@dataclass
class Cell:
    value: int
    visible: bool
    score: int

    @classmethod
    def of_char(cls, char: str):
        return cls(int(char), False, 0)

def solve_p1(lines: list[str]):
    grid = Grid.from_lines(lines).map(Cell.of_char)
    initialize_gif(*grid.img_get_size(scale=SCALE))

    for y in range(grid.height):
        row = grid.row(y)
        process_visibility(row)
        process_visibility(reversed(row))

    for x in range(grid.width):
        col = grid.col(x)
        process_visibility(col)
        process_visibility(reversed(col))

    if grid.height < 10:
        draw_grid_visibility(grid)

    grid.img_draw(visibility_color_map, scale=SCALE)

    print("p1", len([c for c in grid.all_cells() if c.visible]))
    save_gif(Output.create(name="visibility"))

def solve_p2(lines: list[str]):
    grid = Grid.from_lines(lines).map(Cell.of_char)
    initialize_gif(*grid.img_get_size(scale=SCALE))

    for x, y, cell in grid.enumerate_all_cells():
        u, d = calculate_view(grid.col(x), y)
        l, r = calculate_view(grid.row(y), x)
        cell.score = u * d * l * r

    grid.img_draw(score_color_map, scale=SCALE)
    scores = grid.map(lambda c : c.score)

    if scores.height < 10:
        print(scores)
    print("p2", max(scores.all_cells()))
    save_gif(Output.create(name="scores"))

def process_visibility(cells: Iterable[Cell]):
    cur_height = -1
    for c in cells:
        if c.value > cur_height:
            c.visible = True
            cur_height = c.value

def calculate_view(cells: list[Cell], pos: int) -> Tuple[int, int]:
    cell_height = cells[pos].value
    l_distance = 0
    for i in range(pos - 1, -1, -1):
        cell = cells[i]
        l_distance += 1
        if cell.value >= cell_height:
            break

    cell_height = cells[pos].value
    r_distance = 0
    for i in range(pos + 1, len(cells)):
        cell = cells[i]
        r_distance += 1
        if cell.value >= cell_height:
            break
    return l_distance, r_distance


class bcolors:
    LITE = '\033[97m'
    DARK = '\033[94m'
    ENDC = '\033[0m'

def draw_grid_visibility(grid: Grid[Cell]):
    current_row = 0
    current_text = ""
    for _, y, cell in grid.enumerate_all_cells():
        if y > current_row:
            print(current_text)
            current_text = ""
            current_row = y
        if cell.visible:
            current_text += f"{bcolors.LITE}{cell.value}{bcolors.ENDC}"
        else:
            current_text += f"{bcolors.DARK}{cell.value}{bcolors.ENDC}"
    print(current_text)

def visibility_color_map(x: int, y: int, z: Cell) -> Any:
    intensity = z.value * 12 # 0-120
    #return (intensity + 120, intensity + 120, intensity) if z.visible else (intensity // 4 * 3, (intensity + 120) // 4 * 3, intensity // 4 * 3)
    return (intensity, intensity + 120, intensity) if z.visible else (intensity // 4 * 3 + 40, intensity // 4 * 3 + 70, intensity // 4 * 3 + 40)

def score_color_map(x: int, y: int, z: Cell) -> Any:
    height_intensity = int((z.value / 10) * 64)
    score_intensity = int((z.score / 315495) * 192)
    return (height_intensity + score_intensity, height_intensity + score_intensity, height_intensity // 2)

if __name__ == '__main__':
    main()