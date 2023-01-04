"""
Advent of Code 2022 Day 24
"""
import sys
from collections import namedtuple

from itertools import cycle

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


class BlizzardBasin:
    Position = namedtuple("Position", "x y")

    def __init__(self, map_state: list[list[str]]) -> None:
        self.map_frames = self.prerender_frames(map_state)
        self.map_frame_cycle = cycle(self.map_frames)
        self.height, self.width = len(map_state), len(map_state[0])
        self.start = self.Position(0, map_state[0].index("."))
        self.end = self.Position(len(map_state) - 1, map_state[-1].index("."))

    def walk(self, a: Position, b: Position) -> int:
        steps = 0
        reachable = {a: 0}
        while b not in reachable:
            next_reachable = {}
            steps += 1
            frame = next(self.map_frame_cycle)
            for k, v in reachable.items():
                for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                    pos = self.Position(k.x + x, k.y + y)
                    if (pos.x < self.height and pos.y < self.width
                            and frame[pos.x][pos.y] == "."):
                        next_reachable[pos] = v + 1
            reachable = next_reachable
        return steps

    @classmethod
    def get_next(cls, map_state: list[list[str]]) -> list[list[str]]:
        cropped_map = [[r[-2]] + r[1:-1] + [r[1]]
                       for r in [map_state[-2]] + map_state[1:-1] + [map_state[1]]]
        new_data = [map_state[0]]
        for i in range(1, len(cropped_map) - 1):
            new_row = ["#"]
            for j in range(1, len(cropped_map[i]) - 1):
                new_row.append(".".join([w for w, x, y in
                                         [("v", -1, 0), ("^", 1, 0),
                                          (">", 0, -1), ("<", 0, 1)] if
                                         w in cropped_map[i + x][j + y]]) or ".")
            new_data.append(new_row + ["#"])
        return new_data + [map_state[-1]]

    @classmethod
    def prerender_frames(cls, map_state: list[list[str]]) -> list[list[list[str]]]:
        frames: list[list[list[str]]] = []
        next_data = cls.get_next(map_state)
        while next_data != map_state:
            frames.append(next_data)
            next_data = cls.get_next(next_data)
        frames.append(map_state)
        return frames


def load_data() -> list[list[str]]:
    return [[c for c in i] for i in get_daily_input(DAY)]


def main():
    bb = BlizzardBasin(load_data())

    part_1 = bb.walk(bb.start, bb.end)
    print(f"Part 1: {part_1}")

    part_2 = part_1 + bb.walk(bb.end, bb.start) + bb.walk(bb.start, bb.end)
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
