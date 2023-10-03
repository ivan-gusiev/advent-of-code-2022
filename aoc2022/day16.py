from aoc2022.advent import set_day_from_filename
from aoc2022.gif import is_drawing
from aoc2022.util import Input, Output, clean_lines
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Callable, Optional

import igraph as ig


def main():
    set_day_from_filename(__file__)
    input = Input.for_advent()
    for file in [input.test_path]: #, input.challenge_path]:
        print("input:", file)
        with open(file, mode="r") as f:
            lines = clean_lines(f)
            solve_p1(lines)
            solve_p2(lines)


@dataclass
class ValveInfo:
    id: int
    name: str
    flow_rate: int
    tunnels: list[str]

    @classmethod
    def parse(cls, id: int, text: str) -> "ValveInfo":
        text = text.replace("Valve ", "")
        text = text.replace(" has flow rate=", ",")
        text = text.replace("; tunnels lead to valve", ",")
        text = text.replace("; tunnel leads to valve", ",")
        text = text.replace("s ", "")
        text = text.replace(", ", ",")
        parts = text.split(",")
        return ValveInfo(id, parts[0], int(parts[1]), parts[2:])


@dataclass
class Cave:
    valves: list[ValveInfo]
    name_to_id: dict[str, int]

    def __getitem__(self, identifier: str | int) -> ValveInfo:
        match identifier:
            case int() as id:
                return self.valves[id]
            case str() as name:
                return self.valves[self.name_to_id[name]]

    @classmethod
    def create(cls, valves: list[ValveInfo]) -> "Cave":
        return Cave(valves, dict([(valve.name, valve.id) for valve in valves]))


@dataclass(frozen=True, eq=True)
class OpenValve:
    pass


@dataclass(frozen=True, eq=True)
class MoveTo:
    target: int


Action = OpenValve | MoveTo

def action_str(cave: Cave, action: Action) -> str:
    match action:
        case OpenValve():
            return "open valve"
        case MoveTo(id):
            return f"move to {cave[id].name}"

@dataclass
class Simulation:
    cave: Cave
    location: int
    open_valves: set[int]
    flow_rate: int
    pressure_relieved: int
    time_left: int

    def here(self) -> ValveInfo:
        return self.cave[self.location]

    def here_is_open(self) -> bool:
        return self.location in self.open_valves

    def is_open(self, valve: int | str) -> bool:
        return self.cave[valve].id in self.open_valves

    def execute_action(self, action: Action):
        here = self.here()
        print(action_str(self.cave, action))
        match action:
            case OpenValve() if here.id not in self.open_valves:
                self.open_valves.add(here.id)
                self.flow_rate += here.flow_rate
            case OpenValve():
                print(f"[WARN] Opening an already open valve {here.name}")
            case MoveTo(x) if self.cave[x].name in here.tunnels:
                self.location = x
            case MoveTo(x):
                raise Exception(f"Trying to go from {here.name} to {self.cave[x].name}")

    def pass_time(self) -> bool:
        self.pressure_relieved += self.flow_rate
        self.time_left -= 1
        return self.time_left > 0

    @classmethod
    def of_cave(cls, cave: Cave) -> "Simulation":
        return Simulation(cave, cave["AA"].id, set(), 0, 0, 30)


def dumb_strategy(sim: Simulation) -> Action:
    if not sim.here_is_open():
        return OpenValve()
    else:
        for neighbor_name in sim.here().tunnels:
            neighbor = sim.cave[neighbor_name]
            if neighbor.id not in sim.open_valves:
                return MoveTo(neighbor.id)
        return MoveTo(sim.cave[sim.here().tunnels[0]].id)

class SmarterStrategy:
    visited: set[int]

    def __init__(self):
        self.visited = set()

    def find_action(self, sim: Simulation) -> Action:
        def potential_flow(valve: str|int) -> int:
            return sim.cave[valve].flow_rate * (0 if sim.is_open(valve) else 1)

        def score(id: str|int) -> int:
            valve = sim.cave[id]
            result = potential_flow(id)
            if sim.is_open(id):
                result -= 100
            if valve.id in self.visited:
                result -= 100
            result += len(valve.tunnels)
            return result

        self.visited.add(sim.location)

        if potential_flow(sim.location) > 0:
            return OpenValve()
        else:
            tunnel_scores = [(tunnel, score(tunnel)) for tunnel in sim.here().tunnels]
            #print(tunnel_scores)
            best_tunnel, _ = max(tunnel_scores, key=lambda tup: tup[1])
            return MoveTo(sim.cave[best_tunnel].id)

