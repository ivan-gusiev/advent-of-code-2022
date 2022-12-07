from aoc2022.advent import set_day_from_filename
from aoc2022.gif import initialize_gif, request_frame, save_gif, GIF_FONT
from aoc2022.util import Input, Output, split_by_newline
from io import TextIOWrapper
from PIL import ImageDraw
from typing import Any

#sizes
BOX_WIDTH = 10
BOX_HEIGHT = 7
ADJUST_X = 3
ADJUST_Y = -2
BORDER = 5

# colors
BACKGROUND = (0, 0, 100)
HIGHLIGHT = (255, 0, 100)
MAIN_FILL = (0, 255, 100)
GREEN = (0, 255, 100)

def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

def solve(f: TextIOWrapper):
    lines = f.readlines()
    solve_p1(lines)
    solve_p2(lines)

def solve_p1(lines: list[str]):
    stacks = initialize_stacks(lines[0])
    data, commands = split_by_newline(lines)
    load_stacks(data, stacks)
    initialize_images(stacks)
    instructions = map(Instruction.parse, commands)
    draw_stacks(stacks)
    for i in instructions:
        i.execute(stacks)
        draw_stacks(stacks)
    
    result = ""
    for stack in stacks:
        result += stack[-1]

    save_gif(Output.create(name="p1"), loop=0, duration=25)
    print("p1", result)

def solve_p2(lines: list[str]):
    stacks = initialize_stacks(lines[0])
    data, commands = split_by_newline(lines)
    load_stacks(data, stacks)
    instructions = map(Instruction.parse, commands)
    for i in instructions:
        i.execute_9001(stacks)
    
    result = ""
    for stack in stacks:
        result += stack[-1]

    print("p2", result)

def initialize_stacks(first_line: str) -> list[list[Any]]:
    col_width = len(first_line)
    stack_count = int(col_width / 4)
    return list(map(lambda _: [], range(0, stack_count)))

def load_stacks(data: list[str], stacks: list[list[str]]):
    data.reverse()
    for line in data[1:]:  #  the first line is indices
        for x, stack in enumerate(stacks):
            index = 4 * x + 1
            if len(line) <= index:
                break
            letter = line[index]
            if letter and letter != ' ':
                stack.append(letter)

def initialize_images(stacks: list[list[Any]]):
    columns = len(stacks)
    rows = max(map(len, stacks)) * 5  # 5 times max size for safety (not enough tho)
    image_width = BORDER + columns * (BOX_WIDTH + BORDER)
    image_height = (rows + 2) * (BOX_HEIGHT + BORDER)
    initialize_gif(image_width, image_height)

def draw_stacks(stacks: list[list[str]], highlights = None):
    frame_info = request_frame()

    if not frame_info:
        return

    img = frame_info.image
    img_w, img_h = img.size
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 0), (img_w, img_h)), BACKGROUND)

    if highlights == None:
        highlights = set()

    for col, stack in enumerate(stacks):
        for row, letter in enumerate(stack):
            x0 = BORDER + (BOX_WIDTH + BORDER) * col
            y0 = img_h - (BORDER + (BOX_HEIGHT + BORDER) * (row + 2))
            x1 = x0 + BOX_WIDTH
            y1 = y0 + BOX_HEIGHT
            color = HIGHLIGHT if (col, row) in highlights else MAIN_FILL
            draw.rectangle(((x0, y0), (x1, y1)), color)
            draw.text(
                (x0 + ADJUST_X, y0 + ADJUST_Y), 
                letter, 
                BACKGROUND)
    
    draw.text(
        (BORDER, img_h - BORDER - BOX_HEIGHT), 
        str(frame_info.frame_number), 
        font=GIF_FONT, 
        fill=GREEN)

class Instruction:
    move_from: int
    move_to: int
    move_count: int

    def __init__(self, f: int, t: int, c: int):
        self.move_from = f
        self.move_to = t
        self.move_count = c
    
    def execute(self, stacks: list[list[str]]):
        fr = self.move_from - 1
        to = self.move_to - 1
        remlen = len(stacks[fr])
        addlen = len(stacks[to])
        highlights = set(map(lambda y: (fr, y), range( remlen - self.move_count, remlen)))
        highlights.update(map(lambda y: (to, y), range( addlen, addlen + self.move_count)))
        for i in range(self.move_count):
            stacks[to].append(stacks[fr].pop())
            draw_stacks(stacks, highlights)

    def execute_9001(self, stacks: list[list[str]]):
        fr = self.move_from - 1
        to = self.move_to - 1
        buffer = []
        for _ in range(self.move_count):
            buffer.append(stacks[fr].pop())
            draw_stacks(stacks)
        buffer.reverse()
        stacks[to].extend(buffer)
        draw_stacks(stacks)

    @classmethod
    def parse(cls, line: str) -> 'Instruction':
        items = line.split(' ')
        return cls(int(items[3]), int(items[5]), int(items[1]))

if __name__ == '__main__':
    main()