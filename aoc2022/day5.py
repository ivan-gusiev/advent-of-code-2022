from aoc2022.util import Input, split_by_newline
from io import TextIOWrapper

def main():
    input = Input(__file__)
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
    instructions = map(Instruction.parse, commands)
    for i in instructions:
        i.execute(stacks)
    
    result = ""
    for stack in stacks:
        result += stack[-1]

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

def initialize_stacks(first_line: str) -> list[list[str]]:
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
        for i in range(self.move_count):
            stacks[to].append(stacks[fr].pop())

    def execute_9001(self, stacks: list[list[str]]):
        fr = self.move_from - 1
        to = self.move_to - 1
        buffer = []
        for i in range(self.move_count):
            buffer.append(stacks[fr].pop())
        buffer.reverse()
        stacks[to].extend(buffer)

    @classmethod
    def parse(cls, line: str) -> 'Instruction':
        items = line.split(' ')
        return cls(int(items[3]), int(items[5]), int(items[1]))

if __name__ == '__main__':
    main()