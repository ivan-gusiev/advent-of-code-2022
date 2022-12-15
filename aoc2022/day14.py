from aoc2022.advent import set_day_from_filename
from aoc2022.coords import Coords
from aoc2022.gif import initialize_gif, request_frame, save_gif
from aoc2022.grid import Grid, Viewport
from aoc2022.util import Input, Output, clean_lines
from PIL import ImageDraw


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            lines = clean_lines(f)
            solve_p1(lines)
            solve_p2(lines)


Path = list[Coords]
ORIGIN = Coords(500, 0)
SCALE = 1
COLORS = {
    "+": (127, 127, 255),
    ".": (0, 0, 50),
    "#": (255, 200, 50),
    "o": (160, 160, 180),
    "H": (255, 255, 255),
}


def view(grid: Grid[str]) -> Viewport[str]:
    return Viewport(grid, Coords(400, 0), 200, 200)


def draw_grid(grid: Grid[str], highlight: list[Coords] = [], snowflake_id=0):
    viewport = view(grid)
    if highlight and highlight[0].y > viewport.height:
        return

    if snowflake_id > 10 and snowflake_id % 10 != 0:
        return

    if snowflake_id > 100 and snowflake_id % 100 != 0:
        return

    if snowflake_id > 1000 and snowflake_id % 1000 != 0:
        return

    frame = request_frame()
    if not frame:
        return

    draw = ImageDraw.Draw(frame.image)
    draw.rectangle((0, 0, viewport.width, viewport.height), fill=COLORS["."])
    for x, y, sym in viewport.enumerate_all_cells():
        if Coords(x, y) + viewport.origin in highlight:
            sym = "H"
        if sym != ".":
            draw.point((x * SCALE, y * SCALE), fill=COLORS[sym])
        # draw.rectangle((x * SCALE, y * SCALE, (x + 1) * SCALE, (y + 1) * SCALE), fill=COLORS[sym])


def parse_line(line: str) -> Path:
    segments = line.split(" -> ")
    return [Coords.parse(seg) for seg in segments]


def build_paths(grid: Grid[str], paths: list[Path]):
    grid.set_by(ORIGIN, "+")

    for path in paths:
        for fr, to in zip(path, path[1:]):
            delta = (to - fr).rect_normalize()
            grid.set_by(fr, "#")
            while fr != to:
                fr += delta
                grid.set_by(fr, "#")


def simulate_snowflake(grid: Grid[str], snowflake_id: int) -> bool:
    snowflake = ORIGIN
    DOWN = Coords(0, 1)
    DLEFT = Coords(-1, 1)
    DRIGHT = Coords(1, 1)

    while snowflake.y < 499:
        draw_grid(grid, [snowflake], snowflake_id)
        test = snowflake + DOWN
        if grid.get_by(test) == ".":
            snowflake = test
            continue
        test = snowflake + DLEFT
        if grid.get_by(test) == ".":
            snowflake = test
            continue
        test = snowflake + DRIGHT
        if grid.get_by(test) == ".":
            snowflake = test
            continue
        grid.set_by(snowflake, "o")
        return True

    return False


def solve_p1(lines: list[str]):
    paths = [parse_line(line) for line in lines]
    grid = Grid(1000, 500, ".")
    viewport = view(grid)
    initialize_gif(viewport.width * SCALE, viewport.height * SCALE)

    print("building walls...")
    build_paths(grid, paths)

    print("simulating snowflakes")
    cont = True
    snowflake_count = 0
    while cont:
        cont = simulate_snowflake(grid, snowflake_count)
        snowflake_count += 1
        if snowflake_count % 10 == 0:
            print(f"simulated {snowflake_count} flakes...")

    print("drawing result...")
    draw_grid(grid)
    save_gif(Output.create(name="p1"), loop=0)
    print("p1", snowflake_count - 1)


def build_floor(grid: Grid[str]):
    max_y = 0
    for y in range(grid.height):
        if "#" in grid.row(y):
            max_y = y
    max_y += 2
    yrow = grid.row(max_y)
    for x in range(grid.width):
        yrow[x] = "#"


def solve_p2(lines: list[str]):
    paths = [parse_line(line) for line in lines]
    grid = Grid(1000, 500, ".")
    viewport = view(grid)
    initialize_gif(viewport.width * SCALE, viewport.height * SCALE)

    print("building walls...")
    build_paths(grid, paths)
    build_floor(grid)

    print("simulating snowflakes")
    snowflake_count = 0
    while grid.get_by(ORIGIN) != "o":
        simulate_snowflake(grid, snowflake_count)
        snowflake_count += 1
        if snowflake_count % 10 == 0:
            print(f"simulated {snowflake_count} flakes...")

    print("drawing result...")
    draw_grid(grid)
    save_gif(Output.create(name="p2"), loop=0)
    print("p2", snowflake_count)


if __name__ == "__main__":
    main()
