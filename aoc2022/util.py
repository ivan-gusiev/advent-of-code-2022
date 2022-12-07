import os.path
from aoc2022.advent import current_day, day_from_filename
from io import TextIOWrapper
from pathlib import Path
from typing import TypeVar

def clean_lines(f: TextIOWrapper) -> list[str]:
    return list(map(str.rstrip, f.readlines()))

def split_by_newline(lines: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        line = line.rstrip()
        if not line:
            result.append(current)
            current = []
        else:
            current.append(line)
    if current != []:
        result.append(current)
    return result

T = TypeVar('T')
def split_to_chunks(lines: list[T], n) -> list[list[T]]:
    result: list[list[T]] = []
    for i in range(0, len(lines), n):
        result.append(lines[i:i + n])
    return result

class Input:
    challenge_path: str
    test_path: str
    day: str

    def __init__(self, day_num: int):
        """
        Send a message to a recipient.

        :param str current_file: always put __file__ there
        """
        self.day = f"day{day_num}"
        self.test_path = f"input/day{day_num}-test.txt"
        self.challenge_path = f"input/day{day_num}.txt"

    @classmethod
    def for_advent(cls) -> 'Input':
        return cls(current_day())
    
    @classmethod
    def from_filename(cls, filename: str) -> 'Input':
        return cls(day_from_filename(filename))