def draw_cave(cave: Cave):
    if not is_drawing():
        return

    valves = cave.valves
    edges = [
        (valve.id, cave[neighbor].id) for valve in valves for neighbor in valve.tunnels
    ]
    g = ig.Graph(len(valves), edges, directed=True)
    g.vs["name"] = [valve.name for valve in valves]
    g.vs["flow"] = [valve.flow_rate for valve in valves]

    visual_style = {
        "vertex_size": 50,
        "vertex_color": ["pink" for _ in g.vs],
        "vertex_label": [f"{v.name}\n{v.flow_rate}" for v in valves],
        "layout": g.layout("kk"),
        "bbox": (1500, 1500),
        "margin": 20,
        "edge_curved": False,
        "textposition": "top center",
    }

    out = ig.plot(g, **visual_style)
    out.save(Output.create(name="p1_graph", extension="png").request_path())

def simulate(cave: Cave, strat: Callable[[Simulation], Action]) -> int:
    sim = Simulation.of_cave(cave)
    cont = True
    while cont:
        action = strat(sim)
        sim.execute_action(action)
        cont = sim.pass_time()

    return sim.pressure_relieved

@dataclass(eq=True, unsafe_hash=True)
class ActionTree:
    parent: Optional["ActionTree"] = field(hash=False)
    timeleft: int
    location: int
    visited: frozenset[int]
    opened: frozenset[int]
    
    def history(self) -> list["ActionTree"]:
        result = []
        cur: Optional[ActionTree] = self
        while cur:
            result.append(cur)
            cur = cur.parent
        result.reverse()
        return result

    def relieved(self, cave: Cave) -> int:
        result = 0
        for pt in self.history():
            result += sum(cave[op].flow_rate for op in pt.opened)
        return result

@cache
def make_child(node: ActionTree, action: Action) -> ActionTree:
    timeleft = node.timeleft - 1
    location = node.location
    visited = node.visited
    opened = node.opened

    match action:
        case OpenValve():
            opened = opened | frozenset([location])
        case MoveTo(x):
            location = x
            visited = visited | frozenset([location])

    return ActionTree(node, timeleft, location, visited, opened)

timeline = 0
max_relief = 0
best_history: Any = None

def tree_of_all_possible_moves(cave: Cave) -> ActionTree:
    global timeline, max_relief, best_history
    timeline = 0
    best_history = None
    max_relief = 0

    @cache
    def find_children(node: ActionTree):
        global timeline, max_relief, best_history
        children: dict[Action, ActionTree] = {}

        if node.timeleft == 0:
            timeline += 1
            relieved = node.relieved(cave)
            if relieved > max_relief:
                max_relief = relieved
                best_history = node.history()
            if timeline % 1000 == 0:
                print(f"{timeline} timelines calculated, max relief: {max_relief}")
                print(best_history)
            return children

        if node.location not in node.opened:
            if cave[node.location].flow_rate > 0:
                child = make_child(node, OpenValve())
                find_children(child)
                children[OpenValve()] = child
        
        for neighbor in [cave[tunnel] for tunnel in cave[node.location].tunnels]:
            action = MoveTo(neighbor.id)
            child = make_child(node, action)
            find_children(child)
            children[action] = child

        return children
    
    aa = cave["AA"].id
    root = ActionTree(None, 30, aa, frozenset([aa]), frozenset())
    find_children(root)
    
    return root

def solve_p1(lines: list[str]):
    cave = Cave.create([ValveInfo.parse(id, line) for id, line in enumerate(lines)])
    draw_cave(cave)

    tree = tree_of_all_possible_moves(cave)
    #print(len(tree))

    print("p1", len(lines))


def solve_p2(lines: list[str]):
    print("p2", sum(map(len, lines)))


if __name__ == "__main__":
    main()
