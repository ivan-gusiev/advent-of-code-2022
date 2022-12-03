import os.path
from io import TextIOWrapper
from pathlib import Path

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

class Input:
    challenge_path: str
    test_path: str

    def __init__(self, current_file: str):
        """
        Send a message to a recipient.

        :param str current_file: always put __file__ there
        """
        filename = f"input/{os.path.basename(current_file)}"
        challenge_path = str(Path(filename).with_suffix(".txt"))
        self.test_path = challenge_path.replace(".txt", "-test.txt")
        self.challenge_path = challenge_path

    def challenge_path(self) -> str:
        return self.challenge_path

    def test_path(self) -> str:
        return self.test_path