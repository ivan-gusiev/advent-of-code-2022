from aoc2022.advent import set_day_from_filename
from aoc2022.gif import initialize_gif, request_frame, save_gif, GIF_FONT
from aoc2022.util import Input, clean_lines
from io import TextIOWrapper
from typing import Set, Tuple

def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path, input.challenge_path]:
        print("input:", file)
        with open(file, mode='r') as f:
            solve(f)

def solve(f: TextIOWrapper):
    line = f.read()
    solve_p1(line)
    solve_p2(line)

def solve_p1(line: str):
    print("p1", get_message_start(4, line))

def solve_p2(line: str):
    print("p2", get_message_start(14, line))

def get_message_start(chunk_size: int, line: str) -> int:
    initialize_marker_gif(len(line))
    result = -1
    draw_state(line, set())
    for i in range(len(line)):
        l, r = chunk_range(i, chunk_size)
        draw_state(line, set(range(l, r + 1)))
        chunk = line[l:r]
        if len(set(chunk)) == chunk_size:
            result = i
            break
    
    draw_state(line, set(range(l + 1, r + 2)))
    draw_state(line, set(range(l + 1, r + 2)))
    save_gif(f"chunk_{chunk_size}", loop=0, duration=25)
    return result

def chunk_range(i: int, size: int) -> Tuple[int, int]:
    return max(0, i-size), i

# --------- DRAWING ---------

from PIL import ImageDraw
import math

#sizes
BOX_WIDTH = 10
BOX_HEIGHT = 10
BORDER = 5
MARGIN = 5

# colors
BACKGROUND = (0, 0, 50)
HIGHLIGHT = (255, 0, 100)
MAIN_FILL = (0, 255, 100)
SCAN = (255, 255, 255)
GREEN = (0, 255, 100)

def table_size(num_chars: int) -> Tuple[int, int]:
    cols = int(math.sqrt(num_chars)) + 1 # make it square, bias to horizontal
    rows = int(num_chars/cols) + 2
    return cols, rows

def initialize_marker_gif(num_chars: int):
    cols, rows = table_size(num_chars)
    width = BORDER * 2 + MARGIN * (cols - 1) + BOX_WIDTH * cols
    height = BORDER * 2 + MARGIN * (rows - 1) + BOX_WIDTH * rows
    initialize_gif(width, height)

def draw_state(text: str, scan_range: Set[int]):
    frame_info = request_frame()
    if not frame_info:
        return

    print("frame", frame_info.frame_number)
    img = frame_info.image
    img_w, img_h = img.size
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 0), (img_w, img_h)), BACKGROUND)

    letters = list(map(lambda i: text[i], scan_range))
    dupes = set()
    for letter in letters:
        if letters.count(letter) > 1:
            dupes.add(letter)

    cols, rows = table_size(len(text))
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if len(text) <= index:
                break
            x = BORDER + MARGIN * col + BOX_WIDTH * col
            y = BORDER + MARGIN * row + BOX_HEIGHT * row
            letter = text[index]
            if index in scan_range:
                color = HIGHLIGHT if letter in dupes else SCAN
            else:
                color = MAIN_FILL
            draw.text(
                (x, y), 
                letter.upper(),
                font=GIF_FONT,
                fill=color)

    # frame counter
    draw.text(
        (BORDER, img_h - BORDER - BOX_HEIGHT), 
        str(frame_info.frame_number), 
        font=GIF_FONT, 
        fill=GREEN)

if __name__ == '__main__':
    main()