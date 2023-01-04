"""
Advent of Code 2022 Day 24
"""
import sys
from collections import namedtuple

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


Position = namedtuple("Position", "x y")

def load_data() -> list[list[str]]:
    return [[c for c in i] for i in get_daily_input(DAY)]


def get_next(data: list[list[str]]) -> list[list[str]]:
    top, bottom = data[0], data[-1]
    data = [[r[-2]] + r[1:-1] + [r[1]] for r in [data[-2]] + data[1:-1] + [data[1]]]
    new_data = []
    for i in range(1, len(data) - 1):
        new_data.append([])
        new_data[-1].append("#")
        for j in range(1, len(data[i]) - 1):
            d = ""
            for w, x, y in [("v", -1, 0), ("^", 1, 0), (">", 0, -1), ("<", 0, 1)]:
                if w in data[i + x][j + y]:
                    d += w
            new_data[-1].append(d if d else ".")
        new_data[-1].append("#")
    return [top] + new_data + [bottom]


def dump(data: list[list[str]]) -> str:
    return "\n".join(["".join([c if len(c) == 1 else str(len(c)) for c in d])
                      for d in data])


def part_1() -> int:
    data_frames = [load_data()]
    next_data = get_next(data_frames[-1])
    while next_data != data_frames[0]:
        data_frames.append(next_data)
        next_data = get_next(next_data)

    target = Position(len(data_frames[0]) - 1, data_frames[0][-1].index("."))
    passes: list[dict[Position, int]] = [{Position(0, 1): 0}]
    while target not in passes[-1]:
        f = len(passes) % len(data_frames)
        next_pass = {}
        for k, v in passes[-1].items():
            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                pos = Position(k.x + x, k.y + y)
                if data_frames[f][pos.x][pos.y] == ".":
                    next_pass[pos] = v + 1
        passes.append(next_pass)
    return len(passes) - 1


def part_2() -> int:
    return 42


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 247
"""