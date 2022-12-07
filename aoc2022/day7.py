from aoc2022.advent import set_day_from_filename
from aoc2022.util import Input, clean_lines
from io import TextIOWrapper
from dataclasses import dataclass
from typing import Dict, Optional

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

@dataclass
class File:
    name: str
    size: int

@dataclass
class Folder:
    name: str
    parent: Optional['Folder']
    files: Dict[str, File]
    folders: Dict[str, 'Folder']
    size_estimate: Optional[int]

    @classmethod
    def init(cls, name: str, parent: Optional['Folder']) -> 'Folder':
        return cls(name, parent, {}, {}, None)
    
    @classmethod
    def root(cls) -> 'Folder':
        return cls.init("", None)

@dataclass
class Ls:
    pass

@dataclass
class Cd:
    name: str

Command = Ls | Cd

def solve_p1(lines: list[str]):
    root = replay_command_lines(lines)
    small_dirs = [dir.size_estimate for dir in all_dirs(root) if dir.size_estimate < 100_000]
    print("p1", sum(small_dirs))

def solve_p2(lines: list[str]):
    root = replay_command_lines(lines)
    total_size = 70_000_000
    needed_size = 30_000_000
    used_size = root.size_estimate or 0
    target_size = used_size + needed_size - total_size
    dirs = [dir for dir in all_dirs(root)]
    dirs.sort(key=lambda dir: dir.size_estimate)
    for d in dirs:
        if (d.size_estimate >= target_size):
            print("p2", d.name or "/", d.size_estimate)
            break


def parse_command(line: str) -> Optional[Command]:
    if not line.startswith('$'):
        return None

    parts = line.split(' ')[1:]
    return Ls if parts[0] == "ls" else Cd(parts[1])

def update_dir(cd: Folder, line: str):
    size_spec, name = line.split(' ')
    if size_spec == "dir":
        cd.folders[name] = Folder.init(name, cd)
    else:
        cd.files[name] = File(name, int(size_spec))

def replay_command_lines(lines: list[str]) -> Folder:
    root = Folder.root()
    cd = root
    for line in lines:
        match parse_command(line):
            case None:
                update_dir(cd, line)
            case Cd(".."):
                cd = cd.parent or root
            case Cd("/"):
                cd = root
            case Cd(target):
                cd = cd.folders[target]
            case Ls:
                pass
    estimate_size(root)
    return root

def estimate_size(folder: Folder):
    for child in folder.folders.values():
        estimate_size(child)
    
    size_files = sum([file.size for file in folder.files.values()]) 
    size_children = sum([child.size_estimate or 0 for child in folder.folders.values()])
    folder.size_estimate = size_files + size_children

def all_dirs(root: Folder) -> list[Folder]:
    def all_dirs_impl(cd: Folder, lst: list[Folder]):
        lst.append(cd)
        for child in cd.folders.values():
            all_dirs_impl(child, lst)
            
    result = []
    all_dirs_impl(root, result)
    return result

if __name__ == '__main__':
    main()