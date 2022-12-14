from aoc2022.advent import current_day
from aoc2022.util import Output
from dataclasses import dataclass
from PIL import Image, ImageFont
from typing import Optional, Tuple

import os
import sys

GIF_FONT = ImageFont.truetype("./res/font.ttf")


class Colors:
    BACKGROUND = (0, 0, 100)
    HIGHLIGHT = (255, 0, 100)
    MAIN_FILL = (0, 255, 100)
    GREEN = (0, 255, 100)


@dataclass
class GifBuilder:
    id: int
    size: Tuple[int, int]
    images: list[Image.Image]


@dataclass
class FrameInfo:
    frame_number: int
    image: Image.Image


gif_counter: int = 0
current_builder: Optional[GifBuilder] = None


def is_drawing() -> bool:
    return "--paint" in sys.argv


def initialize_gif(width: int, height: int):
    global current_builder

    current_builder = None
    if not is_drawing():
        print("[VIS] Won't paint this time. Set the --paint flag to paint the gif.")
        return
    current_builder = GifBuilder(
        id=increment_gif_counter(), size=(width, height), images=[]
    )


def request_frame() -> Optional[FrameInfo]:
    global current_builder

    if not current_builder:
        return None

    img = Image.new("RGB", current_builder.size, "black")
    current_builder.images.append(img)
    frame_count = len(current_builder.images)
    if frame_count % 100 == 0:
        print(f"[VIS] Painted {frame_count} frames already.")
    return FrameInfo(frame_count, img)


def save_gif(output: Output, cleanup: bool = True, **kwargs):
    global current_builder
    if not current_builder:
        return

    if len(current_builder.images) < 1:
        print("[VIS] Skipping an attempt to save a gif with zero frames.")
        return

    path = output.request_path("gif")

    images = current_builder.images
    images[0].save(path, save_all=True, append_images=images[1:], **kwargs)
    print(f"[VIS] Saved {len(images)} images")

    if cleanup:
        current_builder = None


def current_gif_counter() -> int:
    global gif_counter
    return gif_counter


def increment_gif_counter() -> int:
    global gif_counter
    gif_counter += 1
    return gif_counter
