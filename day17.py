"""
Advent of Code 2022 Day 0
"""
import re
import sys

from copy import deepcopy
from itertools import cycle

from advent_tools import get_daily_input

DAY = 17

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


class Pile:

    rock_shapes = {
        "line": [
            "0011110",
        ],
        "cross": [
            "0001000",
            "0011100",
            "0001000",
        ],
        "elbow": [
            "0000100",
            "0000100",
            "0011100",
        ],
        "column": [
            "0010000",
            "0010000",
            "0010000",
            "0010000",
        ],
        "square": [
            "0011000",
            "0011000",
        ]
    }

    def __init__(self, wind_directions: str):
        self.wind_direction = cycle(wind_directions)
        self.rock_shape = cycle(self.rock_shapes)
        self.stack: list[int] = []

    @property
    def height(self) -> int:
        return len(self.stack)

    def drop_next(self):
        rock = [int(i, 2) for i in self.rock_shapes[next(self.rock_shape)]]
        self.stack = [0] * (3 + len(rock)) + self.stack
        for s in range(len(self.stack)):
            direction = next(self.wind_direction)
            if direction == ">":
                can_shift = True
                for r in range(len(rock)):
                    if (rock[r] & 1) or (rock[r] >> 1 & self.stack[s + r]):
                        can_shift = False
                        break
                if can_shift:
                    for r in range(len(rock)):
                        rock[r] = rock[r] >> 1
            elif direction == "<":
                can_shift = True
                for r in range(len(rock)):
                    if (rock[r] & 2**6) or (rock[r] << 1 & self.stack[s + r]):
                        can_shift = False
                        break
                if can_shift:
                    for r in range(len(rock)):
                        rock[r] = rock[r] << 1

            can_fall = True
            for r in range(len(rock)):
                if (s + r >= len(self.stack) - 1) or (rock[r] & self.stack[s + r + 1]):
                    can_fall = False
                    break
            if not can_fall:
                for r in range(len(rock)):
                    self.stack[s + r] = self.stack[s + r] | rock[r]
                break
        while self.stack[0] == 0:
            self.stack.pop(0)

    def dump(self) -> str:
        output = ""
        for r in self.stack:
            output += "|" + \
                      "".join(["#" if c == "1" else "." for c in format(r, "07b")]) + \
                      "|\n"
        output += "+-------+"
        return output


def part_1() -> int:
    pile = Pile(next(get_daily_input(DAY)))
    for _ in range(2022):
        pile.drop_next()
    return pile.height


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
