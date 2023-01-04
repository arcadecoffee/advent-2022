"""
Advent of Code 2022 Day 24
"""
import sys

from dataclasses import dataclass
from functools import cache

from advent_tools import get_daily_input

DAY = 24

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass
class Location:
    wall: bool = False
    N: bool = False
    S: bool = False
    E: bool = False
    W: bool = False

    @property
    def vacant(self) -> bool:
        return not (self.wall or self.N or self.S or self.E or self.W)

    def __repr__(self):
        if self.wall:
            return "#"

        cnt = self.N + self.S + self.E + self.W
        if not cnt:
            return "."
        if cnt > 1:
            return str(cnt)
        if self.N:
            return "^"
        if self.S:
            return "v"
        if self.E:
            return ">"
        if self.W:
            return "<"


def load_data() -> list[list[Location]]:
    locs = {".": Location(), "#": Location(wall=True), "^": Location(N=True),
            "v": Location(S=True), ">": Location(E=True), "<": Location(W=True)}
    data = [[locs[c] for c in r] for r in get_daily_input(DAY)]
    return data


class WindMap:
    def __init__(self, curr_map: list[list[Location]]):
        self.map = curr_map

    def __hash__(self):
        return hash("\n".join(["".join([str(c) for c in r]) for r in self.map]))


@cache
def get_next_map(curr: WindMap) -> WindMap:
    next_map = [curr.map[0]]
    ht, wt = len(curr.map), len(curr.map[0])
    for r in range(1, ht - 1):
        nr = [Location(wall=True)]
        for c in range(1, wt - 1):
            nr.append(
                Location(
                    N=curr.map[1][c].N if r + 2 == ht else curr.map[r + 1][c].N,
                    S=curr.map[-2][c].S if r == 1 else curr.map[r - 1][c].S,
                    E=curr.map[r][-2].E if c == 1 else curr.map[r][c - 1].E,
                    W=curr.map[r][1].W if c + 2 == wt else curr.map[r][c + 1].W
                )
            )
        nr.append(Location(wall=True))
        next_map.append(nr)
    next_map.append(curr.map[-1])
    return WindMap(next_map)


@cache
def get_options(curr: WindMap, curr_location: tuple[int, int]) -> list[tuple[int, int]]:
    options = []
    r, c = curr_location
    for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
        if 0 <= r + x < len(curr.map) and 0 <= c + y < len(curr.map[r]) and \
                curr.map[r + x][c + y].vacant:
            options.append((r + x, c + y))
    return options


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return (b[0] - a[0]) + (b[1] - a[1])


def dump_map(m: list[list[Location]]) -> str:
    return "\n".join(["".join([str(c) for c in r]) for r in m])


def part_1() -> int:
    curr: WindMap = WindMap(load_data())
    goal = len(curr.map) - 1, len(curr.map[0]) - 2

    found = []
    paths = [[(0, 1)]]
    visited = []
    while not found:
        curr = get_next_map(curr)

        next_paths = []
        for path in paths:
            if (curr, path[-1]) not in visited:
                for option in get_options(curr, path[-1]):
                    if option == goal:
                        found = path + [option]
                        break
                    next_paths.append(path + [option])
                visited.append((curr, path[-1]))
            if found:
                break
            paths = next_paths

    return len(found) - 1


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
